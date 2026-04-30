"""
AUTO-GENERATED view stubs — one per Laravel controller@action.
Do not edit by hand. Replace stubs incrementally by re-exporting
the same name from erpapp/views/<module>.py.
"""
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


def _stub(controller, action, request):
    if request.path.startswith('/api/'):
        return JsonResponse({
            'ok': False,
            'stub': True,
            'controller': controller,
            'action': action,
        }, status=501)
    return render(request, 'stub.html', {
        'controller': controller,
        'action': action,
    }, status=501)


# ---- AcReceivablePayableSummaryController ----
def ac_receivable_payable_summary__index(request, *args, **kwargs):
    return _stub('AcReceivablePayableSummaryController', 'index', request)


# ---- AccountLedgerController ----
def account_ledger__index(request, *args, **kwargs):
    return _stub('AccountLedgerController', 'index', request)

def account_ledger__repair_sales_ledger(request, *args, **kwargs):
    return _stub('AccountLedgerController', 'repairSalesLedger', request)

def account_ledger__customer_ledger_api(request, *args, **kwargs):
    return _stub('AccountLedgerController', 'customerLedgerApi', request)


# ---- AccountMasterController ----
def account_master__account(request, *args, **kwargs):
    return _stub('AccountMasterController', 'account', request)

def account_master__api_account(request, *args, **kwargs):
    return _stub('AccountMasterController', 'apiAccount', request)

def account_master__groups(request, *args, **kwargs):
    return _stub('AccountMasterController', 'groups', request)

def account_master__api_groups(request, *args, **kwargs):
    return _stub('AccountMasterController', 'apiGroups', request)

def account_master__bs_heads(request, *args, **kwargs):
    return _stub('AccountMasterController', 'bsHeads', request)

def account_master__api_b_s_heads(request, *args, **kwargs):
    return _stub('AccountMasterController', 'apiBSHeads', request)

def account_master__position_settings(request, *args, **kwargs):
    return _stub('AccountMasterController', 'positionSettings', request)

def account_master__api_positions(request, *args, **kwargs):
    return _stub('AccountMasterController', 'apiPositions', request)

def account_master__book_stock(request, *args, **kwargs):
    return _stub('AccountMasterController', 'bookStock', request)

def account_master__op_stock_value_set(request, *args, **kwargs):
    return _stub('AccountMasterController', 'opStockValueSet', request)

def account_master__co_party_limit(request, *args, **kwargs):
    return _stub('AccountMasterController', 'coPartyLimit', request)

def account_master__api_co_party_limit(request, *args, **kwargs):
    return _stub('AccountMasterController', 'apiCoPartyLimit', request)

def account_master__sales_man(request, *args, **kwargs):
    return _stub('AccountMasterController', 'salesMan', request)

def account_master__api_sales_man(request, *args, **kwargs):
    return _stub('AccountMasterController', 'apiSalesMan', request)


# ---- AccountRestartDateController ----
def account_restart_date__index(request, *args, **kwargs):
    return _stub('AccountRestartDateController', 'index', request)

def account_restart_date__load_account(request, *args, **kwargs):
    return _stub('AccountRestartDateController', 'loadAccount', request)

def account_restart_date__search_account(request, *args, **kwargs):
    return _stub('AccountRestartDateController', 'searchAccount', request)

def account_restart_date__save(request, *args, **kwargs):
    return _stub('AccountRestartDateController', 'save', request)


# ---- AdminController ----
def admin__users(request, *args, **kwargs):
    return _stub('AdminController', 'users', request)

def admin__add_user(request, *args, **kwargs):
    return _stub('AdminController', 'addUser', request)

def admin__edit_user(request, *args, **kwargs):
    return _stub('AdminController', 'editUser', request)

def admin__delete_user(request, *args, **kwargs):
    return _stub('AdminController', 'deleteUser', request)

def admin__user_permissions(request, *args, **kwargs):
    return _stub('AdminController', 'userPermissions', request)

def admin__user_history(request, *args, **kwargs):
    return _stub('AdminController', 'userHistory', request)


# ---- AdministrationController ----
def administration__index(request, *args, **kwargs):
    return _stub('AdministrationController', 'index', request)

def administration__initialise(request, *args, **kwargs):
    return _stub('AdministrationController', 'initialise', request)

def administration__initialise_doc_no(request, *args, **kwargs):
    return _stub('AdministrationController', 'initialiseDocNo', request)

def administration__add_slno(request, *args, **kwargs):
    return _stub('AdministrationController', 'addSlno', request)

def administration__sql_update(request, *args, **kwargs):
    return _stub('AdministrationController', 'sqlUpdate', request)

def administration__stock_update(request, *args, **kwargs):
    return _stub('AdministrationController', 'stockUpdate', request)

def administration__data_transfer(request, *args, **kwargs):
    return _stub('AdministrationController', 'dataTransfer', request)

def administration__update_log(request, *args, **kwargs):
    return _stub('AdministrationController', 'updateLog', request)

def administration__change_doc_no(request, *args, **kwargs):
    return _stub('AdministrationController', 'changeDocNo', request)

def administration__rearrange_doc_nos(request, *args, **kwargs):
    return _stub('AdministrationController', 'rearrangeDocNos', request)

def administration__run_initialise(request, *args, **kwargs):
    return _stub('AdministrationController', 'runInitialise', request)

def administration__run_initialise_doc_no(request, *args, **kwargs):
    return _stub('AdministrationController', 'runInitialiseDocNo', request)

def administration__run_add_slno(request, *args, **kwargs):
    return _stub('AdministrationController', 'runAddSlno', request)

def administration__run_sql_update(request, *args, **kwargs):
    return _stub('AdministrationController', 'runSqlUpdate', request)

def administration__data_transfer_preview(request, *args, **kwargs):
    return _stub('AdministrationController', 'dataTransferPreview', request)

def administration__data_transfer_run(request, *args, **kwargs):
    return _stub('AdministrationController', 'dataTransferRun', request)

def administration__update_log_data(request, *args, **kwargs):
    return _stub('AdministrationController', 'updateLogData', request)

def administration__clear_update_log(request, *args, **kwargs):
    return _stub('AdministrationController', 'clearUpdateLog', request)

def administration__run_change_doc_no(request, *args, **kwargs):
    return _stub('AdministrationController', 'runChangeDocNo', request)

def administration__run_rearrange_doc_nos(request, *args, **kwargs):
    return _stub('AdministrationController', 'runRearrangeDocNos', request)


# ---- AiInsightsController ----
def ai_insights__index(request, *args, **kwargs):
    return _stub('AiInsightsController', 'index', request)

def ai_insights__fraud_alerts(request, *args, **kwargs):
    return _stub('AiInsightsController', 'fraudAlerts', request)

def ai_insights__customer_analytics(request, *args, **kwargs):
    return _stub('AiInsightsController', 'customerAnalytics', request)

def ai_insights__inventory_prediction(request, *args, **kwargs):
    return _stub('AiInsightsController', 'inventoryPrediction', request)

def ai_insights__business_insights(request, *args, **kwargs):
    return _stub('AiInsightsController', 'businessInsights', request)

def ai_insights__sales_cash_flow_forecast(request, *args, **kwargs):
    return _stub('AiInsightsController', 'salesCashFlowForecast', request)

def ai_insights__sales_assistant(request, *args, **kwargs):
    return _stub('AiInsightsController', 'salesAssistant', request)

def ai_insights__order_predictions(request, *args, **kwargs):
    return _stub('AiInsightsController', 'orderPredictions', request)

def ai_insights__customer_followup(request, *args, **kwargs):
    return _stub('AiInsightsController', 'customerFollowup', request)

def ai_insights__stock_recommendations(request, *args, **kwargs):
    return _stub('AiInsightsController', 'stockRecommendations', request)

def ai_insights__report_assistant(request, *args, **kwargs):
    return _stub('AiInsightsController', 'reportAssistant', request)

def ai_insights__chatbot(request, *args, **kwargs):
    return _stub('AiInsightsController', 'chatbot', request)


# ---- AllTransReportController ----
def all_trans_report__index(request, *args, **kwargs):
    return _stub('AllTransReportController', 'index', request)


# ---- AmtWgtTransferController ----
def amt_wgt_transfer__index(request, *args, **kwargs):
    return _stub('AmtWgtTransferController', 'index', request)

def amt_wgt_transfer__init(request, *args, **kwargs):
    return _stub('AmtWgtTransferController', 'init', request)

def amt_wgt_transfer__load_party(request, *args, **kwargs):
    return _stub('AmtWgtTransferController', 'loadParty', request)

def amt_wgt_transfer__search_party(request, *args, **kwargs):
    return _stub('AmtWgtTransferController', 'searchParty', request)

def amt_wgt_transfer__save(request, *args, **kwargs):
    return _stub('AmtWgtTransferController', 'save', request)


# ---- ApplicationSettingsController ----
def application_settings__index(request, *args, **kwargs):
    return _stub('ApplicationSettingsController', 'index', request)

def application_settings__load(request, *args, **kwargs):
    return _stub('ApplicationSettingsController', 'load', request)

def application_settings__save(request, *args, **kwargs):
    return _stub('ApplicationSettingsController', 'save', request)

def application_settings__upload_logo(request, *args, **kwargs):
    return _stub('ApplicationSettingsController', 'uploadLogo', request)

def application_settings__remove_logo(request, *args, **kwargs):
    return _stub('ApplicationSettingsController', 'removeLogo', request)


# ---- BackupController ----
def backup__index(request, *args, **kwargs):
    return _stub('BackupController', 'index', request)

def backup__run_backup(request, *args, **kwargs):
    return _stub('BackupController', 'runBackup', request)

def backup__run_local_disk_backup(request, *args, **kwargs):
    return _stub('BackupController', 'runLocalDiskBackup', request)

def backup__run_browser_local_disk_backup(request, *args, **kwargs):
    return _stub('BackupController', 'runBrowserLocalDiskBackup', request)

def backup__browse_local_disk_path(request, *args, **kwargs):
    return _stub('BackupController', 'browseLocalDiskPath', request)

def backup__save_local_disk_path(request, *args, **kwargs):
    return _stub('BackupController', 'saveLocalDiskPath', request)

def backup__download(request, *args, **kwargs):
    return _stub('BackupController', 'download', request)

def backup__delete(request, *args, **kwargs):
    return _stub('BackupController', 'delete', request)

def backup__save_auto_settings(request, *args, **kwargs):
    return _stub('BackupController', 'saveAutoSettings', request)


# ---- BankBookController ----
def bank_book__index(request, *args, **kwargs):
    return _stub('BankBookController', 'index', request)


# ---- BarcodeEntryComparisonController ----
def barcode_entry_comparison__index(request, *args, **kwargs):
    return _stub('BarcodeEntryComparisonController', 'index', request)


# ---- BarcodeEntryController ----
def barcode_entry__index(request, *args, **kwargs):
    return _stub('BarcodeEntryController', 'index', request)

def barcode_entry__get(request, *args, **kwargs):
    return _stub('BarcodeEntryController', 'get', request)

def barcode_entry__save(request, *args, **kwargs):
    return _stub('BarcodeEntryController', 'save', request)

def barcode_entry__delete(request, *args, **kwargs):
    return _stub('BarcodeEntryController', 'delete', request)

def barcode_entry__print_barcode(request, *args, **kwargs):
    return _stub('BarcodeEntryController', 'printBarcode', request)

def barcode_entry__print_sample(request, *args, **kwargs):
    return _stub('BarcodeEntryController', 'printSample', request)

def barcode_entry__search(request, *args, **kwargs):
    return _stub('BarcodeEntryController', 'search', request)

def barcode_entry__next_barcode(request, *args, **kwargs):
    return _stub('BarcodeEntryController', 'nextBarcode', request)

def barcode_entry__next_doc_no(request, *args, **kwargs):
    return _stub('BarcodeEntryController', 'nextDocNo', request)

def barcode_entry__load_item(request, *args, **kwargs):
    return _stub('BarcodeEntryController', 'loadItem', request)

def barcode_entry__load_document(request, *args, **kwargs):
    return _stub('BarcodeEntryController', 'loadDocument', request)

def barcode_entry__lookups(request, *args, **kwargs):
    return _stub('BarcodeEntryController', 'lookups', request)

def barcode_entry__action(request, *args, **kwargs):
    return _stub('BarcodeEntryController', 'action', request)


# ---- BarcodeHistoryController ----
def barcode_history__index(request, *args, **kwargs):
    return _stub('BarcodeHistoryController', 'index', request)


# ---- BarcodeListController ----
def barcode_list__index(request, *args, **kwargs):
    return _stub('BarcodeListController', 'index', request)


# ---- BarcodeMultiEntryController ----
def barcode_multi_entry__index(request, *args, **kwargs):
    return _stub('BarcodeMultiEntryController', 'index', request)

