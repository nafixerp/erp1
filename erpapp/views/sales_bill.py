"""
Sales bill — port of SalesBillController.

Implemented:
  - index            (entry/edit/cancel/reprint shell — simplified; the
                     full Laravel index loads rates, items, counters,
                     salesmen via many legacy tables; we render a minimal
                     entry form that calls our APIs.)
  - search           list saved bills (sales_bills)
  - get              fetch by bill_no
  - save             upsert into sales_bills
  - cancel_bill      hard-delete from sales_bills
  - confirm_bill     mark confirmed
  - next_bill_no     simplified next-number (max+1 from sales_bills)
  - check_bill_no
  - customer_search  query clients
  - customer_details / customer_by_mobile

Skipped (still stubbed): e-invoice, recalc, prev/next nav, quotation
list, item-lookup, edit/reprint/cancel pickers, secondary-DB sync,
all legacy salesm/salesd write paths.
"""
from __future__ import annotations

import json
import re
from datetime import date, datetime
from typing import Optional

from django.db import connection, transaction
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from ..models import SalesBill


VALID_MODES = {"bill", "edit", "cancel", "reprint", "confirmation"}


def _is_authorized(request) -> bool:
    return bool((request.session.get("user_code") or "").strip())


def _read_payload(request) -> dict:
    if request.content_type and "application/json" in request.content_type:
        try:
            return json.loads(request.body or "{}") or {}
        except json.JSONDecodeError:
            return {}
    if request.method == "GET":
        return request.GET.dict()
    return request.POST.dict()


def _table_exists(name: str) -> bool:
    try:
        with connection.cursor() as cur:
            cur.execute("SHOW TABLES LIKE %s", [name])
            return cur.fetchone() is not None
    except Exception:
        return False


def _row_dict(cur):
    cols = [c[0] for c in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]


def _to_num(v) -> float:
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def _parse_date(s: str) -> Optional[date]:
    s = (s or "").strip()
    if not s:
        return None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%m/%d/%Y"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


# ---------------------------------------------------------------------------
# Public views
# ---------------------------------------------------------------------------

def index(request, mode: Optional[str] = None):
    if not _is_authorized(request):
        return redirect("/login")
    mode = (mode or request.GET.get("mode") or "bill").lower()
    if mode not in VALID_MODES:
        mode = "bill"
    quotation = request.GET.get("qtn") in ("1", "true") or request.GET.get("quotation") in ("1", "true")
    titles = {
        "bill": "Enter Sales Bill Details",
        "edit": "Edit Sales Bill",
        "cancel": "Cancel Sales Bill",
        "reprint": "Reprint Sales Bill",
        "confirmation": "Bill Confirmation",
    }
    if quotation and mode == "bill":
        titles["bill"] = "Enter Sales Quotation Details"
    return render(request, "sales-bill/index.html", {
        "mode": mode,
        "title": titles[mode],
        "quotation": quotation,
    })


def next_bill_no(request):
    seb = (request.GET.get("seb") or "B").strip().upper()
    if seb not in ("B", "E"):
        seb = "B"
    bill_type = (request.GET.get("bill_type") or "Gold").strip()

    prefix = _read_generals_value("SBPREF" if seb == "B" else "SEPREF",
                                  "SL/" if seb == "B" else "SLE/")
    length = max(int(_to_num(_read_generals_value("SBLEN" if seb == "B" else "SELEN", "5"))), 1)
    counter = _read_generali_counter(f"SALES{seb}")

    candidate_no = counter + 1
    while True:
        candidate = f"{prefix}{candidate_no:0{length}d}"
        if not _bill_no_exists(candidate):
            break
        candidate_no += 1

    tax_perc = 0.0  # simplified; full controller looks up salestype.taxperc by bill_type
    return JsonResponse({"ok": True, "bill_no": candidate, "tax_perc": tax_perc, "bill_type": bill_type})


def check_bill_no(request):
    bill_no = (request.GET.get("bill_no") or "").strip()
    current = (request.GET.get("current_bill_no") or "").strip()
    if not bill_no:
        return JsonResponse({"ok": False, "message": "Bill number required."}, status=422)
    if current and bill_no.lower() == current.lower():
        return JsonResponse({"ok": True, "duplicate": False})
    exists = _bill_no_exists(bill_no)
    return JsonResponse({
        "ok": True,
        "duplicate": exists,
        "message": "This Bill Number already exist..." if exists else "",
    })


