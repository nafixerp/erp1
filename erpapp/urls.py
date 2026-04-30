"""
Top-level URL conf for the ERP app.

We:
  1) hand-wire a small set of routes (login, logout, dashboard, root, healthz),
  2) pull in every Laravel route from _generated_urls.py, but allow specific
     `name=` keys to be overridden by hand-implemented views.

Add new overrides in `OVERRIDES` as you port more controllers.
"""
from django.urls import path

from . import _generated_urls
from .views import auth_views, core_views, customers, masters, sales_bill, stock


# Map URL `name` -> hand-implemented view callable.
OVERRIDES = {
    # auth + core
    "nativeauth.showLogin": auth_views.show_login,
    "nativeauth.login": auth_views.login,
    "nativeauth.logout": auth_views.logout,
    "nativedashboard.index": core_views.dashboard,

    # masters
    "itemmaster.index": masters.item_master__index,
    "itemmaster.save": masters.item_master__save,
    "itemmaster.delete": masters.item_master__delete,

    "modelmaster.index": masters.model_master__index,
    "modelmaster.save": masters.model_master__save,
    "modelmaster.delete": masters.model_master__delete,
    "modelmaster.checkDuplicate": masters.model_master__check_duplicate,
    "modelmaster.getByType": masters.model_master__get_by_type,

    "stocktype.index": masters.stock_type__index,
    "stocktype.getList": masters.stock_type__get_list,
    "stocktype.getDefault": masters.stock_type__get_default,
    "stocktype.checkCode": masters.stock_type__check_code,
    "stocktype.store": masters.stock_type__store,
    "stocktype.update": masters.stock_type__update,
    "stocktype.destroy": masters.stock_type__destroy,

    "gifttable.index": masters.gift_table__index,
    "gifttable.save": masters.gift_table__save,
    "gifttable.delete": masters.gift_table__delete,

    # customer master (NativeCustomerController)
    "nativecustomer.index": customers.index,
    "nativecustomer.add": customers.add,
    "nativecustomer.edit": customers.edit,
    "nativecustomer.deletePage": customers.delete_page,
    "nativecustomer.nextCode": customers.next_code,
    "nativecustomer.get": customers.get,
    "nativecustomer.save": customers.save,
    "nativecustomer.delete": customers.delete,
    "nativecustomer.checkPhone": customers.check_phone,
    "nativecustomer.checkIdNo": customers.check_id_no,

    # sales bill (SalesBillController)
    "salesbill.index": sales_bill.index,
    "salesbill.nextBillNo": sales_bill.next_bill_no,
    "salesbill.checkBillNo": sales_bill.check_bill_no,
    "salesbill.get": sales_bill.get,
    "salesbill.search": sales_bill.search,
    "salesbill.customerSearch": sales_bill.customer_search,
    "salesbill.customerDetails": sales_bill.customer_details,
    "salesbill.customerByMobile": sales_bill.customer_by_mobile,
    "salesbill.save": sales_bill.save,
    "salesbill.cancelBill": sales_bill.cancel_bill,
    "salesbill.confirmBill": sales_bill.confirm_bill,

    # stock (StockController)
    "stock.index": stock.index,
    "stock.update": stock.update,
    "stock.stockList": stock.stock_list,
    "stock.stockListData": stock.stock_list_data,
}

urlpatterns = [
    path("", core_views.root, name="root"),
    path("login", auth_views.show_login, name="login"),
    path("logout", auth_views.logout, name="logout"),
    path("dashboard", core_views.dashboard, name="dashboard"),
    path("healthz", core_views.healthz, name="healthz"),

    # Alias for the Laravel route `/sales-bill/{mode?}` whose optional segment
    # got compiled to a required Django `<str:mode>`.
    path("sales-bill", sales_bill.index, name="sales-bill.bare"),
] + _generated_urls.build_patterns(view_overrides=OVERRIDES)
