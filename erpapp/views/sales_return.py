"""
Sales Return — Django-native inverse of sales bill.

Stores returns as `SalesBill` rows with `bill_type='Return'` and negative
amounts. Posts a `daybook` credit-note line to refund the customer when
both daybook and customer accountm are present. Recovers stock by
calling `stock.apply_sales_return_recovery(items)`.

This is a simplified port of SalesReturnController. Skipped: the legacy
`salesm/salesrm/salesrd` write paths, secondary sync, gold-rate prefill,
custom voucher numbering on the returns counter (we share `SR/` prefix
in `generals`).
"""
from __future__ import annotations

import json
from datetime import datetime
from typing import Optional

from django.db import connection, transaction
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from ..models import SalesBill
from .. import daybook_helpers as dh


def _is_authorized(request) -> bool:
    return bool((request.session.get("user_code") or "").strip())


def _read_payload(request) -> dict:
    if request.content_type and "application/json" in request.content_type:
        try:
            return json.loads(request.body or "{}") or {}
        except json.JSONDecodeError:
            return {}
    return request.POST.dict() if request.method == "POST" else request.GET.dict()


# ---------------------------------------------------------------------------
# Public views
# ---------------------------------------------------------------------------

def index(request, mode: Optional[str] = None):
    if not _is_authorized(request):
        return redirect("/login")
    mode = (mode or "bill").lower()
    if mode not in {"bill", "edit", "cancel", "reprint"}:
        mode = "bill"
    titles = {
        "bill": "Enter Sales Return Bill",
        "edit": "Edit Sales Return Bill",
        "cancel": "Cancel Sales Return Bill",
        "reprint": "Reprint Sales Return Bill",
    }
    return render(request, "sales-return/index.html", {
        "mode": mode, "title": titles[mode],
    })


def next_number(request):
    prefix = dh.general_profile("SRPREF", "SR/")
    length = max(int(dh.to_num(dh.general_profile("SBLEN", "5"))), 1)
    counter = dh.gen_int("SALESR")
    # Also derive from existing SalesBill rows that look like returns.
    for bn in SalesBill.objects.filter(bill_type="Return").values_list("bill_no", flat=True):
        suf = (bn or "").lstrip(prefix)
        if suf.isdigit():
            counter = max(counter, int(suf))
    nxt = counter + 1
    return JsonResponse({"ok": True, "bill_no": f"{prefix}{nxt:0{length}d}"})


def get_list(request):
    qs = SalesBill.objects.filter(bill_type="Return").order_by("-id")[:50]
    rows = []
    for b in qs:
        rows.append({
            "bill_no": b.bill_no,
            "bill_date": b.bill_date.isoformat() if b.bill_date else None,
            "customer_name": b.customer_name,
            "net_total": float(b.net_total or 0),
            "status": b.status,
        })
    return JsonResponse({"ok": True, "rows": rows})


def search_sale_bill(request):
    """Find a sales bill the user wants to return against (by bill_no or customer)."""
    q = (request.GET.get("q") or "").strip()
    qs = SalesBill.objects.exclude(bill_type="Return").order_by("-id")
    if q:
        qs = qs.filter(bill_no__icontains=q) | qs.filter(customer_name__icontains=q) | qs.filter(mobile__icontains=q)
    qs = qs[:25]
    rows = [{
        "bill_no": b.bill_no,
        "bill_date": b.bill_date.isoformat() if b.bill_date else None,
        "customer_name": b.customer_name,
        "customer_code": b.customer_code,
        "mobile": b.mobile,
        "net_total": float(b.net_total or 0),
        "items": _parse(b.items_json),
    } for b in qs]
    return JsonResponse({"ok": True, "rows": rows})


def get(request):
    bill_no = (request.GET.get("bill_no") or "").strip()
    if not bill_no:
        return JsonResponse({"ok": False, "message": "bill_no required"}, status=422)
    b = SalesBill.objects.filter(bill_no=bill_no, bill_type="Return").first()
    if not b:
        return JsonResponse({"ok": False, "message": "Return not found"}, status=404)
    return JsonResponse({"ok": True, "data": {
        "bill_no": b.bill_no,
        "bill_date": b.bill_date.isoformat() if b.bill_date else None,
        "customer_name": b.customer_name,
        "customer_code": b.customer_code,
        "mobile": b.mobile,
        "address": b.address,
        "net_total": float(b.net_total or 0),
        "items": _parse(b.items_json),
        "extra": _parse(b.extra_json) or {},
        "status": b.status,
    }})


