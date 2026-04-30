"""
Customer master — port of NativeCustomerController.

Implemented: index (list), add/edit (form), get, save, delete, nextCode,
checkPhone, checkIdNo. Skipped (still stubbed by _generated_views): photo
upload, CSV import, secondary-DB sync, advanced/clientsgs upserts, kuri
helpers. Re-add those by extending the helpers below.
"""
from __future__ import annotations

import json
import re
from typing import Optional

from django.db import connection, transaction
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

VALID_TYPES = {"C", "S", "F", "D", "G", "R", "J"}
TYPE_INFO = {
    "C": {"title": "Customer", "plural": "Customers"},
    "S": {"title": "Supplier", "plural": "Suppliers"},
    "F": {"title": "Staff", "plural": "Staff"},
    "D": {"title": "Depositor", "plural": "Depositors"},
    "G": {"title": "Goldsmith", "plural": "Goldsmiths"},
    "R": {"title": "Refiner", "plural": "Refiners"},
    "J": {"title": "Jewellery", "plural": "Jewellery"},
}


def _normalize_type(t: str) -> str:
    t = (t or "").strip().upper()
    return t if t in VALID_TYPES else "C"


def _table_exists(name: str) -> bool:
    try:
        with connection.cursor() as cur:
            cur.execute("SHOW TABLES LIKE %s", [name])
            return cur.fetchone() is not None
    except Exception:
        return False


def _columns(table: str) -> set:
    try:
        with connection.cursor() as cur:
            cur.execute(f"SHOW COLUMNS FROM `{table}`")
            return {r[0].lower() for r in cur.fetchall()}
    except Exception:
        return set()


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


def _row_dict(cur):
    cols = [c[0] for c in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]


def _normalize_phone(phone: str) -> str:
    return re.sub(r"[^0-9]", "", (phone or "").strip())


# ---------------------------------------------------------------------------
# Public views
# ---------------------------------------------------------------------------

def index(request):
    if not _is_authorized(request):
        return redirect("/login")

    type_ = _normalize_type(request.GET.get("type", "C"))
    show_list = request.GET.get("list", "") == "1"
    if not show_list:
        return redirect(f"/customer/add?type={type_}")

    search = (request.GET.get("search") or "").strip()
    no_removed = request.GET.get("noremoved", "1") != "0"

    customers = _query_by_type(type_, search, no_removed)
    return render(request, "customer/list.html", {
        "type": type_,
        "type_info": TYPE_INFO[type_],
        "customers": customers,
        "search": search,
        "no_removed": no_removed,
    })


def add(request):
    if not _is_authorized(request):
        return redirect("/login")
    type_ = _normalize_type(request.GET.get("type", "C"))
    return render(request, "customer/form.html", {
        "type": type_,
        "type_info": TYPE_INFO[type_],
        "is_edit": False,
        "data": {
            "code": "",
            "name": (request.GET.get("name") or "").strip(),
            "addr1": (request.GET.get("address") or "").strip(),
            "mobile": (request.GET.get("mobile") or "").strip(),
            "grp": "DEP" if type_ == "D" else "",
        },
    })


def edit(request):
    if not _is_authorized(request):
        return redirect("/login")
    type_ = _normalize_type(request.GET.get("type", "C"))
    code = (request.GET.get("code") or "").strip()
    if not code:
        return redirect(f"/customer/add?type={type_}")
    data = _get_by_code(code)
    if not data:
        return redirect(f"/customer?type={type_}&list=1")
    return render(request, "customer/form.html", {
        "type": type_,
        "type_info": TYPE_INFO[type_],
        "is_edit": True,
        "data": data,
    })


def delete_page(request):
    """GET /customer/delete?code=X  — call delete then redirect to list."""
    if not _is_authorized(request):
        return redirect("/login")
    type_ = _normalize_type(request.GET.get("type", "C"))
    code = (request.GET.get("code") or "").strip()
    if code:
        _delete_by_code(code)
    return redirect(f"/customer?type={type_}&list=1")


def next_code(request):
    if not _is_authorized(request):
        return JsonResponse({"success": False, "message": "Unauthorized"}, status=401)
    type_ = _normalize_type(request.GET.get("type", "C"))
    try:
        code = _next_auto_code(type_)
        return JsonResponse({"success": True, "code": code})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


