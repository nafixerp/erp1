"""Template context — exposes shop name/logo/etc. like Laravel's view composers."""
from django.db import connection


def _generals(code: str, default: str = "") -> str:
    try:
        with connection.cursor() as cur:
            cur.execute("SELECT cvalue FROM generals WHERE code = %s LIMIT 1", [code])
            row = cur.fetchone()
        return (row[0] or default) if row else default
    except Exception:
        return default


def shop_settings(request):
    return {
        "shop_name": _generals("SHOPNM", "ERP"),
        "shop_addr": _generals("SHOPADDR"),
        "shop_phone": _generals("SHOPPHONE"),
        "shop_gst": _generals("GSTIN") or _generals("GSTNO"),
        "user_code": request.session.get("user_code"),
        "user_name": request.session.get("user_name"),
    }
