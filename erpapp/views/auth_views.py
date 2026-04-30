"""Login / logout — port of NativeAuthController."""
from datetime import datetime

from django.db import connection
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .. import auth_legacy
from ..context_processors import _generals


def _greeting() -> str:
    h = datetime.now().hour
    if 5 <= h < 12:
        return "Good Morning"
    if 12 <= h < 17:
        return "Good Afternoon"
    if 17 <= h < 22:
        return "Good Evening"
    return "Welcome"


def _login_context(error: str = "") -> dict:
    return {
        "shop_name": _generals("SHOPNM", "Proaims Custom Dashboard"),
        "shop_addr": _generals("SHOPADDR"),
        "shop_phone": _generals("SHOPPHONE"),
        "shop_gst": _generals("GSTIN") or _generals("GSTNO"),
        "greeting": _greeting(),
        "error": error,
    }


def show_login(request):
    if request.session.get("user_code"):
        return redirect("/dashboard")
    return render(request, "native/login.html", _login_context())


def _table_exists(name: str) -> bool:
    try:
        with connection.cursor() as cur:
            cur.execute("SHOW TABLES LIKE %s", [name])
            return cur.fetchone() is not None
    except Exception:
        return False


@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    password = (request.POST.get("password") or "").strip()
    if not password:
        return render(request, "native/login.html", _login_context("Please enter password"))

    if not _table_exists("userm"):
        return render(
            request, "native/login.html",
            _login_context("Login table not found. Import database_schema.sql and verify DB_DATABASE."),
        )

    try:
        user = auth_legacy.authenticate_legacy(password)
    except Exception:
        return render(
            request, "native/login.html",
            _login_context("Login table is not readable. Repair/recreate userm and retry."),
        )

    if not user:
        return render(request, "native/login.html", _login_context("Invalid password"))

    request.session["user_code"] = user["code"]
    request.session["user_name"] = user["name"]
    request.session["gsuserid"] = user["code"]
    request.session["gsusername"] = user["name"]
    request.session["login_time"] = int(datetime.now().timestamp())

    blocked = []
    if _table_exists("userd"):
        with connection.cursor() as cur:
            cur.execute("SELECT menuitem FROM userd WHERE TRIM(code) = %s", [user["code"]])
            blocked = [(r[0] or "").strip() for r in cur.fetchall()]
    request.session["blocked_items"] = blocked
    request.session["readonly"] = "Y" if any(b.upper() == "READONLY" for b in blocked) else "N"

    if _table_exists("userhist"):
        try:
            with connection.cursor() as cur:
                cur.execute(
                    "INSERT INTO userhist (code, tdate, time1) VALUES (%s, %s, %s)",
                    [user["code"], datetime.now().date(), datetime.now().strftime("%H:%M:%S")],
                )
        except Exception:
            pass

    return redirect("/dashboard")


def logout(request):
    user_code = request.session.get("user_code")
    if user_code and _table_exists("userhist"):
        try:
            today = datetime.now().date()
            with connection.cursor() as cur:
                cur.execute(
                    "UPDATE userhist SET time2 = %s "
                    "WHERE TRIM(code) = %s AND tdate = %s "
                    "AND (time2 IS NULL OR time2 = '')",
                    [datetime.now().strftime("%H:%M:%S"), user_code, today],
                )
        except Exception:
            pass

    request.session.flush()
    return redirect("/login")