def get(request):
    bill_no = (request.GET.get("bill_no") or "").strip()
    if not bill_no:
        return JsonResponse({"ok": False, "message": "Bill number required."}, status=422)
    bill = SalesBill.objects.filter(bill_no=bill_no).first()
    if not bill:
        return JsonResponse({"ok": False, "message": "Bill not found."}, status=404)
    return JsonResponse({"ok": True, "data": _map_bill(bill)})


def search(request):
    q = (request.GET.get("q") or "").strip()
    qs = SalesBill.objects.all()
    if q:
        qs = qs.filter(bill_no__icontains=q) | qs.filter(customer_name__icontains=q)
    rows = list(qs.order_by("-id").values(
        "bill_no", "bill_date", "customer_name", "net_total", "status"
    )[:25])
    for r in rows:
        if r["bill_date"]:
            r["bill_date"] = r["bill_date"].isoformat()
        r["net_total"] = float(r["net_total"] or 0)
    return JsonResponse({"ok": True, "rows": rows})


def customer_search(request):
    q = (request.GET.get("q") or "").strip()
    preload = (request.GET.get("preload") or "").lower() in ("1", "true", "yes")
    if not q and not preload:
        return JsonResponse({"ok": True, "rows": []})
    if not _table_exists("clients"):
        return JsonResponse({"ok": True, "rows": []})

    type_ = (request.GET.get("type") or "C").strip().upper()
    where = ["1=1"]
    params: list = []
    if type_ and type_ != "ALL":
        where.append("ctype = %s")
        params.append(type_)
    where.append("(removed <> 1 OR removed IS NULL)")
    if q:
        s = f"%{q}%"
        where.append("(code LIKE %s OR name LIKE %s OR mobile LIKE %s OR telephone LIKE %s)")
        params += [s, s, s, s]
    sql = (
        "SELECT code, name, mobile, telephone, addr1, city, state, panadhar AS gst_no "
        "FROM clients WHERE " + " AND ".join(where) + " ORDER BY name LIMIT 50"
    )
    try:
        with connection.cursor() as cur:
            cur.execute(sql, params)
            rows = _row_dict(cur)
    except Exception:
        rows = []
    return JsonResponse({"ok": True, "rows": rows})


def customer_details(request):
    code = (request.GET.get("code") or "").strip()
    if not code:
        return JsonResponse({"ok": False, "message": "code required"}, status=422)
    row = _customer_row({"code": code})
    if not row:
        return JsonResponse({"ok": False, "message": "Not found"}, status=404)
    return JsonResponse({"ok": True, "data": row})


def customer_by_mobile(request):
    mobile = (request.GET.get("mobile") or "").strip()
    if not mobile:
        return JsonResponse({"ok": False, "message": "mobile required"}, status=422)
    row = _customer_row({"mobile": mobile})
    if not row:
        return JsonResponse({"ok": False, "data": None})
    return JsonResponse({"ok": True, "data": row})