def barcode_multi_entry__next_barcode(request, *args, **kwargs):
    return _stub('BarcodeMultiEntryController', 'nextBarcode', request)

def barcode_multi_entry__next_doc_no(request, *args, **kwargs):
    return _stub('BarcodeMultiEntryController', 'nextDocNo', request)

def barcode_multi_entry__load_item(request, *args, **kwargs):
    return _stub('BarcodeMultiEntryController', 'loadItem', request)

def barcode_multi_entry__save(request, *args, **kwargs):
    return _stub('BarcodeMultiEntryController', 'save', request)

def barcode_multi_entry__delete_barcode(request, *args, **kwargs):
    return _stub('BarcodeMultiEntryController', 'deleteBarcode', request)

def barcode_multi_entry__load_document(request, *args, **kwargs):
    return _stub('BarcodeMultiEntryController', 'loadDocument', request)


# ---- BarcodeSamtListController ----
def barcode_samt_list__index(request, *args, **kwargs):
    return _stub('BarcodeSamtListController', 'index', request)


# ---- BarcodeSettingsController ----
def barcode_settings__index(request, *args, **kwargs):
    return _stub('BarcodeSettingsController', 'index', request)

def barcode_settings__get(request, *args, **kwargs):
    return _stub('BarcodeSettingsController', 'get', request)

def barcode_settings__printers(request, *args, **kwargs):
    return _stub('BarcodeSettingsController', 'printers', request)

def barcode_settings__images(request, *args, **kwargs):
    return _stub('BarcodeSettingsController', 'images', request)

def barcode_settings__upload_image(request, *args, **kwargs):
    return _stub('BarcodeSettingsController', 'uploadImage', request)

def barcode_settings__set_default_printer(request, *args, **kwargs):
    return _stub('BarcodeSettingsController', 'setDefaultPrinter', request)

def barcode_settings__save(request, *args, **kwargs):
    return _stub('BarcodeSettingsController', 'save', request)


# ---- BarcodeStockListController ----
def barcode_stock_list__index(request, *args, **kwargs):
    return _stub('BarcodeStockListController', 'index', request)


# ---- BarcodeStockVerifyController ----
def barcode_stock_verify__index(request, *args, **kwargs):
    return _stub('BarcodeStockVerifyController', 'index', request)


# ---- BillPrefixController ----
def bill_prefix__index(request, *args, **kwargs):
    return _stub('BillPrefixController', 'index', request)

def bill_prefix__retrieve(request, *args, **kwargs):
    return _stub('BillPrefixController', 'retrieve', request)

def bill_prefix__save(request, *args, **kwargs):
    return _stub('BillPrefixController', 'save', request)

def bill_prefix__check_delete(request, *args, **kwargs):
    return _stub('BillPrefixController', 'checkDelete', request)


# ---- CashBalanceController ----
def cash_balance__index(request, *args, **kwargs):
    return _stub('CashBalanceController', 'index', request)


# ---- CashBookController ----
def cash_book__index(request, *args, **kwargs):
    return _stub('CashBookController', 'index', request)


# ---- ChangeDuedateController ----
def change_duedate__index(request, *args, **kwargs):
    return _stub('ChangeDuedateController', 'index', request)

def change_duedate__load_party(request, *args, **kwargs):
    return _stub('ChangeDuedateController', 'loadParty', request)

def change_duedate__search_party(request, *args, **kwargs):
    return _stub('ChangeDuedateController', 'searchParty', request)

def change_duedate__save(request, *args, **kwargs):
    return _stub('ChangeDuedateController', 'save', request)


# ---- ChartOfAccountsController ----
def chart_of_accounts__index(request, *args, **kwargs):
    return _stub('ChartOfAccountsController', 'index', request)


# ---- CompanySelectController ----
def company_select__index(request, *args, **kwargs):
    return _stub('CompanySelectController', 'index', request)

def company_select__save(request, *args, **kwargs):
    return _stub('CompanySelectController', 'save', request)

def company_select__delete(request, *args, **kwargs):
    return _stub('CompanySelectController', 'delete', request)

def company_select__switch(request, *args, **kwargs):
    return _stub('CompanySelectController', 'switch', request)

def company_select__set_default(request, *args, **kwargs):
    return _stub('CompanySelectController', 'setDefault', request)

def company_select__close(request, *args, **kwargs):
    return _stub('CompanySelectController', 'close', request)


# ---- CounterIssueController ----
def counter_issue__index(request, *args, **kwargs):
    return _stub('CounterIssueController', 'index', request)

def counter_issue__load_items(request, *args, **kwargs):
    return _stub('CounterIssueController', 'loadItems', request)

def counter_issue__lookup_barcode(request, *args, **kwargs):
    return _stub('CounterIssueController', 'lookupBarcode', request)

def counter_issue__update_counter(request, *args, **kwargs):
    return _stub('CounterIssueController', 'updateCounter', request)

def counter_issue__refresh_counter(request, *args, **kwargs):
    return _stub('CounterIssueController', 'refreshCounter', request)


# ---- CountersController ----
def counters__index(request, *args, **kwargs):
    return _stub('CountersController', 'index', request)

def counters__save(request, *args, **kwargs):
    return _stub('CountersController', 'save', request)

def counters__delete(request, *args, **kwargs):
    return _stub('CountersController', 'delete', request)


# ---- CountryCurrencyController ----
def country_currency__index(request, *args, **kwargs):
    return _stub('CountryCurrencyController', 'index', request)

def country_currency__load(request, *args, **kwargs):
    return _stub('CountryCurrencyController', 'load', request)

def country_currency__save(request, *args, **kwargs):
    return _stub('CountryCurrencyController', 'save', request)

def country_currency__config_api(request, *args, **kwargs):
    return _stub('CountryCurrencyController', 'configApi', request)


# ---- CustomerBillwiseRcptController ----
def customer_billwise_rcpt__index(request, *args, **kwargs):
    return _stub('CustomerBillwiseRcptController', 'index', request)

def customer_billwise_rcpt__api(request, *args, **kwargs):
    return _stub('CustomerBillwiseRcptController', 'api', request)


# ---- CustomerCampaignController ----
def customer_campaign__index(request, *args, **kwargs):
    return _stub('CustomerCampaignController', 'index', request)

def customer_campaign__recipients(request, *args, **kwargs):
    return _stub('CustomerCampaignController', 'recipients', request)


# ---- CustomerOpBillsController ----
def customer_op_bills__index(request, *args, **kwargs):
    return _stub('CustomerOpBillsController', 'index', request)

def customer_op_bills__lookup_customer(request, *args, **kwargs):
    return _stub('CustomerOpBillsController', 'lookupCustomer', request)

def customer_op_bills__retrieve_bills(request, *args, **kwargs):
    return _stub('CustomerOpBillsController', 'retrieveBills', request)

def customer_op_bills__search_customers(request, *args, **kwargs):
    return _stub('CustomerOpBillsController', 'searchCustomers', request)

def customer_op_bills__save(request, *args, **kwargs):
    return _stub('CustomerOpBillsController', 'save', request)


# ---- CustomerPopupController ----
def customer_popup__routes_page(request, *args, **kwargs):
    return _stub('CustomerPopupController', 'routesPage', request)

def customer_popup__routes_retrieve(request, *args, **kwargs):
    return _stub('CustomerPopupController', 'routesRetrieve', request)

def customer_popup__routes_save(request, *args, **kwargs):
    return _stub('CustomerPopupController', 'routesSave', request)

def customer_popup__area_page(request, *args, **kwargs):
    return _stub('CustomerPopupController', 'areaPage', request)

def customer_popup__area_retrieve(request, *args, **kwargs):
    return _stub('CustomerPopupController', 'areaRetrieve', request)

def customer_popup__area_save(request, *args, **kwargs):
    return _stub('CustomerPopupController', 'areaSave', request)

def customer_popup__pcard_page(request, *args, **kwargs):
    return _stub('CustomerPopupController', 'pcardPage', request)

def customer_popup__pcard_retrieve(request, *args, **kwargs):
    return _stub('CustomerPopupController', 'pcardRetrieve', request)

def customer_popup__pcard_save(request, *args, **kwargs):
    return _stub('CustomerPopupController', 'pcardSave', request)

def customer_popup__advanced_page(request, *args, **kwargs):
    return _stub('CustomerPopupController', 'advancedPage', request)


# ---- CustomerReportsController ----
def customer_reports__credit_bill_index(request, *args, **kwargs):
    return _stub('CustomerReportsController', 'creditBillIndex', request)

def customer_reports__credit_bill_data(request, *args, **kwargs):
    return _stub('CustomerReportsController', 'creditBillData', request)

def customer_reports__summary_index(request, *args, **kwargs):
    return _stub('CustomerReportsController', 'summaryIndex', request)

def customer_reports__summary_data(request, *args, **kwargs):
    return _stub('CustomerReportsController', 'summaryData', request)

def customer_reports__received_index(request, *args, **kwargs):
    return _stub('CustomerReportsController', 'receivedIndex', request)

def customer_reports__received_data(request, *args, **kwargs):
    return _stub('CustomerReportsController', 'receivedData', request)

def customer_reports__payment_index(request, *args, **kwargs):
    return _stub('CustomerReportsController', 'paymentIndex', request)

def customer_reports__payment_data(request, *args, **kwargs):
    return _stub('CustomerReportsController', 'paymentData', request)

def customer_reports__sales_summary_index(request, *args, **kwargs):
    return _stub('CustomerReportsController', 'salesSummaryIndex', request)

def customer_reports__sales_summary_data(request, *args, **kwargs):
    return _stub('CustomerReportsController', 'salesSummaryData', request)

def customer_reports__billwise_details_index(request, *args, **kwargs):
    return _stub('CustomerReportsController', 'billwiseDetailsIndex', request)

def customer_reports__billwise_details_data(request, *args, **kwargs):
    return _stub('CustomerReportsController', 'billwiseDetailsData', request)

def customer_reports__bill_collection_index(request, *args, **kwargs):
    return _stub('CustomerReportsController', 'billCollectionIndex', request)

def customer_reports__bill_collection_data(request, *args, **kwargs):
    return _stub('CustomerReportsController', 'billCollectionData', request)

def customer_reports__duedate_index(request, *args, **kwargs):
    return _stub('CustomerReportsController', 'duedateIndex', request)

def customer_reports__duedate_data(request, *args, **kwargs):
    return _stub('CustomerReportsController', 'duedateData', request)

def customer_reports__party_history_index(request, *args, **kwargs):
    return _stub('CustomerReportsController', 'partyHistoryIndex', request)

def customer_reports__party_history_data(request, *args, **kwargs):
    return _stub('CustomerReportsController', 'partyHistoryData', request)

def customer_reports__visit_report_index(request, *args, **kwargs):
    return _stub('CustomerReportsController', 'visitReportIndex', request)

def customer_reports__visit_report_data(request, *args, **kwargs):
    return _stub('CustomerReportsController', 'visitReportData', request)

def customer_reports__customer_list_index(request, *args, **kwargs):
    return _stub('CustomerReportsController', 'customerListIndex', request)

def customer_reports__customer_list_data(request, *args, **kwargs):
    return _stub('CustomerReportsController', 'customerListData', request)


# ---- DayBookController ----
def day_book__index(request, *args, **kwargs):
    return _stub('DayBookController', 'index', request)


# ---- DebitCreditNoteController ----
def debit_credit_note__index(request, *args, **kwargs):
    return _stub('DebitCreditNoteController', 'index', request)

def debit_credit_note__api(request, *args, **kwargs):
    return _stub('DebitCreditNoteController', 'api', request)


# ---- DenominationEntryController ----
def denomination_entry__index(request, *args, **kwargs):
    return _stub('DenominationEntryController', 'index', request)

def denomination_entry__load(request, *args, **kwargs):
    return _stub('DenominationEntryController', 'load', request)

def denomination_entry__save(request, *args, **kwargs):
    return _stub('DenominationEntryController', 'save', request)


# ---- DenominationMasterController ----
def denomination_master__index(request, *args, **kwargs):
    return _stub('DenominationMasterController', 'index', request)

def denomination_master__retrieve(request, *args, **kwargs):
    return _stub('DenominationMasterController', 'retrieve', request)

def denomination_master__save(request, *args, **kwargs):
    return _stub('DenominationMasterController', 'save', request)

def denomination_master__check_ref(request, *args, **kwargs):
    return _stub('DenominationMasterController', 'checkRef', request)


# ---- DepositReportController ----
def deposit_report__transactions(request, *args, **kwargs):
    return _stub('DepositReportController', 'transactions', request)

def deposit_report__transactions_data(request, *args, **kwargs):
    return _stub('DepositReportController', 'transactionsData', request)

def deposit_report__depositer_ledger(request, *args, **kwargs):
    return _stub('DepositReportController', 'depositerLedger', request)

