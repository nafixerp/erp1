"""
Stock — port of StockController.

Implemented:
  - index           opening stock entry page (per-item current qty/weight)
  - update          save opening or closing stock (typed via itemsstk OR
                    direct on items)
  - stock_list      list page shell
  - stock_list_data JSON for the list page (current stock, filters)

Skipped (still stubbed): ledger, ledger export, group filter rendering of
fancy multi-table joins. The legacy `aggregateTypedStockToItems` is
ported so that typed writes still propagate into items.qty/weight.

Also exports `apply_sales_bill_deduction(bill, items)` — used by sales
bill save() to deduct sold qty/weight from the buyer's stock type.
"""
from __future__ import annotations

import json
from typing import Iterable, Optional

from django.db import connection, transaction
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _is_authorized(request) -> bool:
    return bool((request.session.get("user_code") or "").strip())


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


def _row_dicts(cur):
    cols = [c[0] for c in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]


def _to_num(v) -> float:
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def _read_payload(request) -> dict:
    if request.content_type and "application/json" in request.content_type:
        try:
            return json.loads(request.body or "{}") or {}
        except json.JSONDecodeError:
            return {}
    if request.method == "GET":
        return request.GET.dict()
    return request.POST.dict()


# ---------------------------------------------------------------------------
# Filter / option helpers
# ---------------------------------------------------------------------------

def _filters(request) -> dict:
    return {
        "stktype": (request.GET.get("stktype") or "").strip().upper(),
        "level": int(request.GET.get("level") or 1),
        "stock_view": (request.GET.get("stock_view") or "opening").lower(),
        "search": (request.GET.get("search") or "").strip(),
        "grpcode": (request.GET.get("grpcode") or "").strip().upper(),
        "itype": (request.GET.get("itype") or "All"),
    }


def _stock_type_options() -> list:
    if not _table_exists("stktype"):
        return []
    try:
        with connection.cursor() as cur:
            cur.execute("SELECT code, name FROM stktype ORDER BY code")
            return _row_dicts(cur)
    except Exception:
        return []


def _group_code_options(items_columns: set) -> list:
    if "grpcode" not in items_columns or not _table_exists("items"):
        return []
    try:
        with connection.cursor() as cur:
            cur.execute(
                "SELECT DISTINCT grpcode FROM items "
                "WHERE grpcode IS NOT NULL AND grpcode <> '' ORDER BY grpcode"
            )
            return [{"code": r[0]} for r in cur.fetchall()]
    except Exception:
        return []


def _column_keys(level: int, is_opening: bool) -> dict:
    """Return the {qty,weight,stonewgt,stoneamt,dmdwgt} column names for level/view."""
    qty = ("opqty" if is_opening else "qty") + ("" if level == 1 else "b")
    wgt = ("opweight" if is_opening else "weight") + ("" if level == 1 else "b")
    stw = ("opstonewgt" if is_opening else "stonewgt") + ("" if level == 1 else "b")
    sta = ("opstoneamt" if is_opening else "stoneamt") + ("" if level == 1 else "b") if is_opening else ""
    dmd = "opdmdwgt" if is_opening else ""
    return {"qty": qty, "weight": wgt, "stonewgt": stw, "stoneamt": sta, "dmdwgt": dmd}