def get(request):
    if not _is_authorized(request):
        return JsonResponse({"success": False, "message": "Unauthorized"}, status=401)
    code = (request.GET.get("code") or "").strip()
    if not code:
        return JsonResponse({"success": False, "message": "Code is required"}, status=400)
    row = _get_by_code(code)
    if not row:
        return JsonResponse({"success": False, "message": "Record not found"}, status=404)
    return JsonResponse({"success": True, "data": row})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def check_phone(request):
    if not _is_authorized(request):
        return JsonResponse({"success": False, "message": "Unauthorized"}, status=401)
    payload = _read_payload(request)
    phone = (payload.get("phone") or "").strip()
    code = (payload.get("code") or "").strip()
    if not phone or not _table_exists("clients"):
        return JsonResponse({"exists": False})

    norm = _normalize_phone(phone)
    sql = (
        "SELECT code, name, addr1 FROM clients WHERE ("
        "TRIM(COALESCE(telephone,'')) = %s OR TRIM(COALESCE(mobile,'')) = %s"
    )
    params = [phone, phone]
    if norm:
        sql += (
            " OR REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(TRIM(COALESCE(telephone,'')),' ',''),'-',''),'(',''),')',''),'+','') = %s"
            " OR REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(TRIM(COALESCE(mobile,'')),' ',''),'-',''),'(',''),')',''),'+','') = %s"
        )
        params += [norm, norm]
    sql += ")"
    if code:
        sql += " AND TRIM(COALESCE(code,'')) <> %s"
        params.append(code)
    sql += " LIMIT 1"

    try:
        with connection.cursor() as cur:
            cur.execute(sql, params)
            rows = _row_dict(cur)
    except Exception:
        return JsonResponse({"exists": False})

    if not rows:
        return JsonResponse({"exists": False})
    r = rows[0]
    details = ", ".join(filter(None, [r.get("code"), r.get("name"), r.get("addr1")]))
    return JsonResponse({"exists": True, "details": details})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def check_id_no(request):
    if not _is_authorized(request):
        return JsonResponse({"success": False, "message": "Unauthorized"}, status=401)
    payload = _read_payload(request)
    idno = (payload.get("idno") or "").strip()
    code = (payload.get("code") or "").strip()
    if not idno or not _table_exists("clients"):
        return JsonResponse({"exists": False})

    sql = "SELECT name FROM clients WHERE TRIM(COALESCE(idno,'')) = %s"
    params = [idno]
    if code:
        sql += " AND TRIM(COALESCE(code,'')) <> %s"
        params.append(code)
    sql += " LIMIT 1"

    try:
        with connection.cursor() as cur:
            cur.execute(sql, params)
            rows = _row_dict(cur)
    except Exception:
        return JsonResponse({"exists": False})
    if not rows:
        return JsonResponse({"exists": False})
    return JsonResponse({"exists": True, "name": rows[0].get("name") or ""})


@csrf_exempt
@require_http_methods(["POST"])
def save(request):
    if not _is_authorized(request):
        return JsonResponse({"success": False, "message": "Unauthorized"}, status=401)
    if not _table_exists("clients"):
        return JsonResponse({"success": False, "message": "clients table not found"}, status=500)

    payload = _read_payload(request)
    code = (payload.get("code") or "").strip().upper()
    original_code = (payload.get("original_code") or code).strip().upper()
    type_ = _normalize_type(payload.get("type") or payload.get("ctype") or "C")
    name = (payload.get("name") or "").strip()
    if not name:
        return JsonResponse({"success": False, "message": "Name is required"}, status=400)

    is_depositor = type_ == "D"
    if is_depositor:
        type_ = "C"
        payload["grp"] = "DEP"

    if not code:
        code = _next_auto_code("D" if is_depositor else type_)
        if not original_code:
            original_code = code

    is_rename = original_code and original_code != code
    with connection.cursor() as cur:
        if is_rename:
            cur.execute("SELECT 1 FROM clients WHERE code = %s", [original_code])
            if not cur.fetchone():
                return JsonResponse({"success": False, "message": "Original code not found"}, status=404)
            cur.execute("SELECT 1 FROM clients WHERE code = %s", [code])
            if cur.fetchone():
                return JsonResponse({"success": False, "message": "New code already exists"}, status=400)
            if _has_linked_transactions(original_code):
                return JsonResponse({"success": False, "message": "Linked transactions exist; rename blocked."}, status=400)

        cur.execute("SELECT 1 FROM clients WHERE code = %s", [code])
        exists = cur.fetchone() is not None

    row = _build_client_row(payload, code, type_)

    try:
        with transaction.atomic():
            if is_rename:
                _rename_code(original_code, code)
                exists = True
            with connection.cursor() as cur:
                if exists:
                    cols = list(row.keys())
                    set_clause = ", ".join(f"`{c}` = %s" for c in cols)
                    cur.execute(
                        f"UPDATE clients SET {set_clause} WHERE code = %s",
                        list(row.values()) + [code],
                    )
                else:
                    cols = list(row.keys())
                    placeholders = ", ".join(["%s"] * len(cols))
                    cur.execute(
                        f"INSERT INTO clients ({', '.join(f'`{c}`' for c in cols)}) VALUES ({placeholders})",
                        list(row.values()),
                    )
                _upsert_accountm(row, payload)
    except Exception as e:
        return JsonResponse({"success": False, "message": f"Error: {e}"}, status=400)

    label = TYPE_INFO["D" if is_depositor else type_]["title"]
    action = "Renamed" if is_rename else ("updated" if exists else "added")
    msg = (
        f"{label} code changed from {original_code} to {code} successfully"
        if is_rename else f"{label} {action} successfully"
    )
    return JsonResponse({"success": True, "message": msg, "data": _get_by_code(code)})