def deposit_report__depositer_ledger_data(request, *args, **kwargs):
    return _stub('DepositReportController', 'depositerLedgerData', request)

def deposit_report__wgt_amt_summary(request, *args, **kwargs):
    return _stub('DepositReportController', 'wgtAmtSummary', request)

def deposit_report__wgt_amt_summary_data(request, *args, **kwargs):
    return _stub('DepositReportController', 'wgtAmtSummaryData', request)

def deposit_report__deposit_book(request, *args, **kwargs):
    return _stub('DepositReportController', 'depositBook', request)

def deposit_report__deposit_book_data(request, *args, **kwargs):
    return _stub('DepositReportController', 'depositBookData', request)

def deposit_report__wgt_balance_summary(request, *args, **kwargs):
    return _stub('DepositReportController', 'wgtBalanceSummary', request)

def deposit_report__wgt_balance_summary_data(request, *args, **kwargs):
    return _stub('DepositReportController', 'wgtBalanceSummaryData', request)


# ---- DepositorsIntPostController ----
def depositors_int_post__index(request, *args, **kwargs):
    return _stub('DepositorsIntPostController', 'index', request)

def depositors_int_post__api(request, *args, **kwargs):
    return _stub('DepositorsIntPostController', 'api', request)


# ---- DiamondPurchaseBillController ----
def diamond_purchase_bill__picker(request, *args, **kwargs):
    return _stub('DiamondPurchaseBillController', 'picker', request)

def diamond_purchase_bill__index(request, *args, **kwargs):
    return _stub('DiamondPurchaseBillController', 'index', request)

def diamond_purchase_bill__next_bill_no(request, *args, **kwargs):
    return _stub('DiamondPurchaseBillController', 'nextBillNo', request)

def diamond_purchase_bill__supplier_search(request, *args, **kwargs):
    return _stub('DiamondPurchaseBillController', 'supplierSearch', request)

def diamond_purchase_bill__supplier_details(request, *args, **kwargs):
    return _stub('DiamondPurchaseBillController', 'supplierDetails', request)

def diamond_purchase_bill__item_lookup(request, *args, **kwargs):
    return _stub('DiamondPurchaseBillController', 'itemLookup', request)

def diamond_purchase_bill__item_search(request, *args, **kwargs):
    return _stub('DiamondPurchaseBillController', 'itemSearch', request)

def diamond_purchase_bill__recalc(request, *args, **kwargs):
    return _stub('DiamondPurchaseBillController', 'recalc', request)

def diamond_purchase_bill__save(request, *args, **kwargs):
    return _stub('DiamondPurchaseBillController', 'save', request)

def diamond_purchase_bill__get(request, *args, **kwargs):
    return _stub('DiamondPurchaseBillController', 'get', request)

def diamond_purchase_bill__prev_bill(request, *args, **kwargs):
    return _stub('DiamondPurchaseBillController', 'prevBill', request)

def diamond_purchase_bill__next_bill(request, *args, **kwargs):
    return _stub('DiamondPurchaseBillController', 'nextBill', request)

def diamond_purchase_bill__search(request, *args, **kwargs):
    return _stub('DiamondPurchaseBillController', 'search', request)

def diamond_purchase_bill__picker_search(request, *args, **kwargs):
    return _stub('DiamondPurchaseBillController', 'pickerSearch', request)

def diamond_purchase_bill__picker_resolve(request, *args, **kwargs):
    return _stub('DiamondPurchaseBillController', 'pickerResolve', request)

def diamond_purchase_bill__cancel_bill(request, *args, **kwargs):
    return _stub('DiamondPurchaseBillController', 'cancelBill', request)

def diamond_purchase_bill__reprint(request, *args, **kwargs):
    return _stub('DiamondPurchaseBillController', 'reprint', request)

def diamond_purchase_bill__create_supplier(request, *args, **kwargs):
    return _stub('DiamondPurchaseBillController', 'createSupplier', request)

def diamond_purchase_bill__rebuild_all_daybook(request, *args, **kwargs):
    return _stub('DiamondPurchaseBillController', 'rebuildAllDaybook', request)

def diamond_purchase_bill__barcode_lookup(request, *args, **kwargs):
    return _stub('DiamondPurchaseBillController', 'barcodeLookup', request)

def diamond_purchase_bill__next_barcode(request, *args, **kwargs):
    return _stub('DiamondPurchaseBillController', 'nextBarcode', request)


# ---- DiamondPurchaseReturnController ----
def diamond_purchase_return__picker(request, *args, **kwargs):
    return _stub('DiamondPurchaseReturnController', 'picker', request)

def diamond_purchase_return__index(request, *args, **kwargs):
    return _stub('DiamondPurchaseReturnController', 'index', request)

def diamond_purchase_return__next_bill_no(request, *args, **kwargs):
    return _stub('DiamondPurchaseReturnController', 'nextBillNo', request)

def diamond_purchase_return__supplier_search(request, *args, **kwargs):
    return _stub('DiamondPurchaseReturnController', 'supplierSearch', request)

def diamond_purchase_return__supplier_details(request, *args, **kwargs):
    return _stub('DiamondPurchaseReturnController', 'supplierDetails', request)

def diamond_purchase_return__item_lookup(request, *args, **kwargs):
    return _stub('DiamondPurchaseReturnController', 'itemLookup', request)

def diamond_purchase_return__item_search(request, *args, **kwargs):
    return _stub('DiamondPurchaseReturnController', 'itemSearch', request)

def diamond_purchase_return__save(request, *args, **kwargs):
    return _stub('DiamondPurchaseReturnController', 'save', request)

def diamond_purchase_return__get(request, *args, **kwargs):
    return _stub('DiamondPurchaseReturnController', 'get', request)

def diamond_purchase_return__prev_bill(request, *args, **kwargs):
    return _stub('DiamondPurchaseReturnController', 'prevBill', request)

def diamond_purchase_return__next_bill(request, *args, **kwargs):
    return _stub('DiamondPurchaseReturnController', 'nextBill', request)

def diamond_purchase_return__search(request, *args, **kwargs):
    return _stub('DiamondPurchaseReturnController', 'search', request)

def diamond_purchase_return__picker_search(request, *args, **kwargs):
    return _stub('DiamondPurchaseReturnController', 'pickerSearch', request)

def diamond_purchase_return__picker_resolve(request, *args, **kwargs):
    return _stub('DiamondPurchaseReturnController', 'pickerResolve', request)

def diamond_purchase_return__cancel_bill(request, *args, **kwargs):
    return _stub('DiamondPurchaseReturnController', 'cancelBill', request)

def diamond_purchase_return__barcode_lookup(request, *args, **kwargs):
    return _stub('DiamondPurchaseReturnController', 'barcodeLookup', request)

def diamond_purchase_return__next_barcode(request, *args, **kwargs):
    return _stub('DiamondPurchaseReturnController', 'nextBarcode', request)


# ---- DiamondStoneStockController ----
def diamond_stone_stock__index(request, *args, **kwargs):
    return _stub('DiamondStoneStockController', 'index', request)


# ---- ExpenseVoucherEntryController ----
def expense_voucher_entry__index(request, *args, **kwargs):
    return _stub('ExpenseVoucherEntryController', 'index', request)

def expense_voucher_entry__load_bill_types(request, *args, **kwargs):
    return _stub('ExpenseVoucherEntryController', 'loadBillTypes', request)

def expense_voucher_entry__defaults(request, *args, **kwargs):
    return _stub('ExpenseVoucherEntryController', 'defaults', request)

def expense_voucher_entry__next_doc(request, *args, **kwargs):
    return _stub('ExpenseVoucherEntryController', 'nextDoc', request)

def expense_voucher_entry__lookup_party(request, *args, **kwargs):
    return _stub('ExpenseVoucherEntryController', 'lookupParty', request)

def expense_voucher_entry__search_party(request, *args, **kwargs):
    return _stub('ExpenseVoucherEntryController', 'searchParty', request)

def expense_voucher_entry__search_account(request, *args, **kwargs):
    return _stub('ExpenseVoucherEntryController', 'searchAccount', request)

def expense_voucher_entry__search(request, *args, **kwargs):
    return _stub('ExpenseVoucherEntryController', 'search', request)

def expense_voucher_entry__get(request, *args, **kwargs):
    return _stub('ExpenseVoucherEntryController', 'get', request)

def expense_voucher_entry__save(request, *args, **kwargs):
    return _stub('ExpenseVoucherEntryController', 'save', request)


# ---- GiftTableController ----
def gift_table__index(request, *args, **kwargs):
    return _stub('GiftTableController', 'index', request)

def gift_table__save(request, *args, **kwargs):
    return _stub('GiftTableController', 'save', request)


# ---- GoldRateStoryController ----
def gold_rate_story__index(request, *args, **kwargs):
    return _stub('GoldRateStoryController', 'index', request)

def gold_rate_story__data(request, *args, **kwargs):
    return _stub('GoldRateStoryController', 'data', request)


# ---- GoldsmithNewWorkNoteController ----
def goldsmith_new_work_note__list(request, *args, **kwargs):
    return _stub('GoldsmithNewWorkNoteController', 'list', request)

def goldsmith_new_work_note__save(request, *args, **kwargs):
    return _stub('GoldsmithNewWorkNoteController', 'save', request)

def goldsmith_new_work_note__delete(request, *args, **kwargs):
    return _stub('GoldsmithNewWorkNoteController', 'delete', request)


# ---- GoldsmithTransactionController ----
def goldsmith_transaction__print_view(request, *args, **kwargs):
    return _stub('GoldsmithTransactionController', 'printView', request)

def goldsmith_transaction__index(request, *args, **kwargs):
    return _stub('GoldsmithTransactionController', 'index', request)

def goldsmith_transaction__picker(request, *args, **kwargs):
    return _stub('GoldsmithTransactionController', 'picker', request)

def goldsmith_transaction__next_number(request, *args, **kwargs):
    return _stub('GoldsmithTransactionController', 'nextNumber', request)

def goldsmith_transaction__get(request, *args, **kwargs):
    return _stub('GoldsmithTransactionController', 'get', request)

def goldsmith_transaction__prev(request, *args, **kwargs):
    return _stub('GoldsmithTransactionController', 'prev', request)

def goldsmith_transaction__next(request, *args, **kwargs):
    return _stub('GoldsmithTransactionController', 'next', request)

def goldsmith_transaction__picker_search(request, *args, **kwargs):
    return _stub('GoldsmithTransactionController', 'pickerSearch', request)

def goldsmith_transaction__picker_resolve(request, *args, **kwargs):
    return _stub('GoldsmithTransactionController', 'pickerResolve', request)

def goldsmith_transaction__save(request, *args, **kwargs):
    return _stub('GoldsmithTransactionController', 'save', request)

def goldsmith_transaction__delete(request, *args, **kwargs):
    return _stub('GoldsmithTransactionController', 'delete', request)

def goldsmith_transaction__balance(request, *args, **kwargs):
    return _stub('GoldsmithTransactionController', 'balance', request)

def goldsmith_transaction__item_help(request, *args, **kwargs):
    return _stub('GoldsmithTransactionController', 'itemHelp', request)

def goldsmith_transaction__item_info(request, *args, **kwargs):
    return _stub('GoldsmithTransactionController', 'itemInfo', request)

def goldsmith_transaction__client_help(request, *args, **kwargs):
    return _stub('GoldsmithTransactionController', 'clientHelp', request)

def goldsmith_transaction__barcode_info(request, *args, **kwargs):
    return _stub('GoldsmithTransactionController', 'barcodeInfo', request)

def goldsmith_transaction__interest_posting_show(request, *args, **kwargs):
    return _stub('GoldsmithTransactionController', 'interestPostingShow', request)

def goldsmith_transaction__interest_posting_save(request, *args, **kwargs):
    return _stub('GoldsmithTransactionController', 'interestPostingSave', request)


# ---- GroupAccountSummaryController ----
def group_account_summary__index(request, *args, **kwargs):
    return _stub('GroupAccountSummaryController', 'index', request)


# ---- GroupAmtAllocationController ----
def group_amt_allocation__index(request, *args, **kwargs):
    return _stub('GroupAmtAllocationController', 'index', request)

def group_amt_allocation__groups(request, *args, **kwargs):
    return _stub('GroupAmtAllocationController', 'groups', request)

def group_amt_allocation__search_account(request, *args, **kwargs):
    return _stub('GroupAmtAllocationController', 'searchAccount', request)

def group_amt_allocation__show(request, *args, **kwargs):
    return _stub('GroupAmtAllocationController', 'show', request)

def group_amt_allocation__set_def(request, *args, **kwargs):
    return _stub('GroupAmtAllocationController', 'setDef', request)

def group_amt_allocation__save(request, *args, **kwargs):
    return _stub('GroupAmtAllocationController', 'save', request)


