"""
Hand-implemented views (override generated stubs).

Each module exports view callables with names matching the URL `name=`
in erpapp._generated_urls (e.g. `nativeauth.login`).
"""
from . import (
    auth_views, cashflow, core_views, customers, masters,
    reports, sales_bill, sales_return, stock,
)
