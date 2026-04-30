"""
Django models translated from Laravel migrations + Eloquent models.

Tables created by Laravel migrations are managed (Django can create/migrate them).
Legacy tables that pre-exist in the customer DB (userm, userd, generals, clients,
daybook, accountm, salesm, etc.) are declared as unmanaged — Django reads/writes
them but never tries to create or alter them.
"""
from django.db import models


# ---------------------------------------------------------------------------
# Managed tables (from database/migrations/*)
# ---------------------------------------------------------------------------

class Item(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = "items"

    def __str__(self):
        return f"{self.code} - {self.name}"


class ProductModel(models.Model):
    """Maps to `models` table (mtype='M' for models, 'S' for sizes)."""
    mtype = models.CharField(max_length=1)
    name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = "models"
        unique_together = (("mtype", "name"),)


class Rotable(models.Model):
    code = models.CharField(max_length=10, db_index=True)
    model = models.CharField(max_length=20, null=True, blank=True)
    size = models.CharField(max_length=20, null=True, blank=True)
    weight1 = models.DecimalField(max_digits=8, decimal_places=3, default=0)
    weight2 = models.DecimalField(max_digits=8, decimal_places=3, default=0)
    minqty = models.IntegerField(default=0)
    maxqty = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = "rotable"


class StockType(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=30)
    is_default = models.SmallIntegerField(db_column="def", default=0, db_index=True)
    compare = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = "stktype"


class PartyMCTable(models.Model):
    pcode = models.CharField(max_length=10, db_index=True)
    icode = models.CharField(max_length=10, db_index=True)
    model = models.CharField(max_length=15, null=True, blank=True)
    wastage = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    mc = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    mcperc = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    mcperqty = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    touch = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    formula = models.CharField(max_length=15, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = "pmctable"
        indexes = [models.Index(fields=["pcode", "icode", "model"])]


class MCTable(models.Model):
    """No PK in Laravel — Django requires one, so we add an implicit id."""
    code = models.CharField(max_length=10, db_index=True)
    weight1 = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    weight2 = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    mc = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    mcpergm = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    mcperqty = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    vaperc = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    iqtype = models.CharField(max_length=10, default="")

    class Meta:
        db_table = "mctable"


class GiftTable(models.Model):
    points = models.IntegerField(primary_key=True)
    particulars = models.CharField(max_length=60, null=True, blank=True)

    class Meta:
        db_table = "gifttable"


class PointCardTable(models.Model):
    """Composite PK (pcard, isubgrp) — declared via unique_together."""
    pcard = models.CharField(max_length=10, db_index=True)
    isubgrp = models.CharField(max_length=10, db_index=True)
    pointbasedon = models.CharField(max_length=10, default="Wgt")
    valuefor1point = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    valueperpoint = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    minsalesamt = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    rounddown = models.DecimalField(max_digits=12, decimal_places=3, default=0)

    class Meta:
        db_table = "pcardtable"
        unique_together = (("pcard", "isubgrp"),)


class DenominationMaster(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=20, null=True, blank=True)
    cvalue = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        db_table = "denom_master"


class Route(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=40, null=True, blank=True)

    class Meta:
        db_table = "route"


class Area(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=30, null=True, blank=True)

    class Meta:
        db_table = "area"


class PCard(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=30, null=True, blank=True)
    vadisc = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    totdisc = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        db_table = "pcard"


class ClientsAdvanced(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    pincode = models.CharField(max_length=30, null=True, blank=True)
    fax = models.CharField(max_length=120, null=True, blank=True)
    relationperiod = models.CharField(max_length=30, null=True, blank=True)
    relationway = models.CharField(max_length=40, null=True, blank=True)
    relationwayname = models.CharField(max_length=120, null=True, blank=True)
    relationbases = models.CharField(max_length=40, null=True, blank=True)
    relationbasesname = models.CharField(max_length=120, null=True, blank=True)
    purchasepurpose = models.CharField(max_length=30, null=True, blank=True)
    purchasecategory = models.CharField(max_length=30, null=True, blank=True)
    purchasetype = models.CharField(max_length=30, null=True, blank=True)
    working = models.CharField(max_length=30, null=True, blank=True)
    comment = models.CharField(max_length=255, null=True, blank=True)
    promptorder = models.CharField(max_length=10, null=True, blank=True)
    dtmarriage = models.DateField(null=True, blank=True)
    dtengagement = models.DateField(null=True, blank=True)
    dtbirthday = models.DateField(null=True, blank=True)
    grateinform = models.CharField(max_length=10, null=True, blank=True)
    staffperf = models.CharField(max_length=20, null=True, blank=True)
    properf = models.CharField(max_length=20, null=True, blank=True)
    respperf = models.CharField(max_length=20, null=True, blank=True)
    speedperf = models.CharField(max_length=20, null=True, blank=True)
    cleanperf = models.CharField(max_length=20, null=True, blank=True)
    facilityperf = models.CharField(max_length=20, null=True, blank=True)
    parkfacilityperf = models.CharField(max_length=20, null=True, blank=True)
    contshop = models.CharField(max_length=10, null=True, blank=True)
    recommend = models.CharField(max_length=10, null=True, blank=True)
    area = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        db_table = "clients_advanced"


class SalesBill(models.Model):
    bill_no = models.CharField(max_length=40, unique=True)
    bill_date = models.DateField(null=True, blank=True)
    bill_time = models.CharField(max_length=20, null=True, blank=True)
    bill_type = models.CharField(max_length=30, default="Gold")
    customer_code = models.CharField(max_length=20, null=True, blank=True)
    customer_name = models.CharField(max_length=120, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    mobile = models.CharField(max_length=30, null=True, blank=True)
    gst_no = models.CharField(max_length=40, null=True, blank=True)
    pan_no = models.CharField(max_length=30, null=True, blank=True)
    state_code = models.CharField(max_length=20, null=True, blank=True)
    rate_per_gm = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    counter_name = models.CharField(max_length=80, null=True, blank=True)
    counter_code = models.CharField(max_length=20, null=True, blank=True)
    salesman_name = models.CharField(max_length=120, null=True, blank=True)
    salesman_code = models.CharField(max_length=20, null=True, blank=True)
    agent_code = models.CharField(max_length=20, null=True, blank=True)
    approved_by = models.CharField(max_length=20, null=True, blank=True)
    cashbank_code = models.CharField(max_length=20, null=True, blank=True)
    bill_total = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    exchange_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    return_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    net_total = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    status = models.CharField(max_length=20, default="saved")
    items_json = models.TextField(null=True, blank=True)
    exchange_json = models.TextField(null=True, blank=True)
    return_json = models.TextField(null=True, blank=True)
    extra_json = models.TextField(null=True, blank=True)
    cancel_reason = models.CharField(max_length=255, null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = "sales_bills"
        indexes = [models.Index(fields=["bill_date", "status"])]


# ---------------------------------------------------------------------------
# Unmanaged legacy tables (referenced by Laravel app but pre-exist in DB).
# Field lists are best-effort from controllers/models; columns that aren't
# declared here are still queryable via raw SQL (used in many reports).
# ---------------------------------------------------------------------------

class UserM(models.Model):
    """Login users — stores fpCrypt-encoded password in `pcode`."""
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=120, null=True, blank=True)
    pcode = models.BinaryField(null=True, blank=True)
    email = models.CharField(max_length=120, null=True, blank=True)
    mobile = models.CharField(max_length=30, null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        managed = False
        db_table = "userm"


class UserD(models.Model):
    """User permission rows: (code, menuitem)."""
    code = models.CharField(max_length=10, db_index=True)
    menuitem = models.CharField(max_length=60)

    class Meta:
        managed = False
        db_table = "userd"


class UserHist(models.Model):
    code = models.CharField(max_length=10, db_index=True)
    tdate = models.DateField(null=True, blank=True)
    time1 = models.CharField(max_length=20, null=True, blank=True)
    time2 = models.CharField(max_length=20, null=True, blank=True)
    ip = models.CharField(max_length=45, null=True, blank=True)
    useragent = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        managed = False
        db_table = "userhist"


class Generals(models.Model):
    """Key-value config table (SHOPNM, SHOPADDR, GSTIN, ...)."""
    code = models.CharField(max_length=20, primary_key=True)
    cvalue = models.TextField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = "generals"


class Generali(models.Model):
    code = models.CharField(max_length=20, primary_key=True)
    ivalue = models.IntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = "generali"


class Clients(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=120, null=True, blank=True)
    address1 = models.CharField(max_length=120, null=True, blank=True)
    address2 = models.CharField(max_length=120, null=True, blank=True)
    city = models.CharField(max_length=60, null=True, blank=True)
    state = models.CharField(max_length=30, null=True, blank=True)
    pincode = models.CharField(max_length=20, null=True, blank=True)
    mobile = models.CharField(max_length=30, null=True, blank=True)
    telephone = models.CharField(max_length=30, null=True, blank=True)
    email = models.CharField(max_length=120, null=True, blank=True)
    ctype = models.CharField(max_length=10, null=True, blank=True)
    gstno = models.CharField(max_length=40, null=True, blank=True)
    panno = models.CharField(max_length=30, null=True, blank=True)

    class Meta:
        managed = False
        db_table = "clients"


class AccountM(models.Model):
    accode = models.CharField(max_length=10, primary_key=True)
    acname = models.CharField(max_length=120, null=True, blank=True)
    grpcode = models.CharField(max_length=10, null=True, blank=True)
    opbal = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    opbaltype = models.CharField(max_length=2, null=True, blank=True)

    class Meta:
        managed = False
        db_table = "accountm"


class DayBook(models.Model):
    """Header for receipts/payments/journal entries."""
    docno = models.CharField(max_length=20, primary_key=True)
    docdate = models.DateField(null=True, blank=True)
    accode = models.CharField(max_length=10, null=True, blank=True, db_index=True)
    naration = models.CharField(max_length=255, null=True, blank=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    voutype = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        managed = False
        db_table = "daybook"


class DayBookPart(models.Model):
    docno = models.CharField(max_length=20, db_index=True)
    accode = models.CharField(max_length=10, null=True, blank=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    taxamt = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        managed = False
        db_table = "daybookpart"


class ItemsStk(models.Model):
    """Per-item per-stocktype on-hand quantities/weights."""
    code = models.CharField(max_length=10, db_index=True)
    stktype = models.CharField(max_length=10, db_index=True)
    qty = models.DecimalField(max_digits=14, decimal_places=3, default=0)
    qtyb = models.DecimalField(max_digits=14, decimal_places=3, default=0)
    weight = models.DecimalField(max_digits=14, decimal_places=3, default=0)
    weightb = models.DecimalField(max_digits=14, decimal_places=3, default=0)
    stonewgt = models.DecimalField(max_digits=14, decimal_places=3, default=0)
    stonewgtb = models.DecimalField(max_digits=14, decimal_places=3, default=0)
    opqty = models.DecimalField(max_digits=14, decimal_places=3, default=0)
    opqtyb = models.DecimalField(max_digits=14, decimal_places=3, default=0)
    opweight = models.DecimalField(max_digits=14, decimal_places=3, default=0)
    opweightb = models.DecimalField(max_digits=14, decimal_places=3, default=0)
    opstonewgt = models.DecimalField(max_digits=14, decimal_places=3, default=0)
    opstonewgtb = models.DecimalField(max_digits=14, decimal_places=3, default=0)
    opstoneamt = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    opstoneamtb = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    opdmdwgt = models.DecimalField(max_digits=14, decimal_places=3, default=0)

    class Meta:
        managed = False
        db_table = "itemsstk"


class SalesType(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=30, null=True, blank=True)
    formno = models.CharField(max_length=10, default="")
    prefix = models.CharField(max_length=10, default="")
    pprefix = models.CharField(max_length=10, default="")
    srprefix = models.CharField(max_length=10, default="")
    prprefix = models.CharField(max_length=10, default="")

    class Meta:
        managed = False
        db_table = "salestype"


# Lightweight unmanaged stubs for additional legacy tables that controllers
# query via raw SQL. They exist as placeholders so views can do raw queries
# without import errors; full field mappings can be added incrementally.

class _LegacyTableMixin(models.Model):
    """Marker base — unmanaged legacy table without enforced columns."""
    class Meta:
        abstract = True
        managed = False


def _legacy(table_name, pk_field="docno", pk_max=20):
    """Factory for trivial legacy table stubs (PK + a free-form text col)."""
    attrs = {
        pk_field: models.CharField(max_length=pk_max, primary_key=True),
        "Meta": type("Meta", (), {"managed": False, "db_table": table_name}),
        "__module__": __name__,
    }
    return type(table_name.title().replace("_", ""), (models.Model,), attrs)


SalesM = _legacy("salesm")
SalesD = _legacy("salesd")
SalesRM = _legacy("salesrm")
SalesRD = _legacy("salesrd")
PurchaseM = _legacy("purchasem")
PurchaseD = _legacy("purchased")
PurchaseRM = _legacy("purchaserm")
PurchaseRD = _legacy("purchaserd")
OrderM = _legacy("orderm")
OrderD = _legacy("orderd")
SmithM = _legacy("smithm")
SmithD = _legacy("smithd")
RefineryM = _legacy("refinerym")
RefineryD = _legacy("refineryd")
RepairM = _legacy("repairm")
RepairD = _legacy("repaird")
ItemAdj = _legacy("itemadj")
DelPart = _legacy("delpart")
OitemTranM = _legacy("oitemtranm")