# ---- GroupLedgerController ----
def group_ledger__index(request, *args, **kwargs):
    return _stub('GroupLedgerController', 'index', request)


# ---- GroupwiseExpandedListController ----
def groupwise_expanded_list__index(request, *args, **kwargs):
    return _stub('GroupwiseExpandedListController', 'index', request)


# ---- ItemAdjustmentController ----
def item_adjustment__index(request, *args, **kwargs):
    return _stub('ItemAdjustmentController', 'index', request)

def item_adjustment__multi(request, *args, **kwargs):
    return _stub('ItemAdjustmentController', 'multi', request)

def item_adjustment__add_less(request, *args, **kwargs):
    return _stub('ItemAdjustmentController', 'addLess', request)

def item_adjustment__add_less_report(request, *args, **kwargs):
    return _stub('ItemAdjustmentController', 'addLessReport', request)

def item_adjustment__stock_adjustment(request, *args, **kwargs):
    return _stub('ItemAdjustmentController', 'stockAdjustment', request)

def item_adjustment__item(request, *args, **kwargs):
    return _stub('ItemAdjustmentController', 'item', request)

def item_adjustment__item_search(request, *args, **kwargs):
    return _stub('ItemAdjustmentController', 'itemSearch', request)

def item_adjustment__barcode(request, *args, **kwargs):
    return _stub('ItemAdjustmentController', 'barcode', request)

def item_adjustment__add_less_report_data(request, *args, **kwargs):
    return _stub('ItemAdjustmentController', 'addLessReportData', request)

def item_adjustment__stock_adjustment_data(request, *args, **kwargs):
    return _stub('ItemAdjustmentController', 'stockAdjustmentData', request)

def item_adjustment__save(request, *args, **kwargs):
    return _stub('ItemAdjustmentController', 'save', request)

def item_adjustment__bc_summary(request, *args, **kwargs):
    return _stub('ItemAdjustmentController', 'bcSummary', request)

def item_adjustment__save_multi(request, *args, **kwargs):
    return _stub('ItemAdjustmentController', 'saveMulti', request)

def item_adjustment__save_add_less(request, *args, **kwargs):
    return _stub('ItemAdjustmentController', 'saveAddLess', request)

def item_adjustment__save_stock_adjustment(request, *args, **kwargs):
    return _stub('ItemAdjustmentController', 'saveStockAdjustment', request)

def item_adjustment__edit_cancel(request, *args, **kwargs):
    return _stub('ItemAdjustmentController', 'editCancel', request)

def item_adjustment__report(request, *args, **kwargs):
    return _stub('ItemAdjustmentController', 'report', request)

def item_adjustment__report_data(request, *args, **kwargs):
    return _stub('ItemAdjustmentController', 'reportData', request)

def item_adjustment__list_adjustments(request, *args, **kwargs):
    return _stub('ItemAdjustmentController', 'listAdjustments', request)

def item_adjustment__update_adjustment(request, *args, **kwargs):
    return _stub('ItemAdjustmentController', 'updateAdjustment', request)

def item_adjustment__cancel_adjustment(request, *args, **kwargs):
    return _stub('ItemAdjustmentController', 'cancelAdjustment', request)


# ---- ItemGroupController ----
def item_group__index(request, *args, **kwargs):
    return _stub('ItemGroupController', 'index', request)

def item_group__save(request, *args, **kwargs):
    return _stub('ItemGroupController', 'save', request)


# ---- ItemHelpController ----
def item_help__index(request, *args, **kwargs):
    return _stub('ItemHelpController', 'index', request)


# ---- ItemMasterController ----
def item_master__index(request, *args, **kwargs):
    return _stub('ItemMasterController', 'index', request)

def item_master__options(request, *args, **kwargs):
    return _stub('ItemMasterController', 'options', request)

def item_master__search(request, *args, **kwargs):
    return _stub('ItemMasterController', 'search', request)

def item_master__get_item(request, *args, **kwargs):
    return _stub('ItemMasterController', 'getItem', request)

def item_master__save(request, *args, **kwargs):
    return _stub('ItemMasterController', 'save', request)

def item_master__delete(request, *args, **kwargs):
    return _stub('ItemMasterController', 'delete', request)


# ---- ItemMovementController ----
def item_movement__index(request, *args, **kwargs):
    return _stub('ItemMovementController', 'index', request)

def item_movement__data(request, *args, **kwargs):
    return _stub('ItemMovementController', 'data', request)


# ---- ItemPurityTypeController ----
def item_purity_type__index(request, *args, **kwargs):
    return _stub('ItemPurityTypeController', 'index', request)

def item_purity_type__save(request, *args, **kwargs):
    return _stub('ItemPurityTypeController', 'save', request)

def item_purity_type__check_delete(request, *args, **kwargs):
    return _stub('ItemPurityTypeController', 'checkDelete', request)


# ---- ItemReportsController ----
def item_reports__item_rate(request, *args, **kwargs):
    return _stub('ItemReportsController', 'itemRate', request)

def item_reports__cost_list(request, *args, **kwargs):
    return _stub('ItemReportsController', 'costList', request)

def item_reports__rate_history(request, *args, **kwargs):
    return _stub('ItemReportsController', 'rateHistory', request)

def item_reports__model_transfer(request, *args, **kwargs):
    return _stub('ItemReportsController', 'modelTransfer', request)

def item_reports__stone_trans_analysis(request, *args, **kwargs):
    return _stub('ItemReportsController', 'stoneTransAnalysis', request)

def item_reports__trans_ra(request, *args, **kwargs):
    return _stub('ItemReportsController', 'transRa', request)

def item_reports__item_stock_party_wgt(request, *args, **kwargs):
    return _stub('ItemReportsController', 'itemStockPartyWgt', request)

def item_reports__item_rate_data(request, *args, **kwargs):
    return _stub('ItemReportsController', 'itemRateData', request)

def item_reports__cost_list_data(request, *args, **kwargs):
    return _stub('ItemReportsController', 'costListData', request)

def item_reports__rate_history_data(request, *args, **kwargs):
    return _stub('ItemReportsController', 'rateHistoryData', request)

def item_reports__model_transfer_data(request, *args, **kwargs):
    return _stub('ItemReportsController', 'modelTransferData', request)

def item_reports__stone_trans_data(request, *args, **kwargs):
    return _stub('ItemReportsController', 'stoneTransData', request)

def item_reports__trans_ra_data(request, *args, **kwargs):
    return _stub('ItemReportsController', 'transRaData', request)

def item_reports__item_stock_party_wgt_data(request, *args, **kwargs):
    return _stub('ItemReportsController', 'itemStockPartyWgtData', request)


# ---- ItemSubGroupController ----
def item_sub_group__index(request, *args, **kwargs):
    return _stub('ItemSubGroupController', 'index', request)

def item_sub_group__save(request, *args, **kwargs):
    return _stub('ItemSubGroupController', 'save', request)

def item_sub_group__delete(request, *args, **kwargs):
    return _stub('ItemSubGroupController', 'delete', request)


# ---- ItemTempController ----
def item_temp__index(request, *args, **kwargs):
    return _stub('ItemTempController', 'index', request)

def item_temp__save(request, *args, **kwargs):
    return _stub('ItemTempController', 'save', request)

def item_temp__delete(request, *args, **kwargs):
    return _stub('ItemTempController', 'delete', request)

def item_temp__item_details(request, *args, **kwargs):
    return _stub('ItemTempController', 'itemDetails', request)

def item_temp__check_duplicate(request, *args, **kwargs):
    return _stub('ItemTempController', 'checkDuplicate', request)

def item_temp__check_delete(request, *args, **kwargs):
    return _stub('ItemTempController', 'checkDelete', request)


# ---- ItemwiseProfitController ----
def itemwise_profit__index(request, *args, **kwargs):
    return _stub('ItemwiseProfitController', 'index', request)

def itemwise_profit__data(request, *args, **kwargs):
    return _stub('ItemwiseProfitController', 'data', request)


# ---- JournalReportController ----
def journal_report__index(request, *args, **kwargs):
    return _stub('JournalReportController', 'index', request)


# ---- KuriFinishController ----
def kuri_finish__close_scheme(request, *args, **kwargs):
    return _stub('KuriFinishController', 'closeScheme', request)

def kuri_finish__draw(request, *args, **kwargs):
    return _stub('KuriFinishController', 'draw', request)

def kuri_finish__refund(request, *args, **kwargs):
    return _stub('KuriFinishController', 'refund', request)

def kuri_finish__api(request, *args, **kwargs):
    return _stub('KuriFinishController', 'api', request)


# ---- KuriIntPostController ----
def kuri_int_post__index(request, *args, **kwargs):
    return _stub('KuriIntPostController', 'index', request)

def kuri_int_post__api(request, *args, **kwargs):
    return _stub('KuriIntPostController', 'api', request)


# ---- MCTableController ----
def m_c_table__index(request, *args, **kwargs):
    return _stub('MCTableController', 'index', request)

def m_c_table__get_item(request, *args, **kwargs):
    return _stub('MCTableController', 'getItem', request)

def m_c_table__get_m_c_table(request, *args, **kwargs):
    return _stub('MCTableController', 'getMCTable', request)

def m_c_table__get_item_types(request, *args, **kwargs):
    return _stub('MCTableController', 'getItemTypes', request)

def m_c_table__save(request, *args, **kwargs):
    return _stub('MCTableController', 'save', request)

def m_c_table__delete_all(request, *args, **kwargs):
    return _stub('MCTableController', 'deleteAll', request)

def m_c_table__find_m_c_for_weight(request, *args, **kwargs):
    return _stub('MCTableController', 'findMCForWeight', request)

def m_c_table__get_items_list(request, *args, **kwargs):
    return _stub('MCTableController', 'getItemsList', request)


# ---- ModelMasterController ----
def model_master__index(request, *args, **kwargs):
    return _stub('ModelMasterController', 'index', request)

def model_master__save(request, *args, **kwargs):
    return _stub('ModelMasterController', 'save', request)

def model_master__delete(request, *args, **kwargs):
    return _stub('ModelMasterController', 'delete', request)

def model_master__check_duplicate(request, *args, **kwargs):
    return _stub('ModelMasterController', 'checkDuplicate', request)

def model_master__get_by_type(request, *args, **kwargs):
    return _stub('ModelMasterController', 'getByType', request)


# ---- NativeAuthController ----
def native_auth__show_login(request, *args, **kwargs):
    return _stub('NativeAuthController', 'showLogin', request)

def native_auth__login(request, *args, **kwargs):
    return _stub('NativeAuthController', 'login', request)

def native_auth__logout(request, *args, **kwargs):
    return _stub('NativeAuthController', 'logout', request)


# ---- NativeCustomerController ----
def native_customer__index(request, *args, **kwargs):
    return _stub('NativeCustomerController', 'index', request)

def native_customer__add(request, *args, **kwargs):
    return _stub('NativeCustomerController', 'add', request)

def native_customer__edit(request, *args, **kwargs):
    return _stub('NativeCustomerController', 'edit', request)

def native_customer__delete_page(request, *args, **kwargs):
    return _stub('NativeCustomerController', 'deletePage', request)

def native_customer__picture(request, *args, **kwargs):
    return _stub('NativeCustomerController', 'picture', request)

def native_customer__check_phone(request, *args, **kwargs):
    return _stub('NativeCustomerController', 'checkPhone', request)

def native_customer__check_id_no(request, *args, **kwargs):
    return _stub('NativeCustomerController', 'checkIdNo', request)

def native_customer__next_code(request, *args, **kwargs):
    return _stub('NativeCustomerController', 'nextCode', request)

def native_customer__get(request, *args, **kwargs):
    return _stub('NativeCustomerController', 'get', request)

def native_customer__save(request, *args, **kwargs):
    return _stub('NativeCustomerController', 'save', request)

def native_customer__delete(request, *args, **kwargs):
    return _stub('NativeCustomerController', 'delete', request)

def native_customer__import_csv(request, *args, **kwargs):
    return _stub('NativeCustomerController', 'importCsv', request)

def native_customer__sync_list(request, *args, **kwargs):
    return _stub('NativeCustomerController', 'syncList', request)


# ---- NativeDashboardController ----
def native_dashboard__index(request, *args, **kwargs):
    return _stub('NativeDashboardController', 'index', request)


# ---- NativeStatesController ----
def native_states__index(request, *args, **kwargs):
    return _stub('NativeStatesController', 'index', request)

def native_states__api(request, *args, **kwargs):
    return _stub('NativeStatesController', 'api', request)


# ---- NonTransactionalDaysReportController ----
def non_transactional_days_report__index(request, *args, **kwargs):
    return _stub('NonTransactionalDaysReportController', 'index', request)


# ---- OrderAdvanceAfterController ----
def order_advance_after__index(request, *args, **kwargs):
    return _stub('OrderAdvanceAfterController', 'index', request)

