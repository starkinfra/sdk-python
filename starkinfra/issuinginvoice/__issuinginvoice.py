from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime
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
    - status [string]: current IssuingHolder status. ex: "active", "blocked" or "canceled"
    - issuing_transaction_id [string]: ledger transaction ids linked to this IssuingInvoice. ex: "issuing-invoice/5656565656565656"
    - updated [datetime.datetime]: latest update datetime for the IssuingInvoice. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - created [datetime.datetime]: creation datetime for the IssuingInvoice. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, amount, id=None, name=None, tax_id=None, status=None, issuing_transaction_id=None,
                 tags=None, updated=None, created=None):
        Resource.__init__(self, id=id)
        self.amount = amount
        self.name = name
        self.tax_id = tax_id
        self.status = status
        self.issuing_transaction_id = issuing_transaction_id
        self.tags = tags
        self.updated = check_datetime(updated)
        self.created = check_datetime(created)


_resource = {"class": IssuingInvoice, "name": "IssuingInvoice"}


def create(amount, name=None, tax_id=None, tags=None, user=None):
    """# Create IssuingInvoices
    Send a list of IssuingInvoice objects for creation in the Stark Bank API
    ## Parameters (required):
    - amount [integer]: Invoice value in cents. Minimum = 0 (any value will be accepted). ex: 1234 (= R$ 12.34)
    ## Parameters (optional):
    - name [string, default None]: payer name. ex: "Iron Bank S.A."
    - tax_id [string, default None]: payer tax ID (CPF or CNPJ) with or without formatting. ex: "01234567890" or "20.018.183/0001-80"
    - tags [list of strings, default None]: list of strings for tagging
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - IssuingInvoice object with updated attributes
    """
    return rest.post_single(
        resource=_resource,
        entity=IssuingInvoice(amount=amount, name=name, tax_id=tax_id, tags=tags),
        user=user
    )


def get(id, user=None):
    """# Retrieve a specific IssuingInvoice
    Receive a single IssuingInvoice object previously created in the Stark Infra API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - IssuingInvoice object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def query(status=None, after=None, before=None, tags=None, limit=None, user=None):
    """# Retrieve IssuingInvoices
    Receive a generator of IssuingInvoices objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default 100]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - status [string, default None]: filter for status of retrieved objects. ex: "paid" or "registered"
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - generator of IssuingInvoices objects with updated attributes
    """
    return rest.get_stream(
        resource=_resource,
        status=status,
        after=check_datetime(after),
        before=check_datetime(before),
        tags=tags,
        limit=limit,
        user=user,
    )


def page(status=None, after=None, before=None, tags=None, limit=None, cursor=None, user=None):
    """# Retrieve IssuingInvoices
    Receive a list of IssuingInvoices objects previously created in the Stark Infra API and the cursor to the next page.
    ## Parameters (optional):
    - limit [integer, default 100]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - status [string, default None]: filter for status of retrieved objects. ex: "paid" or "registered"
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - cursor [string, default None]: cursor returned on the previous page function call
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - list of IssuingInvoices objects with updated attributes
    - cursor to retrieve the next page of IssuingInvoices objects
    """
    return rest.get_page(
        resource=_resource,
        status=status,
        after=check_datetime(after),
        before=check_datetime(before),
        tags=tags,
        limit=limit,
        cursor=cursor,
        user=user,
    )