@csrf_exempt
@require_http_methods(["POST"])
def save(request):
    payload = _read_payload(request)
    bill_no = (payload.get("bill_no") or "").strip()
    if not bill_no:
        return JsonResponse({"ok": False, "message": "bill_no required"}, status=422)
    customer_name = (payload.get("customer_name") or "").strip()
    if not customer_name:
        return JsonResponse({"ok": False, "message": "customer_name required"}, status=422)

    items = _coerce_lines(payload.get("items") or [])
    if not items:
        return JsonResponse({"ok": False, "message": "at least one item required"}, status=422)

    return_total = round(sum(_to_num(r.get("amount")) for r in items), 2)
    src_bill_no = (payload.get("source_bill_no") or "").strip()
    extra = {"source_bill_no": src_bill_no, "is_return": True}

    fields = {
        "bill_date": _parse_date(payload.get("bill_date")),
        "bill_type": "Return",
        "customer_code": (payload.get("customer_code") or "").strip()[:20] or None,
        "customer_name": customer_name[:120],
        "address": (payload.get("address") or "").strip()[:255] or None,
        "mobile": (payload.get("mobile") or "").strip()[:30] or None,
        "rate_per_gm": _to_num(payload.get("rate_per_gm")),
        "bill_total": -return_total,
        "exchange_amount": 0,
        "return_amount": return_total,
        "net_total": -return_total,
        "items_json": json.dumps(items),
        "exchange_json": json.dumps([]),
        "return_json": json.dumps([]),
        "extra_json": json.dumps(extra),
        "status": "saved",
    }

    with transaction.atomic():
        bill, created = SalesBill.objects.update_or_create(bill_no=bill_no, defaults=fields)

    # Recover stock + post a daybook credit note for the customer.
    stock_summary = None
    daybook_summary = None
    if created and items:
        from .stock import apply_sales_return_recovery
        stock_summary = apply_sales_return_recovery(items)

        cust_code = (payload.get("customer_code") or "").strip().upper()
        if cust_code and dh.table_exists("daybook") and dh.table_exists("daybookpart"):
            daybook_summary = _post_credit_note(
                request, bill_no=bill_no, party_accode=cust_code,
                amount=return_total, particular=f"Return {bill_no}",
                tdate=fields["bill_date"] or datetime.now().date().isoformat(),
            )

    response = {
        "ok": True, "message": "Return saved" if created else "Return updated",
        "bill_no": bill.bill_no, "net_total": float(bill.net_total or 0),
    }
    if stock_summary is not None:
        response["stock_recovery"] = stock_summary
    if daybook_summary is not None:
        response["daybook"] = daybook_summary
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["POST"])
def delete(request):
    payload = _read_payload(request)
    bill_no = (payload.get("bill_no") or "").strip()
    if not bill_no:
        return JsonResponse({"ok": False, "message": "bill_no required"}, status=422)
    b = SalesBill.objects.filter(bill_no=bill_no, bill_type="Return").first()
    if not b:
        return JsonResponse({"ok": False, "message": "Return not found"}, status=404)
    b.delete()
    return JsonResponse({"ok": True, "message": "Return deleted"})


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _to_num(v) -> float:
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def _parse(j):
    try:
        return json.loads(j) if j else []
    except (TypeError, ValueError, json.JSONDecodeError):
        return []


def _parse_date(s) -> Optional[str]:
    return dh.parse_date(s)


def _coerce_lines(rows) -> list:
    out = []
    for r in rows:
        if not isinstance(r, dict):
            continue
        code = (r.get("item_code") or "").strip()
        if not code:
            continue
        qty = _to_num(r.get("qty"))
        weight = _to_num(r.get("weight"))
        stone_wgt = _to_num(r.get("stone_wgt"))
        rate = _to_num(r.get("rate"))
        amount = _to_num(r.get("amount"))
        if amount == 0:
            net_wgt = max(weight - stone_wgt, 0)
            amount = net_wgt * rate + _to_num(r.get("stone_price")) + _to_num(r.get("making_charge"))
        out.append({
            **r, "item_code": code,
            "qty": qty, "weight": weight, "stone_wgt": stone_wgt,
            "rate": rate, "amount": round(amount, 2),
        })
    return out


def _post_credit_note(request, *, bill_no: str, party_accode: str,
                      amount: float, particular: str, tdate: str) -> dict:
    """Credit-note daybook entry: party gets a credit, return-control account a debit.

    Uses the legacy SCB (Sales Credit Note) account code from generals if
    available; falls back to 'CASH'.
    """
    if amount <= 0:
        return {"posted": False, "reason": "zero amount"}
    cb_accode = dh.general_profile("RDISCAC", "CASH")  # offset account
    try:
        with transaction.atomic():
            slno = dh.next_serial_no()
            prefix = dh.general_profile("SRPREF", "SR/")
            vchno = dh.reserve_voucher(prefix, "SRCOUNT")
            # For a sales return, party account is credited (-amount) and
            # the offset (cash/sales-return) is debited (+amount). post_voucher
            # with direction='P' models that: party -= amount, cb += amount.
            dh.post_voucher(
                slno=slno, tdate=tdate, vchno=vchno, control=1,
                user_code=request.session.get("user_code") or "",
                cb_accode=cb_accode, party_accode=party_accode,
                amount=amount, direction="P", particular=particular,
            )
        return {"posted": True, "slno": slno, "vchno": vchno}
    except Exception as e:
        return {"posted": False, "reason": str(e)}
