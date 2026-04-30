"""
Master-data CRUD views — port of the simpler Laravel controllers:
ItemMasterController, ModelMasterController, StockTypeController, GiftTableController.
"""
from __future__ import annotations

import json

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from ..models import GiftTable, Item, ProductModel, Rotable, StockType


# ---- Item Master ----

def item_master__index(request):
    items = Item.objects.order_by("code")[:500]
    return render(request, "item-master/index.html", {"items": items})


@csrf_exempt
@require_http_methods(["POST"])
def item_master__save(request):
    data = json.loads(request.body or "{}") if request.content_type == "application/json" else request.POST
    code = (data.get("code") or "").strip().upper()
    name = (data.get("name") or "").strip()
    if not code or not name:
        return JsonResponse({"ok": False, "error": "code and name required"}, status=400)
    obj, created = Item.objects.update_or_create(code=code, defaults={"name": name})
    return JsonResponse({"ok": True, "created": created, "code": obj.code})


@csrf_exempt
@require_http_methods(["POST"])
def item_master__delete(request):
    data = json.loads(request.body or "{}") if request.content_type == "application/json" else request.POST
    code = (data.get("code") or "").strip().upper()
    if not code:
        return JsonResponse({"ok": False, "error": "code required"}, status=400)
    with transaction.atomic():
        Rotable.objects.filter(code=code).delete()
        deleted, _ = Item.objects.filter(code=code).delete()
    return JsonResponse({"ok": True, "deleted": deleted})


# ---- Model Master ----

def model_master__index(request):
    models = ProductModel.objects.filter(mtype="M").order_by("name")
    sizes = ProductModel.objects.filter(mtype="S").order_by("name")
    return render(request, "model-master/index.html", {"models": models, "sizes": sizes})


@csrf_exempt
@require_http_methods(["POST"])
def model_master__save(request):
    data = json.loads(request.body or "{}") if request.content_type == "application/json" else request.POST
    mtype = (data.get("mtype") or "M").upper()[:1]
    name = (data.get("name") or "").strip()
    if not name:
        return JsonResponse({"ok": False, "error": "name required"}, status=400)
    obj, created = ProductModel.objects.update_or_create(mtype=mtype, name=name, defaults={})
    return JsonResponse({"ok": True, "created": created, "id": obj.id})


@csrf_exempt
@require_http_methods(["POST"])
def model_master__delete(request):
    data = json.loads(request.body or "{}") if request.content_type == "application/json" else request.POST
    pk = data.get("id")
    if not pk:
        return JsonResponse({"ok": False, "error": "id required"}, status=400)
    deleted, _ = ProductModel.objects.filter(pk=pk).delete()
    return JsonResponse({"ok": True, "deleted": deleted})


@csrf_exempt
@require_http_methods(["POST"])
def model_master__check_duplicate(request):
    data = json.loads(request.body or "{}") if request.content_type == "application/json" else request.POST
    mtype = (data.get("mtype") or "M").upper()[:1]
    name = (data.get("name") or "").strip()
    exists = ProductModel.objects.filter(mtype=mtype, name=name).exists()
    return JsonResponse({"ok": True, "exists": exists})


def model_master__get_by_type(request):
    mtype = (request.GET.get("type") or request.POST.get("type") or "M").upper()[:1]
    qs = ProductModel.objects.filter(mtype=mtype).order_by("name").values_list("name", flat=True)
    return JsonResponse({"ok": True, "items": list(qs)})


# ---- Stock Type ----

def stock_type__index(request):
    rows = StockType.objects.order_by("code")
    return render(request, "stocktype/index.html", {"rows": rows})


def stock_type__get_list(request):
    qs = StockType.objects.order_by("code").values("id", "code", "name", "is_default", "compare")
    items = [{"id": r["id"], "code": r["code"], "name": r["name"],
              "def": r["is_default"], "compare": r["compare"]} for r in qs]
    return JsonResponse({"ok": True, "items": items})


def stock_type__get_default(request):
    obj = StockType.objects.filter(is_default=1).first()
    if not obj:
        return JsonResponse({"ok": True, "default": None})
    return JsonResponse({"ok": True, "default": {"code": obj.code, "name": obj.name}})


@csrf_exempt
@require_http_methods(["POST"])
def stock_type__check_code(request):
    data = json.loads(request.body or "{}") if request.content_type == "application/json" else request.POST
    code = (data.get("code") or "").strip().upper()
    return JsonResponse({"ok": True, "exists": StockType.objects.filter(code=code).exists()})


@csrf_exempt
@require_http_methods(["POST"])
def stock_type__store(request):
    data = json.loads(request.body or "{}") if request.content_type == "application/json" else request.POST
    code = (data.get("code") or "").strip().upper()
    name = (data.get("name") or "").strip()
    is_def = 1 if str(data.get("def", "0")) in ("1", "true", "True", "on") else 0
    is_cmp = 1 if str(data.get("compare", "0")) in ("1", "true", "True", "on") else 0
    if not code or not name:
        return JsonResponse({"ok": False, "error": "code and name required"}, status=400)

    with transaction.atomic():
        if is_def:
            StockType.objects.update(is_default=0)
        obj, created = StockType.objects.update_or_create(
            code=code,
            defaults={"name": name, "is_default": is_def, "compare": is_cmp},
        )
    return JsonResponse({"ok": True, "created": created, "id": obj.id})


@csrf_exempt
@require_http_methods(["PUT", "POST"])
def stock_type__update(request, code):
    data = json.loads(request.body or "{}") if request.content_type == "application/json" else request.POST
    code = (code or "").strip().upper()
    obj = StockType.objects.filter(code=code).first()
    if not obj:
        return JsonResponse({"ok": False, "error": "not found"}, status=404)
    obj.name = (data.get("name") or obj.name).strip()
    obj.is_default = 1 if str(data.get("def", obj.is_default)) in ("1", "true", "True", "on") else 0
    obj.compare = 1 if str(data.get("compare", obj.compare)) in ("1", "true", "True", "on") else 0
    with transaction.atomic():
        if obj.is_default:
            StockType.objects.exclude(pk=obj.pk).update(is_default=0)
        obj.save()
    return JsonResponse({"ok": True})


@csrf_exempt
@require_http_methods(["DELETE", "POST"])
def stock_type__destroy(request, code):
    code = (code or "").strip().upper()
    deleted, _ = StockType.objects.filter(code=code).delete()
    return JsonResponse({"ok": True, "deleted": deleted})


# ---- Gift Table ----

def gift_table__index(request):
    rows = GiftTable.objects.order_by("points")
    return render(request, "gift-table/index.html", {"rows": rows})


@csrf_exempt
@require_http_methods(["POST"])
def gift_table__save(request):
    data = json.loads(request.body or "{}") if request.content_type == "application/json" else request.POST
    points = data.get("points")
    particulars = (data.get("particulars") or "").strip()
    if points in (None, ""):
        return JsonResponse({"ok": False, "error": "points required"}, status=400)
    obj, created = GiftTable.objects.update_or_create(
        points=int(points), defaults={"particulars": particulars}
    )
    return JsonResponse({"ok": True, "created": created})


@csrf_exempt
@require_http_methods(["POST"])
def gift_table__delete(request):
    data = json.loads(request.body or "{}") if request.content_type == "application/json" else request.POST
    points = data.get("points")
    if points in (None, ""):
        return JsonResponse({"ok": False, "error": "points required"}, status=400)
    deleted, _ = GiftTable.objects.filter(points=int(points)).delete()
    return JsonResponse({"ok": True, "deleted": deleted})