@csrf_exempt
@require_http_methods(["POST"])
def save(request):
    payload = _read_payload(request)
    bill_no = (payload.get("bill_no") or "").strip()
    if not bill_no:
        return JsonResponse({"ok": False, "message": "bill_no required"}, status=422)
    if not (payload.get("customer_name") or "").strip():
        return JsonResponse({"ok": False, "message": "customer_name required"}, status=422)

    items = _coerce_lines(payload.get("items") or [], with_calc=True)
    exchange = _coerce_lines(payload.get("exchange") or [])
    sales_return = _coerce_lines(payload.get("sales_return") or [])

    bill_total = round(sum(_to_num(r.get("amount")) for r in items), 2)
    exchange_amount = round(sum(_to_num(r.get("amount")) for r in exchange), 2)
    return_amount = round(sum(_to_num(r.get("amount")) for r in sales_return), 2)
    net_total = round(bill_total - exchange_amount - return_amount, 2)

    extra = payload.get("extra") or {}
    if isinstance(extra, str):
        try:
            extra = json.loads(extra) or {}
        except json.JSONDecodeError:
            extra = {}
    if payload.get("is_quotation"):
        extra["is_quotation"] = True
    if payload.get("source_quotation_bill_no"):
        extra["source_quotation_bill_no"] = (payload["source_quotation_bill_no"] or "").strip()

    fields = {
        "bill_date": _parse_date(str(payload.get("bill_date") or "")),
        "bill_time": (payload.get("bill_time") or "").strip()[:20] or None,
        "bill_type": (payload.get("bill_type") or "Gold").strip()[:30],
        "customer_code": (payload.get("customer_code") or "").strip()[:20] or None,
        "customer_name": (payload.get("customer_name") or "").strip()[:120],
        "address": (payload.get("address") or "").strip()[:255] or None,
        "mobile": (payload.get("mobile") or "").strip()[:30] or None,
        "gst_no": (payload.get("gst_no") or "").strip()[:40] or None,
        "pan_no": (payload.get("pan_no") or "").strip()[:30] or None,
        "state_code": (payload.get("state_code") or "").strip()[:20] or None,
        "rate_per_gm": _to_num(payload.get("rate_per_gm")),
        "counter_name": (payload.get("counter_name") or "").strip()[:80] or None,
        "counter_code": (payload.get("counter_code") or "").strip()[:20] or None,
        "salesman_name": (payload.get("salesman_name") or "").strip()[:120] or None,
        "salesman_code": (payload.get("salesman_code") or "").strip()[:20] or None,
        "agent_code": (payload.get("agent_code") or "").strip()[:20] or None,
        "approved_by": (payload.get("approved_by") or "").strip()[:20] or None,
        "cashbank_code": (payload.get("cashbank_code") or "").strip()[:20] or None,
        "bill_total": bill_total,
        "exchange_amount": exchange_amount,
        "return_amount": return_amount,
        "net_total": net_total,
        "items_json": json.dumps(items),
        "exchange_json": json.dumps(exchange),
        "return_json": json.dumps(sales_return),
        "extra_json": json.dumps(extra),
    }

    with transaction.atomic():
        bill, created = SalesBill.objects.update_or_create(bill_no=bill_no, defaults=fields)
        if not created and bill.status == "cancelled":
            return JsonResponse({"ok": False, "message": "Cancelled bill cannot be modified."}, status=422)

    # Deduct inventory on first save of a non-quotation bill. Re-saves and
    # quotations don't trigger another deduction. Cancellation/edit-aware
    # inventory recovery is a follow-up.
    stock_summary = None
    if created and not extra.get("is_quotation") and items:
        from .stock import apply_sales_bill_deduction
        stock_summary = apply_sales_bill_deduction(items)

    next_bill_no_value = _next_simple(bill.bill_type or "Gold")
    response = {
        "ok": True,
        "message": "Bill saved" if created else "Bill updated",
        "data": _map_bill(bill),
        "next_bill_no": next_bill_no_value,
    }
    if stock_summary is not None:
        response["stock_adjustment"] = stock_summary
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["POST"])
def cancel_bill(request):
    payload = _read_payload(request)
    bill_no = (payload.get("bill_no") or "").strip()
    if not bill_no:
        return JsonResponse({"ok": False, "message": "bill_no required"}, status=422)
    bill = SalesBill.objects.filter(bill_no=bill_no).first()
    if not bill:
        return JsonResponse({"ok": False, "message": "Bill not found."}, status=404)
    bill.delete()
    return JsonResponse({"ok": True, "message": "Bill deleted from database."})


@csrf_exempt
@require_http_methods(["POST"])
def confirm_bill(request):
    payload = _read_payload(request)
    bill_no = (payload.get("bill_no") or "").strip()
    if not bill_no:
        return JsonResponse({"ok": False, "message": "bill_no required"}, status=422)
    bill = SalesBill.objects.filter(bill_no=bill_no).first()
    if not bill:
        return JsonResponse({"ok": False, "message": "Bill not found."}, status=404)
    if bill.status == "cancelled":
        return JsonResponse({"ok": False, "message": "Cancelled bill cannot be confirmed."}, status=422)
    bill.status = "confirmed"
    bill.confirmed_at = datetime.now()
    bill.save(update_fields=["status", "confirmed_at", "updated_at"])
    return JsonResponse({"ok": True, "message": "Bill confirmed."})


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _bill_no_exists(bill_no: str) -> bool:
    return SalesBill.objects.filter(bill_no=bill_no).exists()


def _read_generals_value(code: str, default: str) -> str:
    if not _table_exists("generals"):
        return default
    try:
        with connection.cursor() as cur:
            cur.execute("SELECT cvalue FROM generals WHERE code = %s LIMIT 1", [code])
            row = cur.fetchone()
            if row and row[0] is not None and str(row[0]).strip():
                return str(row[0])
    except Exception:
        pass
    return default


def _read_generali_counter(code: str) -> int:
    if not _table_exists("generali"):
        # Fall back to derive from sales_bills numeric suffix.
        return _max_numeric_suffix()
    try:
        with connection.cursor() as cur:
            cur.execute("SELECT cvalue FROM generali WHERE code = %s LIMIT 1", [code])
            row = cur.fetchone()
            if row and row[0] is not None:
                return int(_to_num(row[0]))
    except Exception:
        pass
    return _max_numeric_suffix()