def order_advance_after__order_search(request, *args, **kwargs):
    return _stub('OrderAdvanceAfterController', 'orderSearch', request)

def order_advance_after__order_lookup(request, *args, **kwargs):
    return _stub('OrderAdvanceAfterController', 'orderLookup', request)

def order_advance_after__item_lookup(request, *args, **kwargs):
    return _stub('OrderAdvanceAfterController', 'itemLookup', request)

def order_advance_after__item_search(request, *args, **kwargs):
    return _stub('OrderAdvanceAfterController', 'itemSearch', request)

def order_advance_after__save(request, *args, **kwargs):
    return _stub('OrderAdvanceAfterController', 'save', request)

def order_advance_after__get(request, *args, **kwargs):
    return _stub('OrderAdvanceAfterController', 'get', request)

def order_advance_after__search(request, *args, **kwargs):
    return _stub('OrderAdvanceAfterController', 'search', request)

def order_advance_after__delete(request, *args, **kwargs):
    return _stub('OrderAdvanceAfterController', 'delete', request)

def order_advance_after__prev_bill(request, *args, **kwargs):
    return _stub('OrderAdvanceAfterController', 'prevBill', request)

def order_advance_after__next_bill(request, *args, **kwargs):
    return _stub('OrderAdvanceAfterController', 'nextBill', request)


# ---- OrderAdvanceReportController ----
def order_advance_report__index(request, *args, **kwargs):
    return _stub('OrderAdvanceReportController', 'index', request)


# ---- OrderBillController ----
def order_bill__edit_picker(request, *args, **kwargs):
    return _stub('OrderBillController', 'editPicker', request)

def order_bill__search_edit_orders(request, *args, **kwargs):
    return _stub('OrderBillController', 'searchEditOrders', request)

def order_bill__resolve_order_action(request, *args, **kwargs):
    return _stub('OrderBillController', 'resolveOrderAction', request)

def order_bill__print_view(request, *args, **kwargs):
    return _stub('OrderBillController', 'printView', request)

def order_bill__index(request, *args, **kwargs):
    return _stub('OrderBillController', 'index', request)

def order_bill__next_bill_no(request, *args, **kwargs):
    return _stub('OrderBillController', 'nextBillNo', request)

def order_bill__customer_search(request, *args, **kwargs):
    return _stub('OrderBillController', 'customerSearch', request)

def order_bill__customer_details(request, *args, **kwargs):
    return _stub('OrderBillController', 'customerDetails', request)

def order_bill__item_lookup(request, *args, **kwargs):
    return _stub('OrderBillController', 'itemLookup', request)

def order_bill__item_search(request, *args, **kwargs):
    return _stub('OrderBillController', 'itemSearch', request)

def order_bill__recalc(request, *args, **kwargs):
    return _stub('OrderBillController', 'recalc', request)

def order_bill__save(request, *args, **kwargs):
    return _stub('OrderBillController', 'save', request)

def order_bill__get(request, *args, **kwargs):
    return _stub('OrderBillController', 'get', request)

def order_bill__prev_bill(request, *args, **kwargs):
    return _stub('OrderBillController', 'prevBill', request)

def order_bill__next_bill(request, *args, **kwargs):
    return _stub('OrderBillController', 'nextBill', request)

def order_bill__search(request, *args, **kwargs):
    return _stub('OrderBillController', 'search', request)

def order_bill__cancel_bill(request, *args, **kwargs):
    return _stub('OrderBillController', 'cancelBill', request)


# ---- OrderBlockController ----
def order_block__index(request, *args, **kwargs):
    return _stub('OrderBlockController', 'index', request)

def order_block__search_orders(request, *args, **kwargs):
    return _stub('OrderBlockController', 'searchOrders', request)

def order_block__get_order(request, *args, **kwargs):
    return _stub('OrderBlockController', 'getOrder', request)

def order_block__toggle_block(request, *args, **kwargs):
    return _stub('OrderBlockController', 'toggleBlock', request)


# ---- OrderCancelController ----
def order_cancel__index(request, *args, **kwargs):
    return _stub('OrderCancelController', 'index', request)

def order_cancel__search(request, *args, **kwargs):
    return _stub('OrderCancelController', 'search', request)

def order_cancel__apply(request, *args, **kwargs):
    return _stub('OrderCancelController', 'apply', request)


# ---- OrderEnquiryController ----
def order_enquiry__index(request, *args, **kwargs):
    return _stub('OrderEnquiryController', 'index', request)


# ---- OrderEntryReportController ----
def order_entry_report__index(request, *args, **kwargs):
    return _stub('OrderEntryReportController', 'index', request)


# ---- OrderNosListController ----
def order_nos_list__index(request, *args, **kwargs):
    return _stub('OrderNosListController', 'index', request)


# ---- OrderPendingDetailsController ----
def order_pending_details__index(request, *args, **kwargs):
    return _stub('OrderPendingDetailsController', 'index', request)


# ---- OrderPendingRegisterController ----
def order_pending_register__index(request, *args, **kwargs):
    return _stub('OrderPendingRegisterController', 'index', request)


# ---- OrderProcessController ----
def order_process__index(request, *args, **kwargs):
    return _stub('OrderProcessController', 'index', request)


# ---- OrderProfitAnalysisController ----
def order_profit_analysis__index(request, *args, **kwargs):
    return _stub('OrderProfitAnalysisController', 'index', request)


# ---- OrderRateFixController ----
def order_rate_fix__index(request, *args, **kwargs):
    return _stub('OrderRateFixController', 'index', request)

def order_rate_fix__search(request, *args, **kwargs):
    return _stub('OrderRateFixController', 'search', request)

def order_rate_fix__apply(request, *args, **kwargs):
    return _stub('OrderRateFixController', 'apply', request)


# ---- OrderReprintController ----
def order_reprint__index(request, *args, **kwargs):
    return _stub('OrderReprintController', 'index', request)

def order_reprint__search(request, *args, **kwargs):
    return _stub('OrderReprintController', 'search', request)

def order_reprint__resolve(request, *args, **kwargs):
    return _stub('OrderReprintController', 'resolve', request)


# ---- OrderReturnsController ----
def order_returns__index(request, *args, **kwargs):
    return _stub('OrderReturnsController', 'index', request)


# ---- OrderSaleController ----
def order_sale__index(request, *args, **kwargs):
    return _stub('OrderSaleController', 'index', request)

def order_sale__load_order(request, *args, **kwargs):
    return _stub('OrderSaleController', 'loadOrder', request)

def order_sale__order_search(request, *args, **kwargs):
    return _stub('OrderSaleController', 'orderSearch', request)

def order_sale__customer_details(request, *args, **kwargs):
    return _stub('OrderSaleController', 'customerDetails', request)

def order_sale__item_lookup(request, *args, **kwargs):
    return _stub('OrderSaleController', 'itemLookup', request)

def order_sale__item_search(request, *args, **kwargs):
    return _stub('OrderSaleController', 'itemSearch', request)

def order_sale__recalc(request, *args, **kwargs):
    return _stub('OrderSaleController', 'recalc', request)

def order_sale__save(request, *args, **kwargs):
    return _stub('OrderSaleController', 'save', request)

def order_sale__get(request, *args, **kwargs):
    return _stub('OrderSaleController', 'get', request)

def order_sale__search(request, *args, **kwargs):
    return _stub('OrderSaleController', 'search', request)

def order_sale__prev_bill(request, *args, **kwargs):
    return _stub('OrderSaleController', 'prevBill', request)

def order_sale__next_bill(request, *args, **kwargs):
    return _stub('OrderSaleController', 'nextBill', request)

def order_sale__cancel_bill(request, *args, **kwargs):
    return _stub('OrderSaleController', 'cancelBill', request)


# ---- OrderSampleStockController ----
def order_sample_stock__index(request, *args, **kwargs):
    return _stub('OrderSampleStockController', 'index', request)


# ---- OrderSendMailController ----
def order_send_mail__index(request, *args, **kwargs):
    return _stub('OrderSendMailController', 'index', request)

def order_send_mail__export_csv(request, *args, **kwargs):
    return _stub('OrderSendMailController', 'exportCsv', request)


# ---- OrderUpdateController ----
def order_update__index(request, *args, **kwargs):
    return _stub('OrderUpdateController', 'index', request)

def order_update__list_orders(request, *args, **kwargs):
    return _stub('OrderUpdateController', 'listOrders', request)

def order_update__import_csv(request, *args, **kwargs):
    return _stub('OrderUpdateController', 'importCsv', request)

def order_update__save_import(request, *args, **kwargs):
    return _stub('OrderUpdateController', 'saveImport', request)

def order_update__save_manual(request, *args, **kwargs):
    return _stub('OrderUpdateController', 'saveManual', request)

def order_update__delete_order(request, *args, **kwargs):
    return _stub('OrderUpdateController', 'deleteOrder', request)


# ---- OtherItemReportController ----
def other_item_report__sales_book(request, *args, **kwargs):
    return _stub('OtherItemReportController', 'salesBook', request)

def other_item_report__sales_book_data(request, *args, **kwargs):
    return _stub('OtherItemReportController', 'salesBookData', request)

def other_item_report__sales_register(request, *args, **kwargs):
    return _stub('OtherItemReportController', 'salesRegister', request)

def other_item_report__sales_register_data(request, *args, **kwargs):
    return _stub('OtherItemReportController', 'salesRegisterData', request)

def other_item_report__purchase_book(request, *args, **kwargs):
    return _stub('OtherItemReportController', 'purchaseBook', request)

def other_item_report__purchase_book_data(request, *args, **kwargs):
    return _stub('OtherItemReportController', 'purchaseBookData', request)

def other_item_report__purchase_register(request, *args, **kwargs):
    return _stub('OtherItemReportController', 'purchaseRegister', request)

def other_item_report__purchase_register_data(request, *args, **kwargs):
    return _stub('OtherItemReportController', 'purchaseRegisterData', request)

def other_item_report__stock_ledger(request, *args, **kwargs):
    return _stub('OtherItemReportController', 'stockLedger', request)

def other_item_report__stock_ledger_data(request, *args, **kwargs):
    return _stub('OtherItemReportController', 'stockLedgerData', request)

def other_item_report__stock_list(request, *args, **kwargs):
    return _stub('OtherItemReportController', 'stockList', request)

def other_item_report__stock_list_data(request, *args, **kwargs):
    return _stub('OtherItemReportController', 'stockListData', request)

def other_item_report__items_lookup(request, *args, **kwargs):
    return _stub('OtherItemReportController', 'itemsLookup', request)


# ---- OtherItemTransController ----
def other_item_trans__index(request, *args, **kwargs):
    return _stub('OtherItemTransController', 'index', request)

def other_item_trans__picker(request, *args, **kwargs):
    return _stub('OtherItemTransController', 'picker', request)

def other_item_trans__api(request, *args, **kwargs):
    return _stub('OtherItemTransController', 'api', request)


# ---- OtherItemsController ----
def other_items__index(request, *args, **kwargs):
    return _stub('OtherItemsController', 'index', request)

def other_items__help(request, *args, **kwargs):
    return _stub('OtherItemsController', 'help', request)

def other_items__lookup(request, *args, **kwargs):
    return _stub('OtherItemsController', 'lookup', request)

def other_items__add(request, *args, **kwargs):
    return _stub('OtherItemsController', 'add', request)

def other_items__edit(request, *args, **kwargs):
    return _stub('OtherItemsController', 'edit', request)

def other_items__delete(request, *args, **kwargs):
    return _stub('OtherItemsController', 'delete', request)


# ---- PartyMCTableController ----
def party_m_c_table__index(request, *args, **kwargs):
    return _stub('PartyMCTableController', 'index', request)

def party_m_c_table__get_party(request, *args, **kwargs):
    return _stub('PartyMCTableController', 'getParty', request)

def party_m_c_table__get_m_c_table(request, *args, **kwargs):
    return _stub('PartyMCTableController', 'getMCTable', request)

def party_m_c_table__get_items(request, *args, **kwargs):
    return _stub('PartyMCTableController', 'getItems', request)

def party_m_c_table__get_models(request, *args, **kwargs):
    return _stub('PartyMCTableController', 'getModels', request)

def party_m_c_table__get_parties(request, *args, **kwargs):
    return _stub('PartyMCTableController', 'getParties', request)

def party_m_c_table__save(request, *args, **kwargs):
    return _stub('PartyMCTableController', 'save', request)

def party_m_c_table__delete_entry(request, *args, **kwargs):
    return _stub('PartyMCTableController', 'deleteEntry', request)


# ---- PartyOpWeightController ----
def party_op_weight__index(request, *args, **kwargs):
    return _stub('PartyOpWeightController', 'index', request)

def party_op_weight__api(request, *args, **kwargs):
    return _stub('PartyOpWeightController', 'api', request)