def _current_values(code: str, filters: dict, items_columns: set) -> dict:
    """Sum on hand qty/weight for `code`, honoring stktype filter when present."""
    keys = _column_keys(filters["level"], filters["stock_view"] == "opening")
    base = {"qty": 0.0, "weight": 0.0, "stonewgt": 0.0, "stoneamt": 0.0, "dmdwgt": 0.0}

    def _sum(table: str, col: str, where: list, params: list, columns: set) -> float:
        if not col or col not in columns:
            return 0.0
        sql = f"SELECT COALESCE(SUM(`{col}`),0) FROM `{table}` WHERE " + " AND ".join(where)
        try:
            with connection.cursor() as cur:
                cur.execute(sql, params)
                row = cur.fetchone()
                return float(row[0] or 0)
        except Exception:
            return 0.0

    if filters["stktype"] and _table_exists("itemsstk"):
        cols = _columns("itemsstk")
        where = ["code = %s", "stktype = %s"]
        params = [code, filters["stktype"]]
        for k, c in keys.items():
            base[k] = _sum("itemsstk", c, where, params, cols)
        return base

    # No stktype filter — read items.* and fall back to itemsstk sums when items is empty.
    if _table_exists("items"):
        try:
            with connection.cursor() as cur:
                cur.execute("SELECT * FROM items WHERE code = %s LIMIT 1", [code])
                rows = _row_dicts(cur)
                row = rows[0] if rows else {}
            for k, c in keys.items():
                if c and c.lower() in items_columns:
                    base[k] = _to_num(row.get(c))
        except Exception:
            pass

    if all(abs(v) < 0.0001 for v in base.values()) and _table_exists("itemsstk"):
        cols = _columns("itemsstk")
        for k, c in keys.items():
            base[k] = _sum("itemsstk", c, ["code = %s"], [code], cols)
    return base


def _passes_stock_filter(qty: float, weight: float, stock_filter: str, no_weight: bool) -> bool:
    measure = qty if no_weight else weight
    return {
        "With Stock Only": measure > 0,
        "With -ve Stock": measure < 0,
        "With Zero Stock": abs(measure) < 0.0001,
        "With Not Zero Stock": abs(measure) >= 0.0001,
    }.get(stock_filter, True)


def _blank_totals() -> dict:
    return {k: 0.0 for k in (
        "opqty", "opweight", "qty", "weight", "stonewgt", "netwgt", "value",
        "gold_qty", "gold_weight", "silver_qty", "silver_weight",
        "other_qty", "other_weight",
    )}


# ---------------------------------------------------------------------------
# Public views
# ---------------------------------------------------------------------------

def index(request):
    if not _is_authorized(request):
        return redirect("/login")

    if not _table_exists("items"):
        return render(request, "stock/opening-stock.html", {
            "items": [], "filters": _filters(request),
            "message": "Items table not found.",
            "stock_types": [], "group_codes": [],
        })

    filters = _filters(request)
    items_cols = _columns("items")

    where, params = [], []
    if "disabled" in items_cols:
        where.append("(disabled <> 1 OR disabled IS NULL)")
    if filters["grpcode"] and "grpcode" in items_cols:
        where.append("grpcode = %s")
        params.append(filters["grpcode"])
    if filters["search"]:
        where.append("(code LIKE %s OR name LIKE %s)")
        params += [f"%{filters['search']}%"] * 2
    if filters["itype"] != "All" and "itype" in items_cols:
        where.append("itype = %s")
        params.append(filters["itype"][:1])

    sql = "SELECT code, name, " + (
        "touch" if "touch" in items_cols else "0 AS touch"
    ) + " FROM items"
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY name, code LIMIT 500"

    try:
        with connection.cursor() as cur:
            cur.execute(sql, params)
            rows = _row_dicts(cur)
    except Exception:
        rows = []

    items = []
    for r in rows:
        cur_vals = _current_values(r["code"], filters, items_cols)
        items.append({
            "code": r["code"],
            "name": r["name"],
            "touch": _to_num(r.get("touch")),
            "cqty": cur_vals["qty"],
            "cweight": cur_vals["weight"],
            "cstwgt": cur_vals["stonewgt"],
            "cstoneamt": cur_vals["stoneamt"],
            "cdmdwgt": cur_vals["dmdwgt"],
        })

    return render(request, "stock/opening-stock.html", {
        "items": items,
        "filters": filters,
        "message": "",
        "stock_types": _stock_type_options(),
        "group_codes": _group_code_options(items_cols),
    })