def _max_numeric_suffix() -> int:
    """Find largest trailing integer in any bill_no in sales_bills."""
    best = 0
    for bn in SalesBill.objects.values_list("bill_no", flat=True):
        m = re.search(r"(\d+)$", bn or "")
        if m:
            best = max(best, int(m.group(1)))
    return best


def _next_simple(bill_type: str) -> str:
    counter = _max_numeric_suffix() + 1
    prefix = _read_generals_value("SBPREF", "SL/")
    length = max(int(_to_num(_read_generals_value("SBLEN", "5"))), 1)
    candidate_no = counter
    while True:
        candidate = f"{prefix}{candidate_no:0{length}d}"
        if not _bill_no_exists(candidate):
            return candidate
        candidate_no += 1


def _coerce_lines(rows, with_calc: bool = False) -> list:
    out = []
    for r in rows:
        if not isinstance(r, dict):
            continue
        if not (r.get("item_code") or "").strip():
            continue
        qty = _to_num(r.get("qty"))
        weight = _to_num(r.get("weight"))
        stone_wgt = _to_num(r.get("stone_wgt"))
        stone_price = _to_num(r.get("stone_price"))
        making_charge = _to_num(r.get("making_charge"))
        rate = _to_num(r.get("rate"))
        amount = _to_num(r.get("amount"))
        if with_calc and amount == 0.0:
            net_wgt = max(weight - stone_wgt, 0)
            amount = net_wgt * rate + stone_price + making_charge
        out.append({
            **r,
            "qty": qty,
            "weight": weight,
            "stone_wgt": stone_wgt,
            "net_wgt": max(weight - stone_wgt, 0),
            "stone_price": stone_price,
            "making_charge": making_charge,
            "rate": rate,
            "amount": round(amount, 2),
        })
    return out


def _customer_row(filt: dict) -> Optional[dict]:
    if not _table_exists("clients"):
        return None
    where, params = [], []
    if filt.get("code"):
        where.append("TRIM(COALESCE(code,'')) = %s")
        params.append(filt["code"].strip())
    if filt.get("mobile"):
        where.append("(TRIM(COALESCE(mobile,'')) = %s OR TRIM(COALESCE(telephone,'')) = %s)")
        params += [filt["mobile"].strip(), filt["mobile"].strip()]
    if not where:
        return None
    sql = (
        "SELECT code, name, addr1, addr2, city, state, mobile, telephone, "
        "panadhar AS gst_no, idno AS pan_no "
        "FROM clients WHERE " + " AND ".join(where) + " LIMIT 1"
    )
    try:
        with connection.cursor() as cur:
            cur.execute(sql, params)
            rows = _row_dict(cur)
    except Exception:
        return None
    return rows[0] if rows else None


def _map_bill(bill: SalesBill) -> dict:
    def _load(j):
        try:
            return json.loads(j) if j else []
        except (TypeError, ValueError, json.JSONDecodeError):
            return []
    extra = {}
    if bill.extra_json:
        try:
            extra = json.loads(bill.extra_json) or {}
        except (TypeError, ValueError, json.JSONDecodeError):
            extra = {}
    return {
        "bill_no": bill.bill_no,
        "bill_date": bill.bill_date.isoformat() if bill.bill_date else None,
        "bill_time": bill.bill_time,
        "bill_type": bill.bill_type,
        "customer_name": bill.customer_name,
        "customer_code": bill.customer_code,
        "address": bill.address,
        "mobile": bill.mobile,
        "gst_no": bill.gst_no,
        "pan_no": bill.pan_no,
        "state_code": bill.state_code,
        "rate_per_gm": float(bill.rate_per_gm or 0),
        "counter_name": bill.counter_name,
        "counter_code": bill.counter_code,
        "salesman_name": bill.salesman_name,
        "salesman_code": bill.salesman_code,
        "agent_code": bill.agent_code,
        "approved_by": bill.approved_by,
        "cashbank_code": bill.cashbank_code,
        "bill_total": float(bill.bill_total or 0),
        "exchange_amount": float(bill.exchange_amount or 0),
        "return_amount": float(bill.return_amount or 0),
        "net_total": float(bill.net_total or 0),
        "status": bill.status,
        "cancel_reason": bill.cancel_reason,
        "is_quotation": bool(extra.get("is_quotation")),
        "source_quotation_bill_no": (extra.get("source_quotation_bill_no") or "").strip(),
        "items": _load(bill.items_json),
        "exchange": _load(bill.exchange_json),
        "sales_return": _load(bill.return_json),
        "extra": extra,
    }