# ---- PaymentConfirmationController ----
def payment_confirmation__index(request, *args, **kwargs):
    return _stub('PaymentConfirmationController', 'index', request)

def payment_confirmation__load(request, *args, **kwargs):
    return _stub('PaymentConfirmationController', 'load', request)

def payment_confirmation__confirm(request, *args, **kwargs):
    return _stub('PaymentConfirmationController', 'confirm', request)

def payment_confirmation__cancel(request, *args, **kwargs):
    return _stub('PaymentConfirmationController', 'cancel', request)


# ---- PdcReportController ----
def pdc_report__index(request, *args, **kwargs):
    return _stub('PdcReportController', 'index', request)

def pdc_report__destroy(request, *args, **kwargs):
    return _stub('PdcReportController', 'destroy', request)


# ---- PhoneBookController ----
def phone_book__index(request, *args, **kwargs):
    return _stub('PhoneBookController', 'index', request)

def phone_book__contacts(request, *args, **kwargs):
    return _stub('PhoneBookController', 'contacts', request)


# ---- PointCardController ----
def point_card__index(request, *args, **kwargs):
    return _stub('PointCardController', 'index', request)

def point_card__retrieve(request, *args, **kwargs):
    return _stub('PointCardController', 'retrieve', request)

def point_card__save(request, *args, **kwargs):
    return _stub('PointCardController', 'save', request)


# ---- PurchaseBillConfirmationController ----
def purchase_bill_confirmation__index(request, *args, **kwargs):
    return _stub('PurchaseBillConfirmationController', 'index', request)

def purchase_bill_confirmation__load(request, *args, **kwargs):
    return _stub('PurchaseBillConfirmationController', 'load', request)

def purchase_bill_confirmation__confirm(request, *args, **kwargs):
    return _stub('PurchaseBillConfirmationController', 'confirm', request)

def purchase_bill_confirmation__delete(request, *args, **kwargs):
    return _stub('PurchaseBillConfirmationController', 'delete', request)

def purchase_bill_confirmation__view(request, *args, **kwargs):
    return _stub('PurchaseBillConfirmationController', 'view', request)


# ---- PurchaseBillController ----
def purchase_bill__picker(request, *args, **kwargs):
    return _stub('PurchaseBillController', 'picker', request)

def purchase_bill__index(request, *args, **kwargs):
    return _stub('PurchaseBillController', 'index', request)

def purchase_bill__next_bill_no(request, *args, **kwargs):
    return _stub('PurchaseBillController', 'nextBillNo', request)

def purchase_bill__supplier_search(request, *args, **kwargs):
    return _stub('PurchaseBillController', 'supplierSearch', request)

def purchase_bill__supplier_details(request, *args, **kwargs):
    return _stub('PurchaseBillController', 'supplierDetails', request)

def purchase_bill__item_lookup(request, *args, **kwargs):
    return _stub('PurchaseBillController', 'itemLookup', request)

def purchase_bill__item_search(request, *args, **kwargs):
    return _stub('PurchaseBillController', 'itemSearch', request)

def purchase_bill__recalc(request, *args, **kwargs):
    return _stub('PurchaseBillController', 'recalc', request)

def purchase_bill__save(request, *args, **kwargs):
    return _stub('PurchaseBillController', 'save', request)

def purchase_bill__get(request, *args, **kwargs):
    return _stub('PurchaseBillController', 'get', request)

def purchase_bill__prev_bill(request, *args, **kwargs):
    return _stub('PurchaseBillController', 'prevBill', request)

def purchase_bill__next_bill(request, *args, **kwargs):
    return _stub('PurchaseBillController', 'nextBill', request)

def purchase_bill__search(request, *args, **kwargs):
    return _stub('PurchaseBillController', 'search', request)

def purchase_bill__picker_search(request, *args, **kwargs):
    return _stub('PurchaseBillController', 'pickerSearch', request)

def purchase_bill__picker_resolve(request, *args, **kwargs):
    return _stub('PurchaseBillController', 'pickerResolve', request)

def purchase_bill__cancel_bill(request, *args, **kwargs):
    return _stub('PurchaseBillController', 'cancelBill', request)

def purchase_bill__reprint(request, *args, **kwargs):
    return _stub('PurchaseBillController', 'reprint', request)

def purchase_bill__create_supplier(request, *args, **kwargs):
    return _stub('PurchaseBillController', 'createSupplier', request)

def purchase_bill__rebuild_all_daybook(request, *args, **kwargs):
    return _stub('PurchaseBillController', 'rebuildAllDaybook', request)


# ---- PurchaseReturnController ----
def purchase_return__picker(request, *args, **kwargs):
    return _stub('PurchaseReturnController', 'picker', request)

def purchase_return__index(request, *args, **kwargs):
    return _stub('PurchaseReturnController', 'index', request)

def purchase_return__next_bill_no(request, *args, **kwargs):
    return _stub('PurchaseReturnController', 'nextBillNo', request)

def purchase_return__supplier_search(request, *args, **kwargs):
    return _stub('PurchaseReturnController', 'supplierSearch', request)

def purchase_return__supplier_details(request, *args, **kwargs):
    return _stub('PurchaseReturnController', 'supplierDetails', request)

def purchase_return__item_lookup(request, *args, **kwargs):
    return _stub('PurchaseReturnController', 'itemLookup', request)

def purchase_return__item_search(request, *args, **kwargs):
    return _stub('PurchaseReturnController', 'itemSearch', request)

def purchase_return__recalc(request, *args, **kwargs):
    return _stub('PurchaseReturnController', 'recalc', request)

def purchase_return__save(request, *args, **kwargs):
    return _stub('PurchaseReturnController', 'save', request)

def purchase_return__get(request, *args, **kwargs):
    return _stub('PurchaseReturnController', 'get', request)

def purchase_return__prev_bill(request, *args, **kwargs):
    return _stub('PurchaseReturnController', 'prevBill', request)

def purchase_return__next_bill(request, *args, **kwargs):
    return _stub('PurchaseReturnController', 'nextBill', request)

def purchase_return__search(request, *args, **kwargs):
    return _stub('PurchaseReturnController', 'search', request)

def purchase_return__picker_search(request, *args, **kwargs):
    return _stub('PurchaseReturnController', 'pickerSearch', request)

def purchase_return__picker_resolve(request, *args, **kwargs):
    return _stub('PurchaseReturnController', 'pickerResolve', request)

def purchase_return__cancel_bill(request, *args, **kwargs):
    return _stub('PurchaseReturnController', 'cancelBill', request)

def purchase_return__reprint(request, *args, **kwargs):
    return _stub('PurchaseReturnController', 'reprint', request)


# ---- PurityCertificateController ----
def purity_certificate__index(request, *args, **kwargs):
    return _stub('PurityCertificateController', 'index', request)

def purity_certificate__api(request, *args, **kwargs):
    return _stub('PurityCertificateController', 'api', request)


# ---- PurityTestingController ----
def purity_testing__index(request, *args, **kwargs):
    return _stub('PurityTestingController', 'index', request)

def purity_testing__picker(request, *args, **kwargs):
    return _stub('PurityTestingController', 'picker', request)

def purity_testing__api(request, *args, **kwargs):
    return _stub('PurityTestingController', 'api', request)


# ---- RateController ----
def rate__index(request, *args, **kwargs):
    return _stub('RateController', 'index', request)

def rate__save(request, *args, **kwargs):
    return _stub('RateController', 'save', request)

def rate__current(request, *args, **kwargs):
    return _stub('RateController', 'current', request)

def rate__history(request, *args, **kwargs):
    return _stub('RateController', 'history', request)


# ---- RateDiffAdjustmentController ----
def rate_diff_adjustment__index(request, *args, **kwargs):
    return _stub('RateDiffAdjustmentController', 'index', request)

def rate_diff_adjustment__init(request, *args, **kwargs):
    return _stub('RateDiffAdjustmentController', 'init', request)

def rate_diff_adjustment__load_party(request, *args, **kwargs):
    return _stub('RateDiffAdjustmentController', 'loadParty', request)

def rate_diff_adjustment__search_party(request, *args, **kwargs):
    return _stub('RateDiffAdjustmentController', 'searchParty', request)

def rate_diff_adjustment__load_bill(request, *args, **kwargs):
    return _stub('RateDiffAdjustmentController', 'loadBill', request)

def rate_diff_adjustment__save(request, *args, **kwargs):
    return _stub('RateDiffAdjustmentController', 'save', request)


# ---- ReceiptPaymentReportController ----
def receipt_payment_report__index(request, *args, **kwargs):
    return _stub('ReceiptPaymentReportController', 'index', request)


# ---- RefineryBillController ----
def refinery_bill__all_in_one(request, *args, **kwargs):
    return _stub('RefineryBillController', 'allInOne', request)

def refinery_bill__picker(request, *args, **kwargs):
    return _stub('RefineryBillController', 'picker', request)

def refinery_bill__index(request, *args, **kwargs):
    return _stub('RefineryBillController', 'index', request)

def refinery_bill__refiner_lookup(request, *args, **kwargs):
    return _stub('RefineryBillController', 'refinerLookup', request)

def refinery_bill__refiner_search(request, *args, **kwargs):
    return _stub('RefineryBillController', 'refinerSearch', request)

def refinery_bill__item_lookup(request, *args, **kwargs):
    return _stub('RefineryBillController', 'itemLookup', request)

def refinery_bill__item_search(request, *args, **kwargs):
    return _stub('RefineryBillController', 'itemSearch', request)

def refinery_bill__picker_search(request, *args, **kwargs):
    return _stub('RefineryBillController', 'pickerSearch', request)

def refinery_bill__picker_resolve(request, *args, **kwargs):
    return _stub('RefineryBillController', 'pickerResolve', request)

def refinery_bill__save(request, *args, **kwargs):
    return _stub('RefineryBillController', 'save', request)

def refinery_bill__get(request, *args, **kwargs):
    return _stub('RefineryBillController', 'get', request)

def refinery_bill__search(request, *args, **kwargs):
    return _stub('RefineryBillController', 'search', request)

def refinery_bill__prev_bill(request, *args, **kwargs):
    return _stub('RefineryBillController', 'prevBill', request)

def refinery_bill__next_bill(request, *args, **kwargs):
    return _stub('RefineryBillController', 'nextBill', request)

def refinery_bill__cancel_bill(request, *args, **kwargs):
    return _stub('RefineryBillController', 'cancelBill', request)

def refinery_bill__return_index(request, *args, **kwargs):
    return _stub('RefineryBillController', 'returnIndex', request)

def refinery_bill__load_for_return(request, *args, **kwargs):
    return _stub('RefineryBillController', 'loadForReturn', request)

def refinery_bill__get_return(request, *args, **kwargs):
    return _stub('RefineryBillController', 'getReturn', request)

def refinery_bill__search_for_return(request, *args, **kwargs):
    return _stub('RefineryBillController', 'searchForReturn', request)

def refinery_bill__search_return(request, *args, **kwargs):
    return _stub('RefineryBillController', 'searchReturn', request)

def refinery_bill__save_return(request, *args, **kwargs):
    return _stub('RefineryBillController', 'saveReturn', request)

def refinery_bill__prev_return(request, *args, **kwargs):
    return _stub('RefineryBillController', 'prevReturn', request)

def refinery_bill__next_return(request, *args, **kwargs):
    return _stub('RefineryBillController', 'nextReturn', request)


# ---- RefineryReportController ----
def refinery_report__entry_report(request, *args, **kwargs):
    return _stub('RefineryReportController', 'entryReport', request)

def refinery_report__entry_report_data(request, *args, **kwargs):
    return _stub('RefineryReportController', 'entryReportData', request)

def refinery_report__refiners_summary(request, *args, **kwargs):
    return _stub('RefineryReportController', 'refinersSummary', request)

def refinery_report__refiners_summary_data(request, *args, **kwargs):
    return _stub('RefineryReportController', 'refinersSummaryData', request)

def refinery_report__analysis(request, *args, **kwargs):
    return _stub('RefineryReportController', 'analysis', request)

def refinery_report__analysis_data(request, *args, **kwargs):
    return _stub('RefineryReportController', 'analysisData', request)

def refinery_report__ac_summary(request, *args, **kwargs):
    return _stub('RefineryReportController', 'acSummary', request)

def refinery_report__ac_summary_data(request, *args, **kwargs):
    return _stub('RefineryReportController', 'acSummaryData', request)

def refinery_report__less_comparison(request, *args, **kwargs):
    return _stub('RefineryReportController', 'lessComparison', request)

def refinery_report__less_comparison_data(request, *args, **kwargs):
    return _stub('RefineryReportController', 'lessComparisonData', request)


# ---- RegionalHelpController ----
def regional_help__index(request, *args, **kwargs):
    return _stub('RegionalHelpController', 'index', request)


