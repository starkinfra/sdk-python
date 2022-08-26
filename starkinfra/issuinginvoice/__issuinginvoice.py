from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime, check_date, check_datetime_or_date
from ..utils import rest


class IssuingInvoice(Resource):
    """# IssuingInvoice object
    The IssuingInvoice objects created in your Workspace load your Issuing balance when paid.
    ## Parameters (required):
    - amount [integer]: IssuingInvoice value in cents. ex: 1234 (= R$ 12.34)
    ## Parameters (optional):
    - tax_id [string, default sub-issuer tax ID]: payer tax ID (CPF or CNPJ) with or without formatting. ex: "01234567890" or "20.018.183/0001-80"
    - name [string, default sub-issuer name]: payer name. ex: "Iron Bank S.A."
    - tags [list of strings, default []]: list of strings for tagging. ex: ["travel", "food"]
    ## Attributes (return-only):
    - id [string]: unique id returned when IssuingInvoice is created. ex: "5656565656565656"
    - brcode [string]: BR Code for the Invoice payment. ex: "00020101021226930014br.gov.bcb.pix2571brcode-h.development.starkinfra.com/v2/d7f6546e194d4c64a153e8f79f1c41ac5204000053039865802BR5925Stark Bank S.A. - Institu6009Sao Paulo62070503***63042109"
    - due [datetime.datetime or datetime.date or string]: Invoice due and expiration date in UTC ISO format. ex: "2020-10-28T17:59:26.249976+00:00"
    - link [string]: public Invoice webpage URL. ex: "https://starkbank-card-issuer.development.starkbank.com/invoicelink/d7f6546e194d4c64a153e8f79f1c41ac"
    - status [string]: current IssuingInvoice status. ex: "created", "expired", "overdue", "paid"
    - issuing_transaction_id [string]: ledger transaction ids linked to this IssuingInvoice. ex: "issuing-invoice/5656565656565656"
    - updated [datetime.datetime]: latest update datetime for the IssuingInvoice. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - created [datetime.datetime]: creation datetime for the IssuingInvoice. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, amount, tax_id=None, name=None, tags=None, id=None, brcode=None, due=None, link=None, status=None, 
                issuing_transaction_id=None, updated=None, created=None):
        Resource.__init__(self, id=id)

        self.amount = amount
        self.tax_id = tax_id
        self.name = name
        self.tags = tags
        self.brcode = brcode
        self.due = check_datetime_or_date(due)
        self.link = link
        self.status = status
        self.issuing_transaction_id = issuing_transaction_id
        self.updated = check_datetime(updated)
        self.created = check_datetime(created)


_resource = {"class": IssuingInvoice, "name": "IssuingInvoice"}


def create(invoice, user=None):
    """# Create IssuingInvoices
    Send an IssuingInvoice object for creation at the Stark Infra API
    ## Parameters (required):
    - invoice [IssuingInvoice object]: IssuingInvoice object to be created in the API.
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - IssuingInvoice object with updated attributes
    """
    return rest.post_single(resource=_resource, entity=invoice, user=user)


def get(id, user=None):
    """# Retrieve a specific IssuingInvoice
    Receive a single IssuingInvoice object previously created in the Stark Infra API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - IssuingInvoice object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def query(limit=None, after=None, before=None, status=None, tags=None, user=None):
    """# Retrieve IssuingInvoices
    Receive a generator of IssuingInvoice objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. ex: ["created", "expired", "overdue", "paid"]
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - generator of IssuingInvoice objects with updated attributes
    """
    return rest.get_stream(
        resource=_resource,
        status=status,
        after=check_date(after),
        before=check_date(before),
        tags=tags,
        limit=limit,
        user=user,
    )


def page(cursor=None, limit=None, after=None, before=None, status=None, tags=None, user=None):
    """# Retrieve IssuingInvoices
    Receive a list of IssuingInvoice objects previously created in the Stark Infra API and the cursor to the next page.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - limit [integer, default 100]: maximum number of objects to be retrieved. Max = 100. ex: 35
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. ex: ["created", "expired", "overdue", "paid"]
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of IssuingInvoice objects with updated attributes
    - cursor to retrieve the next page of IssuingInvoice objects
    """
    return rest.get_page(
        resource=_resource,
        cursor=cursor,
        status=status,
        after=check_date(after),
        before=check_date(before),
        tags=tags,
        limit=limit,
        user=user,
    )
