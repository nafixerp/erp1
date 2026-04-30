"""
Legacy `fpCrypt` password algorithm port from Laravel's UserM model.

The original Laravel `UserM::fpCrypt` does a per-character offset cipher
where each character's ASCII value is shifted by `(index+1) * (length+2)`,
then converted from Windows-1252 to UTF-8. We reproduce both the algorithm
and the multiple verification fallbacks (raw fpCrypt bytes, hex of bytes,
'SHA256:'+sha256, plaintext).
"""
from __future__ import annotations

import hashlib
from typing import Optional

from django.db import connection


def fp_crypt(password: str, mode: int = 1) -> bytes:
    """Reproduces Laravel UserM::fpCrypt(pcode, 1).

    Returns the raw bytes that get stored as `pcode` in `userm`.
    """
    trimmed = password.strip()
    length = len(trimmed)
    if length == 0:
        return b""

    # Replicate the PHP quirk: result starts with a single space, then trim().
    out_chars = [" "]
    for index in range(length):
        char = password[index] if index < len(password) else ""
        if not char:
            continue
        offset = (index + 1) * (length + 2)
        ascii_val = ord(char)
        new_val = ascii_val + offset if mode == 1 else ascii_val - offset
        # PHP chr() wraps modulo 256 on out-of-range values implicitly via
        # binary string semantics; mimic that.
        out_chars.append(chr(new_val % 256))

    result = "".join(out_chars).strip()
    if result == "":
        return b""

    # PHP did mb_convert_encoding($result, 'UTF-8', 'Windows-1252').
    # The bytes that were stored are the Windows-1252 byte representation
    # of `result`. cp1252 with errors='replace' approximates the same map.
    try:
        return result.encode("cp1252")
    except UnicodeEncodeError:
        return result.encode("cp1252", errors="replace")


def fp_crypt_hex(password: str) -> str:
    """Uppercase hex of fp_crypt — what Laravel compared via UPPER(HEX(pcode))."""
    return fp_crypt(password).hex().upper()


def authenticate_legacy(password: str) -> Optional[dict]:
    """Match the password against any user in `userm` (legacy single-PIN flow)."""
    target_hex = fp_crypt_hex(password)
    if not target_hex:
        return None

    with connection.cursor() as cur:
        cur.execute(
            "SELECT code, name FROM userm WHERE UPPER(HEX(pcode)) = %s LIMIT 1",
            [target_hex],
        )
        row = cur.fetchone()
    if not row:
        return None
    return {"code": (row[0] or "").strip(), "name": (row[1] or "").strip()}


def authenticate_for_code(code: str, password: str) -> Optional[dict]:
    code = code.strip()
    if not code:
        return None

    raw = fp_crypt(password)
    hex_ = raw.hex().upper()
    sha = "SHA256:" + hashlib.sha256(password.encode("utf-8")).hexdigest()

    with connection.cursor() as cur:
        cur.execute(
            """
            SELECT code, name FROM userm
            WHERE UPPER(TRIM(code)) = %s
              AND (UPPER(HEX(pcode)) = %s OR pcode = %s OR pcode = %s OR pcode = %s)
            LIMIT 1
            """,
            [code.upper(), hex_, raw, sha, password],
        )
        row = cur.fetchone()
    if not row:
        return None
    return {"code": (row[0] or "").strip(), "name": (row[1] or "").strip()}
