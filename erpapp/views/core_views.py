"""Dashboard, root, healthcheck."""
from django.http import JsonResponse
from django.shortcuts import redirect, render


def root(request):
    if request.session.get("user_code"):
        return redirect("/dashboard")
    return redirect("/login")


def dashboard(request):
    if not request.session.get("user_code"):
        return redirect("/login")
    return render(request, "native/dashboard.html", {})


def healthz(request):
    return JsonResponse({"ok": True})