@csrf_exempt
@require_http_methods(["POST"])
def delete(request):
    if not _is_authorized(request):
        return JsonResponse({"success": False, "message": "Unauthorized"}, status=401)
    payload = _read_payload(request)
    code = (payload.get("code") or "").strip()
    if not code:
        return JsonResponse({"success": False, "message": "Code is required"}, status=400)
    return _delete_by_code(code)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _query_by_type(type_: str, search: str, no_removed: bool) -> list:
    if not _table_exists("clients"):
        return []
    cols = _columns("clients")

    where = []
    params: list = []
    if type_ == "D":
        where.append("ctype = %s")
        params.append("C")
        sub = ["LEFT(COALESCE(grp,''),3) = 'DEP'"]
        if "dcount" in cols:
            sub.append("dcount > 0")
        where.append("(" + " OR ".join(sub) + ")")
    else:
        where.append("ctype = %s")
        params.append(type_)

    if no_removed and "removed" in cols:
        where.append("(removed <> 1 OR removed IS NULL)")

    if search:
        s = f"%{search}%"
        where.append("(code LIKE %s OR name LIKE %s OR mobile LIKE %s OR telephone LIKE %s OR city LIKE %s OR addr1 LIKE %s)")
        params += [s, s, s, s, s, s]

    sql = (
        "SELECT code, name, mobile, telephone, city, addr1, ctype, grp, removed "
        "FROM clients WHERE " + " AND ".join(where) +
        " ORDER BY name LIMIT 300"
    )
    try:
        with connection.cursor() as cur:
            cur.execute(sql, params)
            return _row_dict(cur)
    except Exception:
        return []


def _get_by_code(code: str) -> Optional[dict]:
    if not _table_exists("clients"):
        return None
    code = (code or "").strip()
    try:
        with connection.cursor() as cur:
            cur.execute(
                "SELECT * FROM clients WHERE TRIM(COALESCE(code,'')) = %s LIMIT 1",
                [code],
            )
            rows = _row_dict(cur)
    except Exception:
        return None
    if not rows:
        return None
    data = {k: (v.strip() if isinstance(v, str) else v) for k, v in rows[0].items()}
    if _table_exists("accountm"):
        try:
            with connection.cursor() as cur:
                cur.execute(
                    "SELECT grcode, bshead, blocked FROM accountm WHERE TRIM(COALESCE(accode,'')) = %s LIMIT 1",
                    [code],
                )
                ac = _row_dict(cur)
                if ac:
                    data["acgrp"] = ac[0].get("grcode")
                    data["bshead"] = ac[0].get("bshead")
                    data["ac_blocked"] = ac[0].get("blocked")
        except Exception:
            pass
    return data


def _next_auto_code(type_: str) -> str:
    is_depositor = type_ == "D"
    base_type = "C" if is_depositor else type_

    counter_code = "CLASTNO" if base_type == "C" else "SLASTNO"
    last_no = 0
    if _table_exists("generali"):
        try:
            with connection.cursor() as cur:
                cur.execute("SELECT cvalue FROM generali WHERE code = %s LIMIT 1", [counter_code])
                row = cur.fetchone()
                if row and row[0] is not None:
                    last_no = int(float(row[0]))
        except Exception:
            pass

    prefix = "C" if is_depositor else base_type
    derived = _max_party_code_number(prefix)
    if derived > last_no:
        last_no = derived
    return f"{prefix}{last_no + 1:04d}"


def _max_party_code_number(prefix: str) -> int:
    if not _table_exists("clients"):
        return 0
    pat = f"{prefix}%"
    try:
        with connection.cursor() as cur:
            cur.execute(
                "SELECT MAX(CAST(SUBSTRING(code, %s) AS UNSIGNED)) "
                "FROM clients WHERE code LIKE %s",
                [len(prefix) + 1, pat],
            )
            row = cur.fetchone()
            return int(row[0] or 0)
    except Exception:
        return 0


