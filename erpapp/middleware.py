"""
Middleware ports of:
  - app/Http/Middleware/ApplySelectedDatabase.php  (per-request DB switching
    based on session/cookie). For the Django port we read the cookie and
    expose the selected DB name on `request.selected_database`; full
    multi-tenant DB switching is left as a follow-up since it requires
    Django DB router wiring.
  - app/Http/Middleware/CheckMenuAccess.php  (gates URL access via the
    user's `userd` row list). Login/static URLs are exempt.
"""
from __future__ import annotations

from django.db import connection
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import resolve, Resolver404


EXEMPT_PREFIXES = (
    "/login", "/logout", "/static/", "/media/", "/favicon",
    "/company-select", "/api/application-settings", "/healthz",
)


class ApplySelectedDatabaseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.selected_database = (
            request.COOKIES.get("selected_company_database")
            or request.session.get("selected_database")
            or ""
        )
        return self.get_response(request)


class CheckMenuAccessMiddleware:
    """Equivalent of Laravel CheckMenuAccess — requires login + checks `userd`."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path or "/"

        if any(path == p or path.startswith(p) for p in EXEMPT_PREFIXES):
            return self.get_response(request)

        user_code = request.session.get("user_code")
        if not user_code:
            if request.method == "GET":
                return redirect("/login")
            return HttpResponseForbidden("Login required")

        # Resolve the URL name to compare against blocked menu items.
        try:
            match = resolve(path)
            url_name = match.url_name or ""
        except Resolver404:
            url_name = ""

        blocked = request.session.get("blocked_items") or []
        # Block items are stored as uppercase tokens; we only block when the
        # URL name is explicitly listed (best-effort, controllers can refine).
        if url_name and url_name.upper() in {b.strip().upper() for b in blocked}:
            return HttpResponseForbidden("Access denied for this menu item")

        return self.get_response(request)


def _has_table(name: str) -> bool:
    try:
        with connection.cursor() as cur:
            cur.execute("SHOW TABLES LIKE %s", [name])
            return cur.fetchone() is not None
    except Exception:
        return False
