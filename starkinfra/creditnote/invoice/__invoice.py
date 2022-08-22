from starkcore.utils.api import from_api_json
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime, check_datetime_or_date, check_timedelta
from .__discount import Discount
from .__discount import resource as _discount_resource
from .__description import Description
from .__description import resource as _description_resource


class Invoice(Resource):
    """# creditnote.Invoice object
    Invoice issued after the contract is signed, to be paid by the credit receiver.
    ## Parameters (required):
    - amount [integer]: Invoice value in cents. Minimum = 1 (any value will be accepted). ex: 1234 (= R$ 12.34)
    ## Parameters (optional):
    - due [datetime.datetime or datetime.date or string, default now + 2 days]: Invoice due date in UTC ISO format. ex: "2020-10-28T17:59:26.249976+00:00" for immediate invoices and "2020-10-28" for scheduled invoices
    - expiration [integer or datetime.timedelta, default 5097600 (59 days)]: time interval in seconds between due date and expiration date. ex 123456789
    - tags [list of strings, default []]: list of strings for tagging
    - descriptions [list of creditnote.invoice.Description objects or dictionaries, default None]: list Description objects
    ## Attributes (return-only):
    - id [string]: unique id returned when Invoice is created. ex: "5656565656565656"
    - name [string]: payer name. ex: "Iron Bank S.A."
    - tax_id [string]: payer tax ID (CPF or CNPJ) with or without formatting. ex: "01234567890" or "20.018.183/0001-80"
    - pdf [string]: public Invoice PDF URL. ex: "https://invoice.starkbank.com/pdf/d454fa4e524441c1b0c1a729457ed9d8"
    - link [string]: public Invoice webpage URL. ex: "https://my-workspace.sandbox.starkbank.com/invoicelink/d454fa4e524441c1b0c1a729457ed9d8"
    - fine [float]: Invoice fine for overdue payment in %. ex: 2.5
    - interest [float]: Invoice monthly interest for overdue payment in %. ex: 5.2
    - nominal_amount [integer]: Invoice emission value in cents (will change if invoice is updated, but not if it's paid). ex: 400000
    - fine_amount [integer]: Invoice fine value calculated over nominal_amount. ex: 20000
    - interest_amount [integer]: Invoice interest value calculated over nominal_amount. ex: 10000
    - discount_amount [integer]: Invoice discount value calculated over nominal_amount. ex: 3000
    - discounts [list of creditnote.invoice.Discount objects]: list of Discount objects. ex: [Discount()]
    - brcode [string]: BR Code for the Invoice payment. ex: "00020101021226800014br.gov.bcb.pix2558invoice.starkbank.com/f5333103-3279-4db2-8389-5efe335ba93d5204000053039865802BR5913Arya Stark6009Sao Paulo6220051656565656565656566304A9A0"
    - status [string]: current Invoice status. ex: "registered" or "paid"
    - fee [integer]: fee charged by this Invoice. ex: 200 (= R$ 2.00)
    - transaction_ids [list of strings]: ledger transaction ids linked to this Invoice (if there are more than one, all but the first are reversals or failed reversal chargebacks). ex: ["19827356981273"]
    - created [datetime.datetime]: creation datetime for the Invoice. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - updated [datetime.datetime]: latest update datetime for the Invoice. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, amount, due=None, expiration=None, tags=None, descriptions=None, id=None, name=None, tax_id=None,
                 pdf=None, link=None, fine=None, interest=None, nominal_amount=None, fine_amount=None,
                 interest_amount=None, discount_amount=None, discounts=None, brcode=None, status=None, fee=None,
                 transaction_ids=None, created=None, updated=None):
        Resource.__init__(self, id=id)

        self.amount = amount
        self.due = check_datetime_or_date(due)
        self.expiration = check_timedelta(expiration)
        self.fine = fine
        self.interest = interest
        self.tags = tags
        self.descriptions = parse_descriptions(descriptions)
        self.name = name
        self.tax_id = tax_id
        self.pdf = pdf
        self.link = link
        self.nominal_amount = nominal_amount
        self.fine_amount = fine_amount
        self.interest_amount = interest_amount
        self.discount_amount = discount_amount
        self.discounts = parse_discounts(discounts)
        self.brcode = brcode
        self.status = status
        self.fee = fee
        self.transaction_ids = transaction_ids
        self.created = check_datetime(created)
        self.updated = check_datetime(updated)


def parse_discounts(discounts):
    parsed_discounts = []
    if discounts is None:
        return discounts
    for discount in discounts:
        if isinstance(discount, Discount):
            parsed_discounts.append(discount)
            continue
        parsed_discounts.append(from_api_json(_discount_resource, discount))
    return parsed_discounts


def parse_descriptions(descriptions):
    parsed_descriptions = []
    if descriptions is None:
        return descriptions
    for description in descriptions:
        if isinstance(description, Description):
            parsed_descriptions.append(description)
            continue
        parsed_descriptions.append(from_api_json(_description_resource, description))
    return parsed_descriptions


_resource = {"class": Invoice, "name": "Invoice"}