@csrf_exempt
@require_http_methods(["POST"])
def update(request):
    if not _is_authorized(request):
        return JsonResponse({"success": False, "message": "Unauthorized"}, status=401)

    payload = _read_payload(request)
    items = payload.get("items") or []
    if not isinstance(items, list) or not items:
        return JsonResponse({"success": False, "message": "items required"}, status=422)
    if not _table_exists("items"):
        return JsonResponse({"success": False, "message": "Items table not found"}, status=500)

    stktype = (payload.get("stktype") or "").strip().upper()
    level = int(payload.get("level") or 1)
    is_opening = (payload.get("stock_view") or "opening").lower() == "opening"
    update_closing_also = bool(payload.get("update_closing_also"))
    same_stock = bool(payload.get("same_stock"))
    items_cols = _columns("items")
    stock_cols = _columns("itemsstk") if _table_exists("itemsstk") else set()

    try:
        with transaction.atomic():
            for row in items:
                code = (row.get("code") or "").strip().upper()
                if not code:
                    continue
                values = {
                    k: _to_num(row.get(k))
                    for k in ("qty", "weight", "stonewgt", "stoneamt", "dmdwgt")
                }
                if stktype and _table_exists("itemsstk"):
                    _save_typed(code, stktype, level, is_opening, values,
                                update_closing_also, same_stock, stock_cols)
                    _aggregate_typed_to_items(code, items_cols, stock_cols)
                else:
                    _save_direct(code, level, is_opening, values,
                                 update_closing_also, same_stock, items_cols)
    except Exception as e:
        return JsonResponse({"success": False, "message": f"Error updating stock: {e}"}, status=500)

    return JsonResponse({"success": True, "message": "Stock updated successfully."})


def stock_list(request):
    if not _is_authorized(request):
        return redirect("/login")
    items_cols = _columns("items") if _table_exists("items") else set()
    return render(request, "stock/list.html", {
        "title": request.GET.get("title") or "Stock List",
        "stock_types": _stock_type_options(),
        "group_codes": _group_code_options(items_cols),
    })