# ---- RemakeReportController ----
def remake_report__remake_reports(request, *args, **kwargs):
    return _stub('RemakeReportController', 'remakeReports', request)

def remake_report__remake_reports_data(request, *args, **kwargs):
    return _stub('RemakeReportController', 'remakeReportsData', request)

def remake_report__remake_pending(request, *args, **kwargs):
    return _stub('RemakeReportController', 'remakePending', request)

def remake_report__remake_pending_data(request, *args, **kwargs):
    return _stub('RemakeReportController', 'remakePendingData', request)

def remake_report__remake_returns(request, *args, **kwargs):
    return _stub('RemakeReportController', 'remakeReturns', request)

def remake_report__remake_returns_data(request, *args, **kwargs):
    return _stub('RemakeReportController', 'remakeReturnsData', request)


# ---- ReorderController ----
def reorder__index(request, *args, **kwargs):
    return _stub('ReorderController', 'index', request)

def reorder__get_item(request, *args, **kwargs):
    return _stub('ReorderController', 'getItem', request)

def reorder__save(request, *args, **kwargs):
    return _stub('ReorderController', 'save', request)

def reorder__delete_all(request, *args, **kwargs):
    return _stub('ReorderController', 'deleteAll', request)

def reorder__search_items(request, *args, **kwargs):
    return _stub('ReorderController', 'searchItems', request)


# ---- RepairComplaintsController ----
def repair_complaints__index(request, *args, **kwargs):
    return _stub('RepairComplaintsController', 'index', request)

def repair_complaints__retrieve(request, *args, **kwargs):
    return _stub('RepairComplaintsController', 'retrieve', request)

def repair_complaints__save(request, *args, **kwargs):
    return _stub('RepairComplaintsController', 'save', request)

def repair_complaints__lookup_item(request, *args, **kwargs):
    return _stub('RepairComplaintsController', 'lookupItem', request)

def repair_complaints__help_list(request, *args, **kwargs):
    return _stub('RepairComplaintsController', 'helpList', request)


# ---- RepairReceiptMemoPartyController ----
def repair_receipt_memo_party__index(request, *args, **kwargs):
    return _stub('RepairReceiptMemoPartyController', 'index', request)

def repair_receipt_memo_party__next_doc(request, *args, **kwargs):
    return _stub('RepairReceiptMemoPartyController', 'nextDoc', request)

def repair_receipt_memo_party__navigate(request, *args, **kwargs):
    return _stub('RepairReceiptMemoPartyController', 'navigate', request)

def repair_receipt_memo_party__search(request, *args, **kwargs):
    return _stub('RepairReceiptMemoPartyController', 'search', request)

def repair_receipt_memo_party__get(request, *args, **kwargs):
    return _stub('RepairReceiptMemoPartyController', 'get', request)

def repair_receipt_memo_party__save(request, *args, **kwargs):
    return _stub('RepairReceiptMemoPartyController', 'save', request)

def repair_receipt_memo_party__cancel(request, *args, **kwargs):
    return _stub('RepairReceiptMemoPartyController', 'cancel', request)

def repair_receipt_memo_party__lookup_item(request, *args, **kwargs):
    return _stub('RepairReceiptMemoPartyController', 'lookupItem', request)

def repair_receipt_memo_party__search_items(request, *args, **kwargs):
    return _stub('RepairReceiptMemoPartyController', 'searchItems', request)

def repair_receipt_memo_party__lookup_customer(request, *args, **kwargs):
    return _stub('RepairReceiptMemoPartyController', 'lookupCustomer', request)

def repair_receipt_memo_party__search_customers(request, *args, **kwargs):
    return _stub('RepairReceiptMemoPartyController', 'searchCustomers', request)


# ---- RepairReturnController ----
def repair_return__picker(request, *args, **kwargs):
    return _stub('RepairReturnController', 'picker', request)

def repair_return__index(request, *args, **kwargs):
    return _stub('RepairReturnController', 'index', request)

def repair_return__next_doc(request, *args, **kwargs):
    return _stub('RepairReturnController', 'nextDoc', request)

def repair_return__search(request, *args, **kwargs):
    return _stub('RepairReturnController', 'search', request)

def repair_return__picker_search(request, *args, **kwargs):
    return _stub('RepairReturnController', 'pickerSearch', request)

def repair_return__picker_resolve(request, *args, **kwargs):
    return _stub('RepairReturnController', 'pickerResolve', request)

def repair_return__get(request, *args, **kwargs):
    return _stub('RepairReturnController', 'get', request)

def repair_return__load_receipt(request, *args, **kwargs):
    return _stub('RepairReturnController', 'loadReceipt', request)

def repair_return__search_receipts(request, *args, **kwargs):
    return _stub('RepairReturnController', 'searchReceipts', request)

def repair_return__save(request, *args, **kwargs):
    return _stub('RepairReturnController', 'save', request)

def repair_return__cancel(request, *args, **kwargs):
    return _stub('RepairReturnController', 'cancel', request)

def repair_return__lookup_customer(request, *args, **kwargs):
    return _stub('RepairReturnController', 'lookupCustomer', request)


# ---- RuffWorkController ----
def ruff_work__index(request, *args, **kwargs):
    return _stub('RuffWorkController', 'index', request)

def ruff_work__api(request, *args, **kwargs):
    return _stub('RuffWorkController', 'api', request)


# ---- SalesBillConfirmationController ----
def sales_bill_confirmation__index(request, *args, **kwargs):
    return _stub('SalesBillConfirmationController', 'index', request)

def sales_bill_confirmation__load(request, *args, **kwargs):
    return _stub('SalesBillConfirmationController', 'load', request)

def sales_bill_confirmation__confirm(request, *args, **kwargs):
    return _stub('SalesBillConfirmationController', 'confirm', request)

def sales_bill_confirmation__delete(request, *args, **kwargs):
    return _stub('SalesBillConfirmationController', 'delete', request)

def sales_bill_confirmation__view(request, *args, **kwargs):
    return _stub('SalesBillConfirmationController', 'view', request)


# ---- SalesBillController ----
def sales_bill__edit_picker(request, *args, **kwargs):
    return _stub('SalesBillController', 'editPicker', request)

def sales_bill__reprint_picker(request, *args, **kwargs):
    return _stub('SalesBillController', 'reprintPicker', request)

def sales_bill__cancel_picker(request, *args, **kwargs):
    return _stub('SalesBillController', 'cancelPicker', request)

def sales_bill__search_edit_bills(request, *args, **kwargs):
    return _stub('SalesBillController', 'searchEditBills', request)

def sales_bill__resolve_edit_bill(request, *args, **kwargs):
    return _stub('SalesBillController', 'resolveEditBill', request)

def sales_bill__resolve_bill_action(request, *args, **kwargs):
    return _stub('SalesBillController', 'resolveBillAction', request)

def sales_bill__index(request, *args, **kwargs):
    return _stub('SalesBillController', 'index', request)

def sales_bill__next_bill_no(request, *args, **kwargs):
    return _stub('SalesBillController', 'nextBillNo', request)

def sales_bill__check_bill_no(request, *args, **kwargs):
    return _stub('SalesBillController', 'checkBillNo', request)

def sales_bill__get(request, *args, **kwargs):
    return _stub('SalesBillController', 'get', request)

def sales_bill__customer_details(request, *args, **kwargs):
    return _stub('SalesBillController', 'customerDetails', request)

def sales_bill__customer_by_mobile(request, *args, **kwargs):
    return _stub('SalesBillController', 'customerByMobile', request)

def sales_bill__prev_bill(request, *args, **kwargs):
    return _stub('SalesBillController', 'prevBill', request)

def sales_bill__next_bill(request, *args, **kwargs):
    return _stub('SalesBillController', 'nextBill', request)

def sales_bill__search(request, *args, **kwargs):
    return _stub('SalesBillController', 'search', request)

def sales_bill__quotation_list(request, *args, **kwargs):
    return _stub('SalesBillController', 'quotationList', request)

def sales_bill__item_lookup(request, *args, **kwargs):
    return _stub('SalesBillController', 'itemLookup', request)

def sales_bill__recalc(request, *args, **kwargs):
    return _stub('SalesBillController', 'recalc', request)

def sales_bill__save(request, *args, **kwargs):
    return _stub('SalesBillController', 'save', request)

def sales_bill__generate_e_invoice(request, *args, **kwargs):
    return _stub('SalesBillController', 'generateEInvoice', request)

def sales_bill__cancel_bill(request, *args, **kwargs):
    return _stub('SalesBillController', 'cancelBill', request)

def sales_bill__confirm_bill(request, *args, **kwargs):
    return _stub('SalesBillController', 'confirmBill', request)

def sales_bill__reprint(request, *args, **kwargs):
    return _stub('SalesBillController', 'reprint', request)

def sales_bill__customer_search(request, *args, **kwargs):
    return _stub('SalesBillController', 'customerSearch', request)


# ---- SalesBillPrintController ----
def sales_bill_print__show(request, *args, **kwargs):
    return _stub('SalesBillPrintController', 'show', request)

def sales_bill_print__save_setting(request, *args, **kwargs):
    return _stub('SalesBillPrintController', 'saveSetting', request)


# ---- SalesBookReportController ----
def sales_book_report__index(request, *args, **kwargs):
    return _stub('SalesBookReportController', 'index', request)

def sales_book_report__data(request, *args, **kwargs):
    return _stub('SalesBookReportController', 'data', request)

def sales_book_report__lookups(request, *args, **kwargs):
    return _stub('SalesBookReportController', 'lookups', request)

def sales_book_report__bulk_e_invoice_json(request, *args, **kwargs):
    return _stub('SalesBookReportController', 'bulkEInvoiceJson', request)

def sales_book_report__rearrange_bill_nos(request, *args, **kwargs):
    return _stub('SalesBookReportController', 'rearrangeBillNos', request)

def sales_book_report__download_e_invoice_archive(request, *args, **kwargs):
    return _stub('SalesBookReportController', 'downloadEInvoiceArchive', request)


# ---- SalesReturnController ----
def sales_return__picker(request, *args, **kwargs):
    return _stub('SalesReturnController', 'picker', request)

def sales_return__index(request, *args, **kwargs):
    return _stub('SalesReturnController', 'index', request)

def sales_return__picker_search(request, *args, **kwargs):
    return _stub('SalesReturnController', 'pickerSearch', request)

def sales_return__picker_resolve(request, *args, **kwargs):
    return _stub('SalesReturnController', 'pickerResolve', request)

def sales_return__customers(request, *args, **kwargs):
    return _stub('SalesReturnController', 'customers', request)

def sales_return__salesmen(request, *args, **kwargs):
    return _stub('SalesReturnController', 'salesmen', request)

def sales_return__cash_banks(request, *args, **kwargs):
    return _stub('SalesReturnController', 'cashBanks', request)

def sales_return__items(request, *args, **kwargs):
    return _stub('SalesReturnController', 'items', request)

def sales_return__bill_types(request, *args, **kwargs):
    return _stub('SalesReturnController', 'billTypes', request)

def sales_return__gold_rate(request, *args, **kwargs):
    return _stub('SalesReturnController', 'goldRate', request)

def sales_return__next_number(request, *args, **kwargs):
    return _stub('SalesReturnController', 'nextNumber', request)

def sales_return__get_list(request, *args, **kwargs):
    return _stub('SalesReturnController', 'getList', request)

def sales_return__get(request, *args, **kwargs):
    return _stub('SalesReturnController', 'get', request)

def sales_return__search_sale_bill(request, *args, **kwargs):
    return _stub('SalesReturnController', 'searchSaleBill', request)

def sales_return__search_sale_bills(request, *args, **kwargs):
    return _stub('SalesReturnController', 'searchSaleBills', request)

def sales_return__item_details(request, *args, **kwargs):
    return _stub('SalesReturnController', 'itemDetails', request)

def sales_return__customer_balance(request, *args, **kwargs):
    return _stub('SalesReturnController', 'customerBalance', request)

def sales_return__save(request, *args, **kwargs):
    return _stub('SalesReturnController', 'save', request)

def sales_return__delete(request, *args, **kwargs):
    return _stub('SalesReturnController', 'delete', request)


# ---- SmithController ----
def smith__index(request, *args, **kwargs):
    return _stub('SmithController', 'index', request)

def smith__photo(request, *args, **kwargs):
    return _stub('SmithController', 'photo', request)

def smith__groups(request, *args, **kwargs):
    return _stub('SmithController', 'groups', request)

def smith__states(request, *args, **kwargs):
    return _stub('SmithController', 'states', request)

def smith__search(request, *args, **kwargs):
    return _stub('SmithController', 'search', request)

def smith__show(request, *args, **kwargs):
    return _stub('SmithController', 'show', request)

def smith__store(request, *args, **kwargs):
    return _stub('SmithController', 'store', request)

