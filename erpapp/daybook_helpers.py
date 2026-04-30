"""
Shared helpers for cash/bank/journal voucher writes against the legacy
`daybook` + `daybookpart` tables.

Receipts, payments, and journal vouchers all share the same posting
shape: a `daybookpart` header row (slno, vchno, particular, dates,
control, ic) plus 2+ `daybook` lines whose amounts net to zero.

`control` is the gilevel from session (typically 1 = main, 2 = B-stock).
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from django.db import connection


# ---------------------------------------------------------------------------
# Schema discovery
# ---------------------------------------------------------------------------

def table_exists(name: str) -> bool:
    try:
        with connection.cursor() as cur:
            cur.execute("SHOW TABLES LIKE %s", [name])
            return cur.fetchone() is not None
    except Exception:
        return False


def columns(table: str) -> set:
    try:
        with connection.cursor() as cur:
            cur.execute(f"SHOW COLUMNS FROM `{table}`")
            return {r[0].lower() for r in cur.fetchall()}
    except Exception:
        return set()


def row_dicts(cur):
    cols = [c[0] for c in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]


def to_num(v) -> float:
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def parse_date(raw) -> Optional[str]:
    """Parse YYYY-MM-DD / DD/MM/YYYY etc. into ISO date string for MySQL."""
    raw = (raw or "").strip() if isinstance(raw, str) else raw
    if not raw or raw == "00/00/0000":
        return None
    if isinstance(raw, str):
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%m/%d/%Y"):
            try:
                return datetime.strptime(raw, fmt).date().isoformat()
            except ValueError:
                continue
    return None


# ---------------------------------------------------------------------------
# Counters / voucher numbers
# ---------------------------------------------------------------------------

def gen_int(code: str) -> int:
    if not table_exists("generali"):
        return 0
    try:
        with connection.cursor() as cur:
            cur.execute("SELECT cvalue FROM generali WHERE code = %s LIMIT 1", [code])
            row = cur.fetchone()
            return int(to_num(row[0])) if row and row[0] is not None else 0
    except Exception:
        return 0


def general_profile(code: str, default: str = "") -> str:
    if not table_exists("generals"):
        return default
    try:
        with connection.cursor() as cur:
            cur.execute("SELECT cvalue FROM generals WHERE code = %s LIMIT 1", [code])
            row = cur.fetchone()
            v = (str(row[0]).strip() if row and row[0] is not None else "")
            return v or default
    except Exception:
        return default


def increment_gen_int(code: str) -> int:
    if not table_exists("generali"):
        return 1
    cur_val = gen_int(code)
    nxt = cur_val + 1
    with connection.cursor() as cur:
        cur.execute("UPDATE generali SET cvalue = %s WHERE code = %s", [nxt, code])
        if cur.rowcount == 0:
            cur.execute("INSERT INTO generali (code, cvalue) VALUES (%s, %s)", [code, nxt])
    return nxt


def last_voucher_number_for_prefix(prefix: str) -> int:
    if not prefix or not table_exists("daybookpart"):
        return 0
    cols = columns("daybookpart")
    if "vchno" not in cols:
        return 0
    try:
        with connection.cursor() as cur:
            cur.execute(
                "SELECT vchno FROM daybookpart WHERE vchno LIKE %s",
                [prefix + "%"],
            )
            best = 0
            for (vchno,) in cur.fetchall():
                v = (vchno or "").strip()
                if not v.startswith(prefix):
                    continue
                suf = v[len(prefix):]
                if suf.isdigit():
                    n = int(suf)
                    if n > best:
                        best = n
            return best
    except Exception:
        return 0


def reserve_voucher(prefix: str, counter_code: str, pad: int = 5) -> str:
    cur_val = gen_int(counter_code)
    max_used = last_voucher_number_for_prefix(prefix)
    nxt = max(cur_val, max_used) + 1
    if table_exists("generali"):
        with connection.cursor() as cur:
            cur.execute("UPDATE generali SET cvalue = %s WHERE code = %s", [nxt, counter_code])
            if cur.rowcount == 0:
                cur.execute("INSERT INTO generali (code, cvalue) VALUES (%s, %s)",
                            [counter_code, nxt])
    return f"{prefix}{nxt:0{pad}d}"


def preview_voucher(prefix: str, counter_code: str, pad: int = 5) -> str:
    cur_val = gen_int(counter_code)
    max_used = last_voucher_number_for_prefix(prefix)
    nxt = max(cur_val, max_used) + 1
    return f"{prefix}{nxt:0{pad}d}"


def next_serial_no() -> int:
    """Global slno across all transaction tables."""
    if not table_exists("generali"):
        return 1
    current = gen_int("SERIALNO")
    max_used = 0
    for tbl in ("salesm", "salesrm", "purchasem", "purchaserm", "daybook",
                "daybookpart", "orderm", "smithm", "refinerym", "repairm"):
        if not table_exists(tbl):
            continue
        if "slno" not in columns(tbl):
            continue
        try:
            with connection.cursor() as cur:
                cur.execute(f"SELECT COALESCE(MAX(slno), 0) FROM `{tbl}`")
                v = int(cur.fetchone()[0] or 0)
                if v > max_used:
                    max_used = v
        except Exception:
            pass
    nxt = max(current, max_used) + 1
    with connection.cursor() as cur:
        cur.execute("UPDATE generali SET cvalue = %s WHERE code = %s", [nxt, "SERIALNO"])
        if cur.rowcount == 0:
            cur.execute("INSERT INTO generali (code, cvalue) VALUES (%s, %s)",
                        ["SERIALNO", nxt])
    return nxt


# ---------------------------------------------------------------------------
# Account balance
# ---------------------------------------------------------------------------

def account_balance(accode: str, control: int = 1) -> float:
    if not accode or not table_exists("daybook"):
        return 0.0
    total = 0.0
    try:
        with connection.cursor() as cur:
            cur.execute(
                "SELECT COALESCE(SUM(amount), 0) FROM daybook "
                "WHERE TRIM(accode) = %s AND control = %s",
                [accode.strip(), control],
            )
            total = float(cur.fetchone()[0] or 0)
    except Exception:
        total = 0.0
    if table_exists("accountm"):
        cols = columns("accountm")
        col = "opbal" if control == 1 else ("opbalb" if "opbalb" in cols else "opbal")
        try:
            with connection.cursor() as cur:
                cur.execute(
                    f"SELECT COALESCE(`{col}`, 0) FROM accountm WHERE TRIM(accode) = %s LIMIT 1",
                    [accode.strip()],
                )
                row = cur.fetchone()
                if row:
                    total += float(row[0] or 0)
        except Exception:
            pass
    return total


# ---------------------------------------------------------------------------
# Posting (the core write)
# ---------------------------------------------------------------------------

def filter_to_columns(row: dict, available: set) -> dict:
    return {k: v for k, v in row.items() if k.lower() in available}


def post_voucher(
    *,
    slno: int,
    tdate: str,
    vchno: str,
    control: int,
    user_code: str,
    cb_accode: str,
    party_accode: str,
    amount: float,
    direction: str,            # "R" (receipt) | "P" (payment)
    particular: str = "",
    discount: float = 0.0,
    discount_accode: Optional[str] = None,
    extra_dp_fields: Optional[dict] = None,
) -> None:
    """Write a daybookpart header + 2-3 daybook lines for a receipt/payment.

    Sign conventions (matching the legacy app):
      Receipt: party  +amount + discount   (debit reduces / credit increases)
               cb     -amount               (cash flowed in to bank)
               disc   -discount             (discount given to customer)
      Payment: party  -amount - discount
               cb     +amount
               disc   +discount

    Caller is responsible for opening a transaction.
    """
    if not table_exists("daybook") or not table_exists("daybookpart"):
        raise RuntimeError("daybook/daybookpart tables not present")

    db_cols = columns("daybook")
    dp_cols = columns("daybookpart")

    dp_row = {
        "slno": slno,
        "vchno": vchno,
        "particular": (particular or "")[:200],
        "tdate": tdate,
        "control": control,
        "ic": (user_code or "")[:20],
        "ttime": datetime.now().strftime("%H:%M:%S"),
        "discount": round(abs(discount), 2),
    }
    if extra_dp_fields:
        dp_row.update(extra_dp_fields)
    dp_row = filter_to_columns(dp_row, dp_cols)

    with connection.cursor() as cur:
        cols_list = list(dp_row.keys())
        placeholders = ", ".join(["%s"] * len(cols_list))
        cur.execute(
            f"INSERT INTO daybookpart ({', '.join(f'`{c}`' for c in cols_list)}) "
            f"VALUES ({placeholders})",
            list(dp_row.values()),
        )

        sign = 1 if direction == "R" else -1
        party_total = round(amount + abs(discount), 2) * sign
        cb_amount = -round(amount, 2) * sign

        for accode, amt, opacc in (
            (party_accode, party_total, cb_accode),
            (cb_accode, cb_amount, party_accode),
        ):
            row = {
                "slno": slno, "tdate": tdate, "accode": accode,
                "amount": amt, "control": control, "opaccode": opacc,
            }
            row = filter_to_columns(row, db_cols)
            cur.execute(
                f"INSERT INTO daybook ({', '.join(f'`{c}`' for c in row)}) "
                f"VALUES ({', '.join(['%s'] * len(row))})",
                list(row.values()),
            )

        if discount and discount_accode:
            disc_amt = -round(abs(discount), 2) * sign
            row = {
                "slno": slno, "tdate": tdate, "accode": discount_accode,
                "amount": disc_amt, "control": control, "opaccode": party_accode,
            }
            row = filter_to_columns(row, db_cols)
            cur.execute(
                f"INSERT INTO daybook ({', '.join(f'`{c}`' for c in row)}) "
                f"VALUES ({', '.join(['%s'] * len(row))})",
                list(row.values()),
            )


def post_journal(
    *,
    slno: int,
    tdate: str,
    vchno: str,
    control: int,
    user_code: str,
    debit_accode: str,
    credit_accode: str,
    amount: float,
    particular: str = "",
) -> None:
    """Write a 2-line journal voucher: debit account +amount, credit -amount."""
    if not table_exists("daybook") or not table_exists("daybookpart"):
        raise RuntimeError("daybook/daybookpart tables not present")
    db_cols = columns("daybook")
    dp_cols = columns("daybookpart")

    dp_row = filter_to_columns({
        "slno": slno, "vchno": vchno, "particular": (particular or "")[:200],
        "tdate": tdate, "control": control, "ic": (user_code or "")[:20],
        "ttime": datetime.now().strftime("%H:%M:%S"),
    }, dp_cols)

    with connection.cursor() as cur:
        cur.execute(
            f"INSERT INTO daybookpart ({', '.join(f'`{c}`' for c in dp_row)}) "
            f"VALUES ({', '.join(['%s'] * len(dp_row))})",
            list(dp_row.values()),
        )
        for accode, amt, opacc in (
            (debit_accode, abs(amount), credit_accode),
            (credit_accode, -abs(amount), debit_accode),
        ):
            row = filter_to_columns({
                "slno": slno, "tdate": tdate, "accode": accode,
                "amount": round(amt, 2), "control": control, "opaccode": opacc,
            }, db_cols)
            cur.execute(
                f"INSERT INTO daybook ({', '.join(f'`{c}`' for c in row)}) "
                f"VALUES ({', '.join(['%s'] * len(row))})",
                list(row.values()),
            )


def list_cash_bank_accounts() -> list:
    if not table_exists("accountm"):
        return []
    cols = columns("accountm")
    if "actype2" not in cols:
        return []
    where = ["TRIM(actype2) IN ('H','B')"]
    if "removed" in cols:
        where.append("(removed <> 1 OR removed IS NULL)")
    sql = (
        f"SELECT TRIM(accode) AS accode, TRIM(name) AS name, TRIM(actype2) AS actype2 "
        f"FROM accountm WHERE {' AND '.join(where)} ORDER BY accode"
    )
    try:
        with connection.cursor() as cur:
            cur.execute(sql)
            return row_dicts(cur)
    except Exception:
        return []


def list_accounts(filter_type: str = "", search: str = "") -> list:
    if not table_exists("accountm"):
        return []
    cols = columns("accountm")
    select = ["TRIM(accode) AS accode"]
    select.append("TRIM(name) AS name" if "name" in cols else "TRIM(accode) AS name")
    if "actype2" in cols:
        select.append("actype2")
    where = []
    params: list = []
    if "removed" in cols:
        where.append("(removed <> 1 OR removed IS NULL)")
    t = (filter_type or "").upper()
    if t in {"C", "S", "J", "G", "R", "F"} and "actype2" in cols:
        where.append("TRIM(actype2) = %s")
        params.append(t)
    elif t == "O" and "actype2" in cols:
        where.append("TRIM(actype2) NOT IN ('C','S','J','G','R','F','H','B')")
    if search:
        where.append("(TRIM(accode) LIKE %s OR TRIM(name) LIKE %s)")
        s = f"%{search}%"
        params += [s, s]
    sql = f"SELECT {', '.join(select)} FROM accountm"
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY name"
    try:
        with connection.cursor() as cur:
            cur.execute(sql, params)
            return row_dicts(cur)
    except Exception:
        return []