def stock_list_data(request):
    if not _is_authorized(request):
        return JsonResponse({"ok": False, "message": "Unauthorized"}, status=401)
    if not _table_exists("items"):
        return JsonResponse({
            "ok": True, "rows": [], "totals": _blank_totals(),
            "groups": [], "stock_types": [],
        })

    items_cols = _columns("items")
    grp_code = (request.GET.get("grpcode") or "").strip().upper()
    filter_by_group = (request.GET.get("filter_group", "1") not in ("0", "false", "False"))
    metal_type = request.GET.get("metal_type") or "All"
    ornament_filter = request.GET.get("ornament_filter") or "All"
    stock_filter = request.GET.get("stock_filter") or "With Not Zero Stock"
    sort_on_code = request.GET.get("sort_on_code") in ("1", "true", "True")
    no_weight = request.GET.get("no_weight") in ("1", "true", "True")
    value_mode = (request.GET.get("value_mode") or "rate").lower()
    stktype = (request.GET.get("stktype") or "").strip().upper()

    select_cols = ["code", "name"]
    for c in ("itype", "grpcode", "subgrpcode", "ornament", "orn",
              "srate", "prate", "crate", "cost", "pos", "disabled", "showinstkrep"):
        if c in items_cols:
            select_cols.append(c)
    where = []
    params: list = []
    if "disabled" in items_cols:
        where.append("(disabled <> 1 OR disabled IS NULL)")
    if "showinstkrep" in items_cols:
        where.append("(showinstkrep <> 'N' OR showinstkrep IS NULL)")
    if metal_type != "All" and "itype" in items_cols:
        where.append("itype = %s")
        params.append(metal_type[:1])
    ornament_col = "ornament" if "ornament" in items_cols else ("orn" if "orn" in items_cols else None)
    if ornament_col:
        if ornament_filter == "Ornaments Only":
            where.append(f"{ornament_col} = 'Y'")
        elif ornament_filter == "Not Ornaments":
            where.append(f"({ornament_col} <> 'Y' OR {ornament_col} IS NULL)")
    if filter_by_group and grp_code and "grpcode" in items_cols:
        where.append("grpcode = %s")
        params.append(grp_code)

    sql = f"SELECT {', '.join(select_cols)} FROM items"
    if where:
        sql += " WHERE " + " AND ".join(where)
    if sort_on_code:
        sql += " ORDER BY code, name"
    elif "pos" in items_cols:
        sql += " ORDER BY pos, name, code"
    else:
        sql += " ORDER BY name, code"

    try:
        with connection.cursor() as cur:
            cur.execute(sql, params)
            base_rows = _row_dicts(cur)
    except Exception:
        base_rows = []

    base_filters = {"stktype": stktype, "stock_view": "closing", "level": 1,
                    "search": "", "grpcode": grp_code, "itype": "All"}
    opening_filters = {**base_filters, "stock_view": "opening"}

    rows = []
    for r in base_rows:
        code = r.get("code") or ""
        cur_vals = _current_values(code, base_filters, items_cols)
        op_vals = _current_values(code, opening_filters, items_cols)
        weight = cur_vals["weight"]
        qty = cur_vals["qty"]
        stonewgt = cur_vals["stonewgt"]
        netwgt = weight - stonewgt
        if not _passes_stock_filter(qty, weight, stock_filter, no_weight):
            continue
        if value_mode == "cost":
            rate = _to_num(r.get("cost") or r.get("crate"))
        else:
            rate = _to_num(r.get("crate") or r.get("cost"))
        if rate == 0.0:
            rate = _to_num(r.get("srate"))
        value_base = qty if no_weight else netwgt
        rows.append({
            "code": code, "name": r.get("name") or "",
            "grpcode": r.get("grpcode") or "",
            "subgrpcode": r.get("subgrpcode") or "",
            "itype": r.get("itype") or "",
            "ornament": (r.get(ornament_col) or "") if ornament_col else "",
            "opqty": op_vals["qty"], "opweight": op_vals["weight"],
            "qty": qty, "weight": weight, "stonewgt": stonewgt, "netwgt": netwgt,
            "srate": _to_num(r.get("srate")), "prate": _to_num(r.get("prate")),
            "crate": _to_num(r.get("crate") or r.get("cost")),
            "rate": rate, "value": round(value_base * rate, 2),
        })

    totals = _blank_totals()
    for row in rows:
        for k in ("opqty", "opweight", "qty", "weight", "stonewgt", "netwgt", "value"):
            totals[k] += row[k]
        if row["itype"] == "G":
            totals["gold_qty"] += row["qty"]
            totals["gold_weight"] += row["weight"]
        elif row["itype"] == "S":
            totals["silver_qty"] += row["qty"]
            totals["silver_weight"] += row["weight"]
        else:
            totals["other_qty"] += row["qty"]
            totals["other_weight"] += row["weight"]

    return JsonResponse({
        "ok": True, "rows": rows, "totals": totals,
        "groups": _group_code_options(items_cols),
        "stock_types": _stock_type_options(),
    })


# ---------------------------------------------------------------------------
# Save helpers (typed itemsstk + direct items)
# ---------------------------------------------------------------------------

def _set_if_col(d: dict, available: set, col: str, value: float) -> None:
    if col and col.lower() in available:
        d[col] = value


