"""
Reports — read-only aggregations against legacy tables.

  - cashbook_index / cashbook_api
        Cash ledger (CASH account in `daybook` joined to `daybookpart`)
        with running-balance, debit/credit totals, optional incharge filter.

  - stock_summary_index / stock_summary_data
        Per-item stock summary: opening + purchases (purchasem/d) + sales
        (salesm/d) + current closing, with category totals.

These views are deliberately simpler than the legacy controllers (which
weave together salesrm/repairm/refinerym/smithm/orderm). Add the missing
sources incrementally as needed.
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from django.db import connection
from django.http import JsonResponse
from django.shortcuts import redirect, render

from .. import daybook_helpers as dh


def _is_authorized(request) -> bool:
    return bool((request.session.get("user_code") or "").strip())


# ---------------------------------------------------------------------------
# CashBook
# ---------------------------------------------------------------------------

def cashbook_index(request):
    if not _is_authorized(request):
        return redirect("/login")
    return render(request, "reports/cashbook.html", {})


def cashbook_api(request):
    if not _is_authorized(request):
        return JsonResponse({"success": False, "error": "Unauthorized"}, status=401)
    if not (dh.table_exists("daybook") and dh.table_exists("daybookpart")):
        return JsonResponse({"success": True, "rows": [], "totals": _blank_cb_totals()})

    gilevel = max(1, int(request.session.get("gilevel") or 1))
    dfrom = dh.parse_date(request.GET.get("date1")) or datetime.now().date().isoformat()
    dto = dh.parse_date(request.GET.get("date2")) or datetime.now().date().isoformat()
    incharge = (request.GET.get("ic") or "").strip().upper()

    opening = _opening_balance("CASH", dfrom, gilevel, incharge)
    rows = _cash_rows(dfrom, dto, gilevel, incharge)

    running = -opening   # legacy displays previous close = -ledger balance
    debit_total = credit_total = 0.0
    out = []
    for r in rows:
        amt = float(r["amount"] or 0)
        debit = abs(amt) if amt < 0 else 0.0
        credit = amt if amt > 0 else 0.0
        running = running + debit - credit
        debit_total += debit
        credit_total += credit
        out.append({
            "slno": r["slno"], "date": str(r["tdate"]),
            "vchno": (r.get("vchno") or "").strip(),
            "particular": (r.get("particular") or "").strip(),
            "othacname": (r.get("othacname") or "").strip(),
            "ic": (r.get("ic") or "").strip(),
            "debit": round(debit, 2), "credit": round(credit, 2),
            "running_balance": round(running, 2),
        })

    return JsonResponse({
        "success": True, "rows": out,
        "totals": {
            "opening": round(opening, 2),
            "display_opening": round(-opening, 2),
            "debit": round(debit_total, 2),
            "credit": round(credit_total, 2),
            "closing": round(running, 2),
            "display_closing": round(abs(running), 2),
        },
        "incharges": _incharge_options(),
    })


def _blank_cb_totals():
    return {"opening": 0.0, "display_opening": 0.0, "debit": 0.0,
            "credit": 0.0, "closing": 0.0, "display_closing": 0.0}


def _opening_balance(code: str, dfrom: str, gilevel: int, incharge: str) -> float:
    base = 0.0
    if dh.table_exists("accountm"):
        col = "opbal" if gilevel == 1 else "opbalb"
        try:
            with connection.cursor() as cur:
                cur.execute(
                    f"SELECT COALESCE(`{col}`, 0) FROM accountm "
                    f"WHERE TRIM(accode) = %s LIMIT 1",
                    [code],
                )
                row = cur.fetchone()
                if row:
                    base = float(row[0] or 0)
        except Exception:
            pass
    if not dh.table_exists("daybook"):
        return base
    where = ["TRIM(d.accode) = %s", "d.control <= %s", "d.tdate < %s"]
    params: list = [code, gilevel, dfrom]
    sql = (
        "SELECT COALESCE(SUM(d.amount), 0) FROM daybook d "
        "JOIN daybookpart dp ON dp.slno = d.slno "
        "WHERE " + " AND ".join(where)
    )
    if incharge and "ic" in dh.columns("daybookpart"):
        sql += " AND TRIM(COALESCE(dp.ic, '')) = %s"
        params.append(incharge)
    try:
        with connection.cursor() as cur:
            cur.execute(sql, params)
            return base + float(cur.fetchone()[0] or 0)
    except Exception:
        return base


def _cash_rows(dfrom: str, dto: str, gilevel: int, incharge: str) -> list:
    sql = (
        "SELECT d.slno, d.tdate, d.amount, "
        "       TRIM(COALESCE(dp.vchno,'')) AS vchno, "
        "       TRIM(COALESCE(dp.particular,'')) AS particular, "
        "       TRIM(COALESCE(oth.name,'')) AS othacname, "
        "       TRIM(COALESCE(dp.ic,'')) AS ic "
        "FROM daybook d "
        "JOIN daybookpart dp ON dp.slno = d.slno "
        "LEFT JOIN accountm oth ON TRIM(oth.accode) = TRIM(d.opaccode) "
        "WHERE TRIM(d.accode) = 'CASH' AND d.control <= %s "
        "AND d.tdate BETWEEN %s AND %s"
    )
    params: list = [gilevel, dfrom, dto]
    if incharge and "ic" in dh.columns("daybookpart"):
        sql += " AND TRIM(COALESCE(dp.ic, '')) = %s"
        params.append(incharge)
    sql += " ORDER BY d.tdate, d.slno"
    try:
        with connection.cursor() as cur:
            cur.execute(sql, params)
            return dh.row_dicts(cur)
    except Exception:
        return []


def _incharge_options() -> list:
    if not dh.table_exists("incharges"):
        # Fall back to distinct values from daybookpart.ic.
        if not (dh.table_exists("daybookpart") and "ic" in dh.columns("daybookpart")):
            return []
        try:
            with connection.cursor() as cur:
                cur.execute(
                    "SELECT DISTINCT TRIM(ic) AS ic FROM daybookpart "
                    "WHERE ic IS NOT NULL AND TRIM(ic) <> '' ORDER BY ic"
                )
                return [{"code": r[0], "name": r[0]} for r in cur.fetchall()]
        except Exception:
            return []
    try:
        with connection.cursor() as cur:
            cur.execute("SELECT code, name FROM incharges ORDER BY code")
            return dh.row_dicts(cur)
    except Exception:
        return []


# ---------------------------------------------------------------------------
# Stock Summary (rate-wise simplified)
# ---------------------------------------------------------------------------

def stock_summary_index(request):
    if not _is_authorized(request):
        return redirect("/login")
    return render(request, "reports/stock-summary.html", {})


def stock_summary_data(request):
    if not _is_authorized(request):
        return JsonResponse({"success": False, "error": "Unauthorized"}, status=401)
    if not dh.table_exists("items"):
        return JsonResponse({"success": True, "rows": [], "totals": _blank_ss_totals()})

    gilevel = max(1, int(request.session.get("gilevel") or 1))
    date_to = dh.parse_date(request.GET.get("date2")) or datetime.now().date().isoformat()
    metal_type = (request.GET.get("metal_type") or "All").strip()
    items_cols = dh.columns("items")

    select_cols = ["code", "name"]
    for c in ("itype", "grpcode", "ornament", "orn", "srate", "crate", "cost"):
        if c in items_cols:
            select_cols.append(c)
    where = []
    params: list = []
    if "disabled" in items_cols:
        where.append("(disabled <> 1 OR disabled IS NULL)")
    if metal_type != "All" and "itype" in items_cols:
        where.append("itype = %s"); params.append(metal_type[:1])
    sql = f"SELECT {', '.join(select_cols)} FROM items"
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY name"
    try:
        with connection.cursor() as cur:
            cur.execute(sql, params)
            rows = dh.row_dicts(cur)
    except Exception:
        rows = []

    out = []
    for r in rows:
        code = r.get("code") or ""
        opening = _stock_opening(code, items_cols)
        purch = _movement(code, "purchasem", "purchased", date_to, gilevel)
        sales = _movement(code, "salesm", "salesd", date_to, gilevel)
        sret = _movement(code, "salesrm", "salesrd", date_to, gilevel)
        closing_qty = opening["qty"] + purch["qty"] - sales["qty"] + sret["qty"]
        closing_wgt = opening["weight"] + purch["weight"] - sales["weight"] + sret["weight"]
        out.append({
            "code": code, "name": r.get("name") or "",
            "itype": r.get("itype") or "",
            "grpcode": r.get("grpcode") or "",
            "opening_qty": round(opening["qty"], 3),
            "opening_weight": round(opening["weight"], 3),
            "purch_qty": round(purch["qty"], 3),
            "purch_weight": round(purch["weight"], 3),
            "sales_qty": round(sales["qty"], 3),
            "sales_weight": round(sales["weight"], 3),
            "sret_qty": round(sret["qty"], 3),
            "sret_weight": round(sret["weight"], 3),
            "closing_qty": round(closing_qty, 3),
            "closing_weight": round(closing_wgt, 3),
        })

    totals = _blank_ss_totals()
    for row in out:
        for k in ("opening_qty", "opening_weight", "purch_qty", "purch_weight",
                  "sales_qty", "sales_weight", "sret_qty", "sret_weight",
                  "closing_qty", "closing_weight"):
            totals[k] += row[k]
        if row["itype"] == "G":
            totals["gold_weight"] += row["closing_weight"]
        elif row["itype"] == "S":
            totals["silver_weight"] += row["closing_weight"]
        else:
            totals["other_weight"] += row["closing_weight"]

    return JsonResponse({"success": True, "rows": out, "totals": totals})


def _blank_ss_totals():
    return {k: 0.0 for k in (
        "opening_qty", "opening_weight", "purch_qty", "purch_weight",
        "sales_qty", "sales_weight", "sret_qty", "sret_weight",
        "closing_qty", "closing_weight",
        "gold_weight", "silver_weight", "other_weight",
    )}


def _stock_opening(code: str, items_cols: set) -> dict:
    """Read items.opqty / opweight if present."""
    base = {"qty": 0.0, "weight": 0.0}
    qty_col = "opqty" if "opqty" in items_cols else None
    wgt_col = "opweight" if "opweight" in items_cols else None
    if not qty_col and not wgt_col:
        return base
    select = []
    if qty_col:
        select.append(qty_col)
    if wgt_col:
        select.append(wgt_col)
    try:
        with connection.cursor() as cur:
            cur.execute(
                f"SELECT {', '.join(f'COALESCE(`{c}`,0)' for c in select)} "
                f"FROM items WHERE code = %s LIMIT 1",
                [code],
            )
            row = cur.fetchone()
            if row:
                if qty_col:
                    base["qty"] = float(row[0] or 0)
                if wgt_col and len(row) > (1 if qty_col else 0):
                    base["weight"] = float(row[1 if qty_col else 0] or 0)
    except Exception:
        pass
    return base


def _movement(code: str, header_table: str, detail_table: str,
              date_to: str, gilevel: int) -> dict:
    base = {"qty": 0.0, "weight": 0.0}
    if not (dh.table_exists(header_table) and dh.table_exists(detail_table)):
        return base
    h_cols = dh.columns(header_table)
    d_cols = dh.columns(detail_table)
    if "code" not in d_cols:
        return base
    qty_col = "qty" if "qty" in d_cols else None
    wgt_col = "weight" if "weight" in d_cols else None
    if not qty_col and not wgt_col:
        return base
    select = ", ".join([
        f"COALESCE(SUM({d}.{qty_col}), 0)" if qty_col else "0",
        f"COALESCE(SUM({d}.{wgt_col}), 0)" if wgt_col else "0",
    ]).format(d=detail_table)
    sql = (
        f"SELECT {select} FROM `{detail_table}` d "
        f"JOIN `{header_table}` h ON h.slno = d.slno "
        f"WHERE TRIM(d.code) = %s"
    )
    params: list = [code]
    if "tdate" in h_cols:
        sql += " AND h.tdate <= %s"
        params.append(date_to)
    if "control" in h_cols:
        sql += " AND h.control <= %s"
        params.append(gilevel)
    if "status" in h_cols:
        sql += " AND h.status <> 0"
    try:
        with connection.cursor() as cur:
            cur.execute(sql, params)
            row = cur.fetchone()
            if row:
                base["qty"] = float(row[0] or 0)
                base["weight"] = float(row[1] or 0)
    except Exception:
        pass
    return base
