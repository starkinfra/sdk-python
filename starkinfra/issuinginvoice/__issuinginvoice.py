from starkbank.utils.resource import Resource
from starkbank.utils.checks import check_datetime
from starkbank.utils import rest


class IssuingInvoice(Resource):

    def __init__(self, id=None, name=None, amount=None, tax_id=None, status=None, issuing_transaction_id=None,
                 tags=None, updated=None, created=None):
        super().__init__(id)
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
    """# Create Invoices
    Send a list of Invoice objects for creation in the Stark Bank API
    ## Parameters (required):
    - invoices [list of Invoice objects]: list of Invoice objects to be created in the API
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkbank.user was set before function call
    ## Return:
    - list of Invoice objects with updated attributes
    """
    return rest.post_single(resource=_resource,
                            entity=IssuingInvoice(amount=amount, name=name, tax_id=tax_id, tags=tags),
                            user=user)


def get(id, user=None):
    """# Retrieve a specific Invoice
    Receive a single Invoice object previously created in the Stark Bank API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkbank.user was set before function call
    ## Return:
    - Invoice object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def query(status=None, after=None, before=None, tags=None, limit=None, user=None):
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
