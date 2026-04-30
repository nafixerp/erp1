"""
Receipts, payments, journal, and the day-book listing.

  - receipt_index / receipt_api  -> ReceiptController index + api dispatcher
  - payment_index / payment_api  -> PaymentController index + api dispatcher
  - journal_index / journal_api  -> JournalController
  - daybook_index                -> DayBookController index (list of vouchers)

The api endpoints accept ?action=<init|account_list|load_account|save|list|delete>
matching the legacy controllers' shape.
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

from .. import daybook_helpers as dh


# ---------------------------------------------------------------------------
# Common helpers
# ---------------------------------------------------------------------------

def _is_authorized(request) -> bool:
    return bool((request.session.get("user_code") or "").strip())


def _control(request) -> int:
    c = int(request.session.get("gilevel") or 1)
    return c if c > 0 else 1


def _read_payload(request) -> dict:
    if request.content_type and "application/json" in request.content_type:
        try:
            return json.loads(request.body or "{}") or {}
        except json.JSONDecodeError:
            return {}
    if request.method == "GET":
        return request.GET.dict()
    return request.POST.dict()


def _trim_upper(v) -> str:
    return (str(v) if v is not None else "").strip().upper()


# ---------------------------------------------------------------------------
# Receipts
# ---------------------------------------------------------------------------

def receipt_index(request):
    if not _is_authorized(request):
        return redirect("/login")
    return render(request, "receipt/index.html", {"voucher_type": "Receipt"})


@csrf_exempt
def receipt_api(request):
    return _voucher_api(request, direction="R")


def payment_index(request):
    if not _is_authorized(request):
        return redirect("/login")
    return render(request, "receipt/index.html", {"voucher_type": "Payment"})


@csrf_exempt
def payment_api(request):
    return _voucher_api(request, direction="P")


def _voucher_prefix(direction: str) -> tuple:
    """Returns (prefix, counter_code) for receipt / payment."""
    if direction == "R":
        prefix = dh.general_profile("RVPREF", "RV/")
        counter = "RVCOUNT"
    else:
        prefix = dh.general_profile("PVPREF", "PV/")
        counter = "PVCOUNT"
    return prefix, counter


def _voucher_api(request, direction: str) -> JsonResponse:
    if not _is_authorized(request):
        return JsonResponse({"success": False, "error": "Unauthorized"}, status=401)
    payload = _read_payload(request)
    action = (payload.get("action") or "").strip().lower()
    control = _control(request)

    if action == "init":
        return _action_init(request, direction, control)
    if action == "account_list":
        return JsonResponse({
            "success": True,
            "data": dh.list_accounts(payload.get("type") or "A", payload.get("search") or ""),
        })
    if action == "load_account":
        accode = _trim_upper(payload.get("accode"))
        if not accode:
            return JsonResponse({"success": False, "error": "Account code required"})
        bal = dh.account_balance(accode, control)
        return JsonResponse({
            "success": True, "accode": accode,
            "balance": round(bal, 2),
            "balance_label": "Cr" if bal >= 0 else "Dr",
        })
    if action == "save":
        return _action_save(request, payload, direction, control)
    if action == "list":
        return _action_list(direction, control,
                            (payload.get("from") or ""), (payload.get("to") or ""))
    if action == "delete":
        return _action_delete(payload)
    return JsonResponse({"success": False, "error": "Invalid action"}, status=400)


def _action_init(request, direction: str, control: int) -> JsonResponse:
    cb_accounts = dh.list_cash_bank_accounts()
    default_cb = ""
    for r in cb_accounts:
        if (r.get("accode") or "").upper() == "CASH":
            default_cb = r.get("accode")
            break
    if not default_cb and cb_accounts:
        default_cb = cb_accounts[0].get("accode") or ""

    prefix, counter = _voucher_prefix(direction)
    next_vchno = dh.preview_voucher(prefix, counter)

    disc_code = dh.general_profile("RDISCAC" if direction == "R" else "PDISCAC", "DISC")
    return JsonResponse({
        "success": True,
        "direction": direction,
        "control": control,
        "next_vchno": next_vchno,
        "default_cb": default_cb,
        "cb_accounts": cb_accounts,
        "disc_accode": disc_code,
        "today": datetime.now().date().isoformat(),
    })


def _action_save(request, payload: dict, direction: str, control: int) -> JsonResponse:
    if not dh.table_exists("daybook") or not dh.table_exists("daybookpart"):
        return JsonResponse({"success": False, "error": "daybook tables missing"}, status=500)

    tdate = dh.parse_date(payload.get("tdate"))
    if not tdate:
        return JsonResponse({"success": False, "error": "Valid date is required"}, status=422)

    cb_accode = _trim_upper(payload.get("cbcode"))
    party_accode = _trim_upper(payload.get("accode"))
    amount = abs(dh.to_num(payload.get("amount")))
    discount = abs(dh.to_num(payload.get("discount")))
    particular = (payload.get("particular") or "").strip()
    mode = (payload.get("mode") or "A").strip().upper()
    edit_slno = int(payload.get("slno") or 0)

    if not cb_accode:
        return JsonResponse({"success": False, "error": "Cash/Bank account is required"}, status=422)
    if not party_accode:
        return JsonResponse({"success": False, "error": "Account code is required"}, status=422)
    if amount <= 0:
        return JsonResponse({"success": False, "error": "Amount must be > 0"}, status=422)

    prefix, counter = _voucher_prefix(direction)
    disc_code = dh.general_profile(
        "RDISCAC" if direction == "R" else "PDISCAC", "DISC"
    )

    try:
        with transaction.atomic():
            if mode == "E" and edit_slno > 0:
                with connection.cursor() as cur:
                    cur.execute("DELETE FROM daybook WHERE slno = %s", [edit_slno])
                    cur.execute("DELETE FROM daybookpart WHERE slno = %s", [edit_slno])
                slno = edit_slno
                vchno = (payload.get("vchno") or "").strip() or dh.reserve_voucher(prefix, counter)
            else:
                slno = dh.next_serial_no()
                vchno = dh.reserve_voucher(prefix, counter)

            dh.post_voucher(
                slno=slno, tdate=tdate, vchno=vchno, control=control,
                user_code=request.session.get("user_code") or "",
                cb_accode=cb_accode, party_accode=party_accode,
                amount=amount, direction=direction, particular=particular,
                discount=discount, discount_accode=disc_code if discount else None,
                extra_dp_fields={
                    "rate": dh.to_num(payload.get("rate")),
                    "taxperc": dh.to_num(payload.get("taxperc")),
                    "taxamt": dh.to_num(payload.get("taxamt")),
                    "interstate": "Y" if payload.get("interstate") else "N",
                    "taxreverse": "Y" if payload.get("taxreverse") else "N",
                    "chequeno": (payload.get("chequeno") or "").strip(),
                    "chequedate": dh.parse_date(payload.get("chequedate")),
                    "duedate": dh.parse_date(payload.get("duedate")),
                    "staff": (payload.get("staff") or "").strip(),
                },
            )
    except Exception as e:
        return JsonResponse({"success": False, "error": f"Error saving: {e}"}, status=500)

    return JsonResponse({
        "success": True, "slno": slno, "vchno": vchno,
        "balance": round(dh.account_balance(party_accode, control), 2),
        "next_vchno": dh.preview_voucher(prefix, counter),
    })


def _action_list(direction: str, control: int, frm: str, to: str) -> JsonResponse:
    if not dh.table_exists("daybook") or not dh.table_exists("daybookpart"):
        return JsonResponse({"success": True, "rows": []})
    prefix, _ = _voucher_prefix(direction)
    where = ["dp.vchno LIKE %s", "db.control = %s"]
    params: list = [f"{prefix}%", control]
    f = dh.parse_date(frm)
    t = dh.parse_date(to)
    if f:
        where.append("dp.tdate >= %s"); params.append(f)
    if t:
        where.append("dp.tdate <= %s"); params.append(t)
    sql = (
        "SELECT dp.slno, dp.vchno, dp.tdate, dp.particular, "
        "       SUM(CASE WHEN db.amount > 0 THEN db.amount ELSE 0 END) AS amount, "
        "       MIN(CASE WHEN db.amount > 0 THEN db.accode END) AS party, "
        "       MIN(CASE WHEN db.amount < 0 THEN db.accode END) AS cb "
        "FROM daybookpart dp JOIN daybook db ON db.slno = dp.slno "
        "WHERE " + " AND ".join(where) +
        " GROUP BY dp.slno, dp.vchno, dp.tdate, dp.particular "
        "ORDER BY dp.tdate DESC, dp.slno DESC LIMIT 200"
    )
    try:
        with connection.cursor() as cur:
            cur.execute(sql, params)
            rows = dh.row_dicts(cur)
    except Exception:
        rows = []
    return JsonResponse({"success": True, "rows": rows})


def _action_delete(payload: dict) -> JsonResponse:
    slno = int(payload.get("slno") or 0)
    if slno <= 0:
        return JsonResponse({"success": False, "error": "slno required"}, status=422)
    if not dh.table_exists("daybook"):
        return JsonResponse({"success": False, "error": "daybook missing"}, status=500)
    with transaction.atomic(), connection.cursor() as cur:
        cur.execute("DELETE FROM daybook WHERE slno = %s", [slno])
        cur.execute("DELETE FROM daybookpart WHERE slno = %s", [slno])
    return JsonResponse({"success": True, "deleted_slno": slno})


# ---------------------------------------------------------------------------
# Journal
# ---------------------------------------------------------------------------

def journal_index(request):
    if not _is_authorized(request):
        return redirect("/login")
    return render(request, "journal/index.html", {})


@csrf_exempt
def journal_api(request):
    if not _is_authorized(request):
        return JsonResponse({"success": False, "error": "Unauthorized"}, status=401)
    payload = _read_payload(request)
    action = (payload.get("action") or "").strip().lower()
    control = _control(request)

    if action == "init":
        prefix = dh.general_profile("JVPREF", "JV/")
        return JsonResponse({
            "success": True, "control": control,
            "next_vchno": dh.preview_voucher(prefix, "JVCOUNT"),
            "today": datetime.now().date().isoformat(),
        })
    if action == "account_list":
        return JsonResponse({
            "success": True,
            "data": dh.list_accounts(payload.get("type") or "A", payload.get("search") or ""),
        })
    if action == "save":
        debit = _trim_upper(payload.get("debit_accode"))
        credit = _trim_upper(payload.get("credit_accode"))
        amount = abs(dh.to_num(payload.get("amount")))
        tdate = dh.parse_date(payload.get("tdate"))
        if not debit or not credit:
            return JsonResponse({"success": False, "error": "debit and credit accounts required"}, status=422)
        if amount <= 0:
            return JsonResponse({"success": False, "error": "amount must be > 0"}, status=422)
        if not tdate:
            return JsonResponse({"success": False, "error": "valid date required"}, status=422)
        prefix = dh.general_profile("JVPREF", "JV/")
        try:
            with transaction.atomic():
                slno = dh.next_serial_no()
                vchno = dh.reserve_voucher(prefix, "JVCOUNT")
                dh.post_journal(
                    slno=slno, tdate=tdate, vchno=vchno, control=control,
                    user_code=request.session.get("user_code") or "",
                    debit_accode=debit, credit_accode=credit, amount=amount,
                    particular=(payload.get("particular") or "")[:200],
                )
        except Exception as e:
            return JsonResponse({"success": False, "error": f"Error: {e}"}, status=500)
        return JsonResponse({
            "success": True, "slno": slno, "vchno": vchno,
            "next_vchno": dh.preview_voucher(prefix, "JVCOUNT"),
        })
    if action == "list":
        return _action_journal_list(control,
                                    payload.get("from") or "",
                                    payload.get("to") or "")
    return JsonResponse({"success": False, "error": "Invalid action"}, status=400)


def _action_journal_list(control: int, frm: str, to: str) -> JsonResponse:
    if not dh.table_exists("daybookpart"):
        return JsonResponse({"success": True, "rows": []})
    prefix = dh.general_profile("JVPREF", "JV/")
    where = ["dp.vchno LIKE %s", "db.control = %s"]
    params: list = [f"{prefix}%", control]
    f = dh.parse_date(frm); t = dh.parse_date(to)
    if f:
        where.append("dp.tdate >= %s"); params.append(f)
    if t:
        where.append("dp.tdate <= %s"); params.append(t)
    sql = (
        "SELECT dp.slno, dp.vchno, dp.tdate, dp.particular, "
        "       MIN(CASE WHEN db.amount > 0 THEN db.accode END) AS debit, "
        "       MIN(CASE WHEN db.amount < 0 THEN db.accode END) AS credit, "
        "       SUM(CASE WHEN db.amount > 0 THEN db.amount ELSE 0 END) AS amount "
        "FROM daybookpart dp JOIN daybook db ON db.slno = dp.slno "
        "WHERE " + " AND ".join(where) +
        " GROUP BY dp.slno, dp.vchno, dp.tdate, dp.particular "
        "ORDER BY dp.tdate DESC, dp.slno DESC LIMIT 200"
    )
    try:
        with connection.cursor() as cur:
            cur.execute(sql, params)
            rows = dh.row_dicts(cur)
    except Exception:
        rows = []
    return JsonResponse({"success": True, "rows": rows})


# ---------------------------------------------------------------------------
# DayBook (list of all vouchers within a date range)
# ---------------------------------------------------------------------------

def daybook_index(request):
    if not _is_authorized(request):
        return redirect("/login")
    return render(request, "daybook/index.html", {})


def daybook_api(request):
    if not _is_authorized(request):
        return JsonResponse({"success": False, "error": "Unauthorized"}, status=401)
    if not dh.table_exists("daybookpart") or not dh.table_exists("daybook"):
        return JsonResponse({"success": True, "rows": [], "totals": {"debit": 0, "credit": 0}})

    control = _control(request)
    frm = dh.parse_date(request.GET.get("from"))
    to = dh.parse_date(request.GET.get("to"))
    accode = _trim_upper(request.GET.get("accode"))

    where = ["db.control = %s"]
    params: list = [control]
    if frm:
        where.append("dp.tdate >= %s"); params.append(frm)
    if to:
        where.append("dp.tdate <= %s"); params.append(to)
    if accode:
        where.append("TRIM(db.accode) = %s"); params.append(accode)

    sql = (
        "SELECT dp.slno, dp.vchno, dp.tdate, dp.particular, "
        "       db.accode, db.amount, db.opaccode "
        "FROM daybookpart dp JOIN daybook db ON db.slno = dp.slno "
        "WHERE " + " AND ".join(where) +
        " ORDER BY dp.tdate DESC, dp.slno DESC LIMIT 500"
    )
    try:
        with connection.cursor() as cur:
            cur.execute(sql, params)
            rows = dh.row_dicts(cur)
    except Exception:
        rows = []

    debit = sum(float(r["amount"] or 0) for r in rows if float(r["amount"] or 0) > 0)
    credit = sum(-float(r["amount"] or 0) for r in rows if float(r["amount"] or 0) < 0)
    return JsonResponse({
        "success": True, "rows": rows,
        "totals": {"debit": round(debit, 2), "credit": round(credit, 2)},
    })