def _save_typed(code: str, stktype: str, level: int, is_opening: bool,
                v: dict, update_closing_also: bool, same_stock: bool,
                stock_cols: set) -> None:
    update: dict = {}
    keys = _column_keys(level, is_opening)
    _set_if_col(update, stock_cols, keys["qty"], v["qty"])
    _set_if_col(update, stock_cols, keys["weight"], v["weight"])
    _set_if_col(update, stock_cols, keys["stonewgt"], v["stonewgt"])
    if keys["stoneamt"]:
        _set_if_col(update, stock_cols, keys["stoneamt"], v["stoneamt"])
    if keys["dmdwgt"]:
        _set_if_col(update, stock_cols, keys["dmdwgt"], v["dmdwgt"])

    if same_stock:
        mirror = _column_keys(2 if level == 1 else 1, is_opening)
        _set_if_col(update, stock_cols, mirror["qty"], v["qty"])
        _set_if_col(update, stock_cols, mirror["weight"], v["weight"])
        _set_if_col(update, stock_cols, mirror["stonewgt"], v["stonewgt"])

    if is_opening and update_closing_also:
        closing = _column_keys(level, False)
        _set_if_col(update, stock_cols, closing["qty"], v["qty"])
        _set_if_col(update, stock_cols, closing["weight"], v["weight"])
        _set_if_col(update, stock_cols, closing["stonewgt"], v["stonewgt"])

    if not update:
        return

    with connection.cursor() as cur:
        cur.execute("SELECT 1 FROM itemsstk WHERE code = %s AND stktype = %s LIMIT 1",
                    [code, stktype])
        exists = cur.fetchone() is not None
        if exists:
            sets = ", ".join(f"`{c}` = %s" for c in update)
            cur.execute(
                f"UPDATE itemsstk SET {sets} WHERE code = %s AND stktype = %s",
                list(update.values()) + [code, stktype],
            )
        else:
            cols = list(update.keys()) + ["code", "stktype"]
            placeholders = ", ".join(["%s"] * len(cols))
            cur.execute(
                f"INSERT INTO itemsstk ({', '.join(f'`{c}`' for c in cols)}) "
                f"VALUES ({placeholders})",
                list(update.values()) + [code, stktype],
            )


def _aggregate_typed_to_items(code: str, items_cols: set, stock_cols: set) -> None:
    update: dict = {}
    for col in ("qty", "qtyb", "weight", "weightb", "stonewgt", "stonewgtb",
                "opqty", "opqtyb", "opweight", "opweightb",
                "opstonewgt", "opstonewgtb", "opstoneamt", "opstoneamtb", "opdmdwgt"):
        if col not in items_cols or col not in stock_cols:
            continue
        try:
            with connection.cursor() as cur:
                cur.execute(f"SELECT COALESCE(SUM(`{col}`),0) FROM itemsstk WHERE code = %s", [code])
                row = cur.fetchone()
                update[col] = float(row[0] or 0)
        except Exception:
            pass
    if not update:
        return
    sets = ", ".join(f"`{c}` = %s" for c in update)
    with connection.cursor() as cur:
        cur.execute(f"UPDATE items SET {sets} WHERE code = %s",
                    list(update.values()) + [code])


def _save_direct(code: str, level: int, is_opening: bool, v: dict,
                 update_closing_also: bool, same_stock: bool, items_cols: set) -> None:
    update: dict = {}
    keys = _column_keys(level, is_opening)
    _set_if_col(update, items_cols, keys["qty"], v["qty"])
    _set_if_col(update, items_cols, keys["weight"], v["weight"])
    _set_if_col(update, items_cols, keys["stonewgt"], v["stonewgt"])
    if keys["stoneamt"]:
        _set_if_col(update, items_cols, keys["stoneamt"], v["stoneamt"])
    if keys["dmdwgt"]:
        _set_if_col(update, items_cols, keys["dmdwgt"], v["dmdwgt"])

    if same_stock:
        mirror = _column_keys(2 if level == 1 else 1, is_opening)
        _set_if_col(update, items_cols, mirror["qty"], v["qty"])
        _set_if_col(update, items_cols, mirror["weight"], v["weight"])
        _set_if_col(update, items_cols, mirror["stonewgt"], v["stonewgt"])

    if is_opening and update_closing_also:
        closing = _column_keys(level, False)
        _set_if_col(update, items_cols, closing["qty"], v["qty"])
        _set_if_col(update, items_cols, closing["weight"], v["weight"])
        _set_if_col(update, items_cols, closing["stonewgt"], v["stonewgt"])

    if not update:
        return
    sets = ", ".join(f"`{c}` = %s" for c in update)
    with connection.cursor() as cur:
        cur.execute(f"UPDATE items SET {sets} WHERE code = %s",
                    list(update.values()) + [code])


