from starkcore.utils.api import from_api_json
from starkcore.utils.subresource import SubResource
from ..creditnote.invoice.__invoice import Invoice, _resource as _invoice_resource


class CreditNotePreview(SubResource):
    """# CreditNotePreview object
    A CreditNotePreview is used to preview a CCB contract between the borrower and lender with a specific table type.
    When you initialize a CreditNotePreview, the entity will be automatically sent to the Stark Infra API.
    The 'create' function sends the objects
    to the Stark Infra API and returns the list of preview data.
    ## Parameters (required):
    - type [string]: table type that defines the amortization system. Options: "sac", "price", "american", "bullet", "custom"
    - nominal_amount [integer]: amount in cents transferred to the credit receiver, before deductions. ex: 11234 (= R$ 112.34)
    - scheduled [datetime.date, datetime.datetime or string]: date of transfer execution. ex: datetime(2020, 3, 10)
    - tax_id [string]: credit receiver's tax ID (CPF or CNPJ). ex: "20.018.183/0001-80"
    ## Parameters (conditionally required):
    - invoices [list of Invoice objects]: list of Invoice objects to be created and sent to the credit receiver. ex: [Invoice(), Invoice()]
    - nominal_interest [float]: yearly nominal interest rate of the credit note, in percentage. ex: 12.5
    - initial_due [datetime.date, datetime.datetime or string]: date of the first invoice. ex: datetime(2020, 3, 10)
    - count [integer]: quantity of invoices for payment. ex: 12
    - initial_amount [integer]: value of the first invoice in cents. ex: 1234 (= R$12.34)
    - interval [string]: interval between invoices. ex: "year", "month"
    ## Parameters (optional):
    - rebate_amount [integer, default None]: credit analysis fee deducted from lent amount. ex: 11234 (= R$ 112.34)
    ## Attributes (return-only):
    - amount [integer]: CreditNote value in cents. ex: 1234 (= R$ 12.34)
    - interest [float]: yearly effective interest rate of the credit note, in percentage. ex: 12.5
    - tax_amount [integer]: tax amount included in the CreditNote. ex: 100
    """

    def __init__(self, type, nominal_amount, scheduled, tax_id, invoices=None, nominal_interest=None,
                 initial_due=None, count=None, initial_amount=None, interval=None, rebate_amount=None,
                 amount=None, interest=None, tax_amount=None):
        self.type = type
        self.nominal_amount = nominal_amount
        self.scheduled = scheduled
        self.tax_id = tax_id
        self.invoices = _parse_optional_invoices(invoices)
        self.nominal_interest = nominal_interest
        self.initial_due = initial_due
        self.count = count
        self.initial_amount = initial_amount
        self.interval = interval
        self.rebate_amount = rebate_amount
        self.amount = amount
        self.interest = interest
        self.tax_amount = tax_amount


_sub_resource = {"class": CreditNotePreview, "name": "CreditNotePreview"}


def _parse_optional_invoices(invoices):
    if invoices is None:
        return None

    parsed_invoices = []
    for invoice in invoices:
        if isinstance(invoice, Invoice):
            parsed_invoices.append(invoice)
            continue
        parsed_invoices.append(from_api_json(_invoice_resource, invoice))
    return parsed_invoices
