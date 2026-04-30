# ERP — Django port (in progress)

This branch is a port of the Laravel 12 ERP application (originally in
`TESTER.zip`) to Django 5. It is **a foundation, not a finished port**:
all routes are registered, models for migration-defined tables are
translated, auth works, and a handful of master-data flows are wired
end-to-end. The remaining ~140 controllers are registered as stubs that
return HTTP 501 until ported.

## Layout

```
manage.py
requirements.txt
.env.example
erp/                      # Django project (settings, urls, wsgi)
  settings.py
  urls.py
  wsgi.py
  asgi.py
erpapp/                   # Single Django app holding the ERP code
  models.py               # Managed + unmanaged (legacy) models
  middleware.py           # ApplySelectedDatabase + CheckMenuAccess
  context_processors.py   # shop_settings (SHOPNM, SHOPADDR, ...)
  auth_legacy.py          # fpCrypt password algorithm port
  urls.py                 # Hand-wired routes + generated routes w/ overrides
  _generated_urls.py      # AUTO-GENERATED 800 routes from routes/web.php
  _generated_views.py     # AUTO-GENERATED 799 stub view functions
  views/
    auth_views.py         # NativeAuthController port (login/logout)
    core_views.py         # root + dashboard + healthz
    masters.py            # ItemMaster, ModelMaster, StockType, GiftTable
templates/
  base.html               # Shared layout
  stub.html               # Rendered for any unported HTML route
  native/login.html       # Port of resources/views/native/login.blade.php
  native/dashboard.html
  item-master/index.html
  model-master/index.html
  stocktype/index.html
  gift-table/index.html
```

## Status

| Area | Status |
| --- | --- |
| Project skeleton, settings, URL routing | Done |
| Models: migration-defined tables (items, models, rotable, stktype, pmctable, mctable, gifttable, pcardtable, denom_master, route, area, pcard, clients_advanced, sales_bills) | Done — managed |
| Models: legacy tables (userm, userd, userhist, generals, generali, clients, accountm, daybook, daybookpart, itemsstk, salestype, salesm/d, purchasem/d, orderm/d, smithm/d, refinerym/d, repairm/d, itemadj, delpart, oitemtranm) | Stubs — unmanaged, columns added incrementally as needed |
| Auth (NativeAuthController + fpCrypt) | Done |
| CheckMenuAccess + ApplySelectedDatabase middleware | Done (gating works; full multi-DB switching is a follow-up) |
| All 800 routes from `routes/web.php` (+ 1 closure for `/`) | Registered |
| Implemented controllers | Item Master, Model Master, Stock Type, Gift Table, Native Auth, Native Dashboard, Native Customer, Sales Bill |
| Stub controllers | ~138 — return HTTP 501 |
| Views/templates ported | login, dashboard, stub, item-master, model-master, stocktype, gift-table, customer/list, customer/form, sales-bill/index |

## Running

```bash
# 1. Create a venv and install
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. Configure DB
cp .env.example .env
# Edit .env: point at the same MySQL DB the Laravel app used,
# OR set DB_ENGINE=django.db.backends.sqlite3 to test the managed
# tables without the legacy schema.

# 3. Apply Django-managed migrations
python manage.py migrate

# 4. Run
python manage.py runserver
```

Visit `http://localhost:8000/login`. Passwords use the same legacy
`fpCrypt` algorithm as the Laravel app, so any existing `userm` row
will authenticate unchanged.

## How to port a controller

1. Read the Laravel source at
   `_laravel_src/app/Http/Controllers/<Name>Controller.php` (the original
   ZIP is preserved as `TESTER.zip` and extracted to `_laravel_src/` —
   the latter is gitignored; re-extract with `unzip TESTER.zip -d _laravel_src`).
2. Add a Python view function in a new module under `erpapp/views/`.
3. Register it in `OVERRIDES` in `erpapp/urls.py` keyed by the URL
   `name=` from `_generated_urls.py` (e.g. `"salesbill.save"`).
4. If the controller queries legacy tables that aren't yet declared in
   `erpapp/models.py`, either add the missing columns to the unmanaged
   model or use raw SQL via `django.db.connection.cursor()`.
5. Convert the corresponding Blade template under
   `_laravel_src/resources/views/...` into a Django template under
   `templates/...`. Replace `@extends`, `@section`, `{{ }}` Blade syntax
   with their Django template equivalents.

## Regenerating routes / stubs

If the original `routes/web.php` changes, re-run the parser:

```bash
unzip -o TESTER.zip -d _laravel_src
python _laravel_src/scripts/parse_routes.py
```

This rewrites `erpapp/_generated_urls.py` and `erpapp/_generated_views.py`.
Hand-implemented overrides in `erpapp/urls.py:OVERRIDES` keep working.

## Known gaps

- **Reports**: 100+ report controllers (DayBook, CashBook, JournalReport,
  StockSummaryRateWise, etc.) are stubs. Most read raw SQL from legacy
  tables; port one at a time as needed.
- **Multi-tenant DB switching** (`ApplySelectedDatabase` in Laravel)
  routes some queries to a per-customer database. The Django middleware
  records the selected DB on `request.selected_database` but does not
  yet swap connections per request — needs a Django DB router.
- **Background jobs**: Laravel queues (`jobs`, `failed_jobs`) are not
  ported — the few queue use sites should be migrated to Celery or
  django-q.
- **Blade-only templates**: 285 of 292 original Blade templates are
  un-ported. Convert as you wire each controller.
- **CSRF on `*_OVERRIDES_*`**: hand-implemented POST views currently use
  `@csrf_exempt`. Drop the decorator and pass `{% csrf_token %}` from
  the calling template once the form layer is rewritten in Django.