# ---------------------------------------------------------------------------
# Cross-module helper for sales bill -> deduct inventory
# ---------------------------------------------------------------------------

def apply_sales_return_recovery(items: Iterable[dict], default_stktype: Optional[str] = None) -> dict:
    """Inverse of apply_sales_bill_deduction — adds stock back."""
    inverted = []
    for line in items:
        line = dict(line)
        line["qty"] = -_to_num(line.get("qty"))
        line["weight"] = -_to_num(line.get("weight"))
        line["stone_wgt"] = -_to_num(line.get("stone_wgt"))
        inverted.append(line)
    summary = apply_sales_bill_deduction(inverted, default_stktype)
    summary["recovered"] = summary.pop("adjusted", 0)
    return summary


def apply_sales_bill_deduction(items: Iterable[dict], default_stktype: Optional[str] = None) -> dict:
    """
    Subtract sold qty/weight/stonewgt from the buyer's stock type.

    `items` is a list of dicts with keys: item_code, qty, weight, stone_wgt,
    optionally stktype (overrides default_stktype). Returns a summary dict
    {"adjusted": int, "skipped": list[str]}.
    """
    summary = {"adjusted": 0, "skipped": []}
    if not _table_exists("itemsstk"):
        summary["skipped"].append("itemsstk table missing")
        return summary
    if not default_stktype:
        # Pick configured default from stktype.def=1 if present.
        if _table_exists("stktype"):
            try:
                with connection.cursor() as cur:
                    cur.execute("SELECT code FROM stktype WHERE def = 1 LIMIT 1")
                    row = cur.fetchone()
                    if row:
                        default_stktype = row[0]
            except Exception:
                pass
    if not default_stktype:
        summary["skipped"].append("no default stktype")
        return summary

    cols = _columns("itemsstk")
    items_cols = _columns("items")

    with transaction.atomic():
        for line in items:
            code = (line.get("item_code") or "").strip().upper()
            if not code:
                continue
            stktype = (line.get("stktype") or default_stktype or "").strip().upper()
            qty = _to_num(line.get("qty"))
            weight = _to_num(line.get("weight"))
            stonewgt = _to_num(line.get("stone_wgt"))
            if qty == 0 and weight == 0 and stonewgt == 0:
                continue

            update_clauses = []
            params: list = []
            for col, delta in (("qty", qty), ("weight", weight), ("stonewgt", stonewgt)):
                if col in cols and delta:
                    update_clauses.append(f"`{col}` = COALESCE(`{col}`,0) - %s")
                    params.append(delta)
            if not update_clauses:
                continue

            with connection.cursor() as cur:
                cur.execute(
                    "SELECT 1 FROM itemsstk WHERE code = %s AND stktype = %s LIMIT 1",
                    [code, stktype],
                )
                exists = cur.fetchone() is not None
                if exists:
                    cur.execute(
                        f"UPDATE itemsstk SET {', '.join(update_clauses)} "
                        f"WHERE code = %s AND stktype = %s",
                        params + [code, stktype],
                    )
                else:
                    insert_cols = ["code", "stktype"]
                    insert_vals = [code, stktype]
                    for col, delta in (("qty", qty), ("weight", weight), ("stonewgt", stonewgt)):
                        if col in cols and delta:
                            insert_cols.append(col)
                            insert_vals.append(-delta)
                    placeholders = ", ".join(["%s"] * len(insert_cols))
                    cur.execute(
                        f"INSERT INTO itemsstk ({', '.join(f'`{c}`' for c in insert_cols)}) "
                        f"VALUES ({placeholders})",
                        insert_vals,
                    )
            _aggregate_typed_to_items(code, items_cols, cols)
            summary["adjusted"] += 1

    return summary