def smith__update(request, *args, **kwargs):
    return _stub('SmithController', 'update', request)

def smith__destroy(request, *args, **kwargs):
    return _stub('SmithController', 'destroy', request)


# ---- StaffLeaveEntryController ----
def staff_leave_entry__index(request, *args, **kwargs):
    return _stub('StaffLeaveEntryController', 'index', request)

def staff_leave_entry__load_data(request, *args, **kwargs):
    return _stub('StaffLeaveEntryController', 'loadData', request)

def staff_leave_entry__save(request, *args, **kwargs):
    return _stub('StaffLeaveEntryController', 'save', request)


# ---- StaffLogUpdateController ----
def staff_log_update__index(request, *args, **kwargs):
    return _stub('StaffLogUpdateController', 'index', request)

def staff_log_update__load_users(request, *args, **kwargs):
    return _stub('StaffLogUpdateController', 'loadUsers', request)

def staff_log_update__load_logs(request, *args, **kwargs):
    return _stub('StaffLogUpdateController', 'loadLogs', request)

def staff_log_update__update_logs(request, *args, **kwargs):
    return _stub('StaffLogUpdateController', 'updateLogs', request)

def staff_log_update__delete_log(request, *args, **kwargs):
    return _stub('StaffLogUpdateController', 'deleteLog', request)

def staff_log_update__clear_logs(request, *args, **kwargs):
    return _stub('StaffLogUpdateController', 'clearLogs', request)

def staff_log_update__connect_device(request, *args, **kwargs):
    return _stub('StaffLogUpdateController', 'connectDevice', request)

def staff_log_update__download_users(request, *args, **kwargs):
    return _stub('StaffLogUpdateController', 'downloadUsers', request)

def staff_log_update__download_logs(request, *args, **kwargs):
    return _stub('StaffLogUpdateController', 'downloadLogs', request)

def staff_log_update__clear_device_logs(request, *args, **kwargs):
    return _stub('StaffLogUpdateController', 'clearDeviceLogs', request)


# ---- StaffReportsController ----
def staff_reports__index(request, *args, **kwargs):
    return _stub('StaffReportsController', 'index', request)

def staff_reports__salesman_book(request, *args, **kwargs):
    return _stub('StaffReportsController', 'salesmanBook', request)

def staff_reports__salesman_summary(request, *args, **kwargs):
    return _stub('StaffReportsController', 'salesmanSummary', request)

def staff_reports__counter_sales(request, *args, **kwargs):
    return _stub('StaffReportsController', 'counterSales', request)

def staff_reports__incharge_report(request, *args, **kwargs):
    return _stub('StaffReportsController', 'inchargeReport', request)

def staff_reports__commission_report(request, *args, **kwargs):
    return _stub('StaffReportsController', 'commissionReport', request)

def staff_reports__performance(request, *args, **kwargs):
    return _stub('StaffReportsController', 'performance', request)

def staff_reports__term_summary(request, *args, **kwargs):
    return _stub('StaffReportsController', 'termSummary', request)

def staff_reports__attendance_report(request, *args, **kwargs):
    return _stub('StaffReportsController', 'attendanceReport', request)

def staff_reports__leave_report(request, *args, **kwargs):
    return _stub('StaffReportsController', 'leaveReport', request)

def staff_reports__staff_log(request, *args, **kwargs):
    return _stub('StaffReportsController', 'staffLog', request)

def staff_reports__ledger(request, *args, **kwargs):
    return _stub('StaffReportsController', 'ledger', request)

def staff_reports__wgt_trans(request, *args, **kwargs):
    return _stub('StaffReportsController', 'wgtTrans', request)


# ---- StaffTransactionController ----
def staff_transaction__index(request, *args, **kwargs):
    return _stub('StaffTransactionController', 'index', request)

def staff_transaction__load_staff(request, *args, **kwargs):
    return _stub('StaffTransactionController', 'loadStaff', request)

def staff_transaction__calc_salary(request, *args, **kwargs):
    return _stub('StaffTransactionController', 'calcSalary', request)

def staff_transaction__log_based_calc(request, *args, **kwargs):
    return _stub('StaffTransactionController', 'logBasedCalc', request)

def staff_transaction__save(request, *args, **kwargs):
    return _stub('StaffTransactionController', 'save', request)

def staff_transaction__lookup_account(request, *args, **kwargs):
    return _stub('StaffTransactionController', 'lookupAccount', request)


# ---- StaffWgtTransactionController ----
def staff_wgt_transaction__index(request, *args, **kwargs):
    return _stub('StaffWgtTransactionController', 'index', request)

def staff_wgt_transaction__next_doc(request, *args, **kwargs):
    return _stub('StaffWgtTransactionController', 'nextDoc', request)

def staff_wgt_transaction__load_sman(request, *args, **kwargs):
    return _stub('StaffWgtTransactionController', 'loadSman', request)

def staff_wgt_transaction__lookup_item(request, *args, **kwargs):
    return _stub('StaffWgtTransactionController', 'lookupItem', request)

def staff_wgt_transaction__search_items(request, *args, **kwargs):
    return _stub('StaffWgtTransactionController', 'searchItems', request)

def staff_wgt_transaction__search(request, *args, **kwargs):
    return _stub('StaffWgtTransactionController', 'search', request)

def staff_wgt_transaction__get(request, *args, **kwargs):
    return _stub('StaffWgtTransactionController', 'get', request)

def staff_wgt_transaction__save(request, *args, **kwargs):
    return _stub('StaffWgtTransactionController', 'save', request)

def staff_wgt_transaction__cancel(request, *args, **kwargs):
    return _stub('StaffWgtTransactionController', 'cancel', request)


# ---- StockController ----
def stock__index(request, *args, **kwargs):
    return _stub('StockController', 'index', request)

def stock__update(request, *args, **kwargs):
    return _stub('StockController', 'update', request)

def stock__stock_list(request, *args, **kwargs):
    return _stub('StockController', 'stockList', request)

def stock__stock_list_data(request, *args, **kwargs):
    return _stub('StockController', 'stockListData', request)

def stock__ledger(request, *args, **kwargs):
    return _stub('StockController', 'ledger', request)

def stock__ledger_export(request, *args, **kwargs):
    return _stub('StockController', 'ledgerExport', request)


# ---- StockPeriodLedgerController ----
def stock_period_ledger__index(request, *args, **kwargs):
    return _stub('StockPeriodLedgerController', 'index', request)

def stock_period_ledger__item_history(request, *args, **kwargs):
    return _stub('StockPeriodLedgerController', 'itemHistory', request)


# ---- StockSummaryCostWiseController ----
def stock_summary_cost_wise__index(request, *args, **kwargs):
    return _stub('StockSummaryCostWiseController', 'index', request)

def stock_summary_cost_wise__show(request, *args, **kwargs):
    return _stub('StockSummaryCostWiseController', 'show', request)


# ---- StockSummaryRateWiseController ----
def stock_summary_rate_wise__index(request, *args, **kwargs):
    return _stub('StockSummaryRateWiseController', 'index', request)

def stock_summary_rate_wise__show(request, *args, **kwargs):
    return _stub('StockSummaryRateWiseController', 'show', request)


# ---- StockSuspenseEntryController ----
def stock_suspense_entry__index(request, *args, **kwargs):
    return _stub('StockSuspenseEntryController', 'index', request)

def stock_suspense_entry__picker(request, *args, **kwargs):
    return _stub('StockSuspenseEntryController', 'picker', request)

def stock_suspense_entry__api(request, *args, **kwargs):
    return _stub('StockSuspenseEntryController', 'api', request)


# ---- StockTypeController ----
def stock_type__index(request, *args, **kwargs):
    return _stub('StockTypeController', 'index', request)

def stock_type__get_list(request, *args, **kwargs):
    return _stub('StockTypeController', 'getList', request)

def stock_type__get_by_code(request, *args, **kwargs):
    return _stub('StockTypeController', 'getByCode', request)

def stock_type__check_code(request, *args, **kwargs):
    return _stub('StockTypeController', 'checkCode', request)

def stock_type__check_usage(request, *args, **kwargs):
    return _stub('StockTypeController', 'checkUsage', request)

def stock_type__get_default(request, *args, **kwargs):
    return _stub('StockTypeController', 'getDefault', request)

def stock_type__store(request, *args, **kwargs):
    return _stub('StockTypeController', 'store', request)

def stock_type__update(request, *args, **kwargs):
    return _stub('StockTypeController', 'update', request)

def stock_type__destroy(request, *args, **kwargs):
    return _stub('StockTypeController', 'destroy', request)

def stock_type__module_settings(request, *args, **kwargs):
    return _stub('StockTypeController', 'moduleSettings', request)


# ---- StockVerificationController ----
def stock_verification__index(request, *args, **kwargs):
    return _stub('StockVerificationController', 'index', request)

def stock_verification__lookup_barcode(request, *args, **kwargs):
    return _stub('StockVerificationController', 'lookupBarcode', request)

def stock_verification__delete_item(request, *args, **kwargs):
    return _stub('StockVerificationController', 'deleteItem', request)

def stock_verification__fresh_mark(request, *args, **kwargs):
    return _stub('StockVerificationController', 'freshMark', request)

def stock_verification__finished(request, *args, **kwargs):
    return _stub('StockVerificationController', 'finished', request)

def stock_verification__update_as_correct(request, *args, **kwargs):
    return _stub('StockVerificationController', 'updateAsCorrect', request)

def stock_verification__summary(request, *args, **kwargs):
    return _stub('StockVerificationController', 'summary', request)

def stock_verification__import_file(request, *args, **kwargs):
    return _stub('StockVerificationController', 'importFile', request)


# ---- SupplierBillwisePaymentController ----
def supplier_billwise_payment__index(request, *args, **kwargs):
    return _stub('SupplierBillwisePaymentController', 'index', request)

def supplier_billwise_payment__api(request, *args, **kwargs):
    return _stub('SupplierBillwisePaymentController', 'api', request)


# ---- SupplierReportsController ----
def supplier_reports__duedate_index(request, *args, **kwargs):
    return _stub('SupplierReportsController', 'duedateIndex', request)

def supplier_reports__duedate_data(request, *args, **kwargs):
    return _stub('SupplierReportsController', 'duedateData', request)

def supplier_reports__supplier_list_index(request, *args, **kwargs):
    return _stub('SupplierReportsController', 'supplierListIndex', request)

def supplier_reports__supplier_list_data(request, *args, **kwargs):
    return _stub('SupplierReportsController', 'supplierListData', request)


# ---- SuspenseLedgerController ----
def suspense_ledger__index(request, *args, **kwargs):
    return _stub('SuspenseLedgerController', 'index', request)


# ---- TermSummaryController ----
def term_summary__index(request, *args, **kwargs):
    return _stub('TermSummaryController', 'index', request)

def term_summary__data(request, *args, **kwargs):
    return _stub('TermSummaryController', 'data', request)


# ---- UserAccessController ----
def user_access__index(request, *args, **kwargs):
    return _stub('UserAccessController', 'index', request)

def user_access__get_users(request, *args, **kwargs):
    return _stub('UserAccessController', 'getUsers', request)

def user_access__get_user(request, *args, **kwargs):
    return _stub('UserAccessController', 'getUser', request)

def user_access__save_user(request, *args, **kwargs):
    return _stub('UserAccessController', 'saveUser', request)

def user_access__delete_user(request, *args, **kwargs):
    return _stub('UserAccessController', 'deleteUser', request)


# ---- WastageTableController ----
def wastage_table__index(request, *args, **kwargs):
    return _stub('WastageTableController', 'index', request)

def wastage_table__validate_item(request, *args, **kwargs):
    return _stub('WastageTableController', 'validateItem', request)

def wastage_table__show_rows(request, *args, **kwargs):
    return _stub('WastageTableController', 'showRows', request)

def wastage_table__save(request, *args, **kwargs):
    return _stub('WastageTableController', 'save', request)


# ---- WgtRcptPmntController ----
def wgt_rcpt_pmnt__index(request, *args, **kwargs):
    return _stub('WgtRcptPmntController', 'index', request)

def wgt_rcpt_pmnt__api(request, *args, **kwargs):
    return _stub('WgtRcptPmntController', 'api', request)


# ---- YearEndAccountCloseController ----
def year_end_account_close__index(request, *args, **kwargs):
    return _stub('YearEndAccountCloseController', 'index', request)

def year_end_account_close__init_doc_nos(request, *args, **kwargs):
    return _stub('YearEndAccountCloseController', 'initDocNos', request)

def year_end_account_close__close_accounts(request, *args, **kwargs):
    return _stub('YearEndAccountCloseController', 'closeAccounts', request)


# ---- YearlyCashBalanceController ----
def yearly_cash_balance__index(request, *args, **kwargs):
    return _stub('YearlyCashBalanceController', 'index', request)

