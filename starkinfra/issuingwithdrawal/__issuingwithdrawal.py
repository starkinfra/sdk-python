from starkbank.utils.resource import Resource
from starkbank.utils.checks import check_datetime
from starkbank.utils import rest


class IssuingWithdrawal(Resource):

    def __init__(self, id=None, amount=None, description=None, transaction_id=None, issuing_transaction_id=None,
                 external_id=None, tags=None, updated=None, created=None):
        super().__init__(id)
        self.amount = amount
        self.description = description
        self.transaction_id = transaction_id
        self.issuing_transaction_id = issuing_transaction_id
        self.external_id = external_id
        self.tags = tags
        self.updated = check_datetime(updated)
        self.created = check_datetime(created)


_resource = {"class": IssuingWithdrawal, "name": "IssuingWithdrawal"}


def create(withdrawals, user=None):
    """# Create Invoices
    Send a list of Invoice objects for creation in the Stark Bank API
    ## Parameters (required):
    - invoices [list of Invoice objects]: list of Invoice objects to be created in the API
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkbank.user was set before function call
    ## Return:
    - list of Invoice objects with updated attributes
    """
    return rest.post_single(resource=_resource, entity=withdrawals, user=user)


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


def query(external_ids=None, after=None, before=None, limit=None, tags=None, user=None):
    return rest.get_stream(
        resource=_resource,
        external_ids=external_ids,
        after=check_datetime(after),
        before=check_datetime(before),
        tags=tags,
        limit=limit,
        user=user,
    )


def page(external_ids=None, after=None, before=None, limit=None, tags=None, cursor=None, user=None):
    return rest.get_page(
        resource=_resource,
        external_ids=external_ids,
        after=check_datetime(after),
        before=check_datetime(before),
        tags=tags,
        limit=limit,
        cursor=cursor,
        user=user,
    )