def _build_client_row(data: dict, code: str, type_: str) -> dict:
    customer_like = type_ in ("C", "D")
    op_balance = float(data.get("opbalance") or 0)
    op_type = (data.get("balance_type") or "debit").lower()
    if customer_like:
        op_balance = abs(op_balance) if op_type == "debit" else -abs(op_balance)
    else:
        op_balance = abs(op_balance) if op_type == "credit" else -abs(op_balance)

    weight = float(data.get("opweight") or 0)
    weight = abs(weight) if (data.get("weight_type") or "debit").lower() == "credit" else -abs(weight)

    candidate = {
        "code": code,
        "name": (data.get("name") or "").strip()[:40],
        "addr1": (data.get("addr1") or "").strip(),
        "addr2": (data.get("addr2") or "").strip(),
        "addr3": (data.get("addr3") or "").strip(),
        "city": (data.get("city") or "").strip(),
        "telephone": (data.get("telephone") or "").strip(),
        "mobile": (data.get("mobile") or "").strip(),
        "email": (data.get("email") or "").strip(),
        "pin": (data.get("pin") or "").strip(),
        "state": (data.get("state") or "").strip(),
        "panadhar": (data.get("panadhar") or "").strip(),
        "tin": (data.get("tin") or "").strip(),
        "opbalance": op_balance,
        "ctype": type_,
        "control": 1,
        "removed": 1 if data.get("removed") else 0,
        "blocked": "Y" if data.get("blocked") else "N",
        "grp": (data.get("grp") or "O").strip(),
        "route": (data.get("route") or "").strip(),
        "carea": (data.get("carea") or data.get("area") or "").strip(),
        "opweight": weight,
        "idno": (data.get("idno") or "").strip(),
        "religion": (data.get("religion") or "").strip(),
        "note": (data.get("note") or "").strip(),
        "pcard": (data.get("pcard") or "").strip(),
        "smcode": (data.get("smcode") or "").strip(),
    }
    actual_cols = _columns("clients")
    return {k: v for k, v in candidate.items() if k.lower() in actual_cols}


def _upsert_accountm(client_row: dict, payload: dict) -> None:
    if not _table_exists("accountm"):
        return
    code = client_row["code"]
    grcode = (payload.get("acgrp") or "").strip()
    name = client_row.get("name", "")
    cols = _columns("accountm")
    with connection.cursor() as cur:
        cur.execute("SELECT 1 FROM accountm WHERE accode = %s", [code])
        exists = cur.fetchone() is not None
        row = {"accode": code, "acname": name}
        if "grcode" in cols and grcode:
            row["grcode"] = grcode
        if exists:
            set_clause = ", ".join(f"`{c}` = %s" for c in row)
            cur.execute(
                f"UPDATE accountm SET {set_clause} WHERE accode = %s",
                list(row.values()) + [code],
            )
        else:
            placeholders = ", ".join(["%s"] * len(row))
            cur.execute(
                f"INSERT INTO accountm ({', '.join(f'`{c}`' for c in row)}) VALUES ({placeholders})",
                list(row.values()),
            )


def _has_linked_transactions(code: str) -> bool:
    for table in ("daybook", "salesm", "purchasem", "orderm"):
        if not _table_exists(table):
            continue
        col = "accode" if table == "daybook" else "custcode"
        cols = _columns(table)
        if col not in cols:
            continue
        try:
            with connection.cursor() as cur:
                cur.execute(f"SELECT 1 FROM `{table}` WHERE `{col}` = %s LIMIT 1", [code])
                if cur.fetchone():
                    return True
        except Exception:
            pass
    return False


def _rename_code(old: str, new: str) -> None:
    with connection.cursor() as cur:
        cur.execute("UPDATE clients SET code = %s WHERE code = %s", [new, old])
        for table, col in [
            ("accountm", "accode"),
            ("clientsgs", "code"),
            ("clientspict", "code"),
            ("clients_advanced", "code"),
        ]:
            if _table_exists(table):
                try:
                    cur.execute(f"UPDATE `{table}` SET `{col}` = %s WHERE `{col}` = %s", [new, old])
                except Exception:
                    pass


def _delete_by_code(code: str) -> JsonResponse:
    if _table_exists("daybook"):
        with connection.cursor() as cur:
            cur.execute("SELECT 1 FROM daybook WHERE accode = %s LIMIT 1", [code])
            if cur.fetchone():
                return JsonResponse({"success": False, "message": "Transactions exist. Cannot delete this code."}, status=400)
    try:
        with transaction.atomic(), connection.cursor() as cur:
            cur.execute("DELETE FROM clients WHERE code = %s", [code])
            for table, col in [
                ("accountm", "accode"),
                ("clientsgs", "code"),
                ("clientspict", "code"),
                ("clients_advanced", "code"),
            ]:
                if _table_exists(table):
                    cur.execute(f"DELETE FROM `{table}` WHERE `{col}` = %s", [code])
    except Exception as e:
        return JsonResponse({"success": False, "message": f"Error: {e}"}, status=400)
    return JsonResponse({"success": True, "message": "Customer deleted successfully"})
