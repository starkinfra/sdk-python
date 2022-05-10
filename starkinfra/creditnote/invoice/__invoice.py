from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime, check_datetime_or_date, check_timedelta


class Invoice(Resource):
    """# creditnote.Invoice object
    Invoice object to be created and sent to the credit receiver.
    ## Parameters (required):
    - amount [integer]: Invoice value in cents. Minimum = 0 (any value will be accepted). ex: 1234 (= R$ 12.34)
    - tax_id [string]: payer tax ID (CPF or CNPJ) with or without formatting. ex: "01234567890" or "20.018.183/0001-80"
    - name [string]: payer name. ex: "Iron Bank S.A."
    ## Parameters (optional):
    - due [datetime.datetime or datetime.date or string, default now + 2 days]: Invoice due date in UTC ISO format. ex: "2020-10-28T17:59:26.249976+00:00" for immediate invoices and "2020-10-28" for scheduled invoices
    - expiration [integer or datetime.timedelta, default 5097600 (59 days)]: time interval in seconds between due date and expiration date. ex 123456789
    - fine [float, default 2.0]: Invoice fine for overdue payment in %. ex: 2.5
    - interest [float, default 1.0]: Invoice monthly interest for overdue payment in %. ex: 5.2
    - discounts [list of dictionaries, default None]: list of dictionaries with "percentage":float and "due":datetime.datetime or string pairs
    - tags [list of strings, default None]: list of strings for tagging
    - descriptions [list of dictionaries, default None]: list of dictionaries with "key":string and (optional) "value":string pairs
    ## Attributes (return-only):
    - pdf [string, default None]: public Invoice PDF URL. ex: "https://invoice.starkbank.com/pdf/d454fa4e524441c1b0c1a729457ed9d8"
    - link [string, default None]: public Invoice webpage URL. ex: "https://my-workspace.sandbox.starkbank.com/invoicelink/d454fa4e524441c1b0c1a729457ed9d8"
    - nominal_amount [integer, default None]: Invoice emission value in cents (will change if invoice is updated, but not if it's paid). ex: 400000
    - fine_amount [integer, default None]: Invoice fine value calculated over nominal_amount. ex: 20000
    - interest_amount [integer, default None]: Invoice interest value calculated over nominal_amount. ex: 10000
    - discount_amount [integer, default None]: Invoice discount value calculated over nominal_amount. ex: 3000
    - id [string, default None]: unique id returned when Invoice is created. ex: "5656565656565656"
    - brcode [string, default None]: BR Code for the Invoice payment. ex: "00020101021226800014br.gov.bcb.pix2558invoice.starkbank.com/f5333103-3279-4db2-8389-5efe335ba93d5204000053039865802BR5913Arya Stark6009Sao Paulo6220051656565656565656566304A9A0"
    - status [string, default None]: current Invoice status. ex: "registered" or "paid"
    - fee [integer, default None]: fee charged by this Invoice. ex: 200 (= R$ 2.00)
    - transaction_ids [list of strings]: ledger transaction ids linked to this Invoice (if there are more than one, all but the first are reversals or failed reversal chargebacks). ex: ["19827356981273"]
    - created [datetime.datetime, default None]: creation datetime for the Invoice. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - updated [datetime.datetime, default None]: latest update datetime for the Invoice. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, amount, tax_id, name, due=None, expiration=None, fine=None, interest=None, discounts=None,
                 tags=None, descriptions=None, pdf=None, link=None, nominal_amount=None, fine_amount=None,
                 interest_amount=None, discount_amount=None, id=None, brcode=None, status=None, fee=None,
                 transaction_ids=None, created=None, updated=None):
        Resource.__init__(self, id=id)

        self.amount = amount
        self.nominal_amount = nominal_amount
        self.fine_amount = fine_amount
        self.interest_amount = interest_amount
        self.discount_amount = discount_amount
        self.due = check_datetime_or_date(due)
        self.tax_id = tax_id
        self.name = name
        self.expiration = check_timedelta(expiration)
        self.fine = fine
        self.interest = interest
        self.discounts = discounts
        self.tags = tags
        self.pdf = pdf
        self.link = link
        self.descriptions = descriptions
        self.brcode = brcode
        self.status = status
        self.fee = fee
        self.transaction_ids = transaction_ids
        self.created = check_datetime(created)
        self.updated = check_datetime(updated)


_resource = {"class": Invoice, "name": "Invoice"}
