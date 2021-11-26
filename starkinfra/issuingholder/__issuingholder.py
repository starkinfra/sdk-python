from ..utils import rest
from ..utils.resource import Resource
from ..utils.checks import check_datetime



class IssuingHolder(Resource):

    def __init__(self, id=None, external_id=None, name=None, rules=None, status=None, tags=None, tax_id=None,
                 updated=None, created=None):
        super().__init__(id)
        self.name = name
        self.tax_id = tax_id
        self.external_id = external_id
        self.status = status
        self.rules = rules
        self.tags = tags
        self.updated = check_datetime(updated)
        self.created = check_datetime(created)


_resource = {"class": IssuingHolder, "name": "IssuingHolder"}


def create(holders, user=None):
    """# Create Invoices
    Send a list of Invoice objects for creation in the Stark Bank API
    ## Parameters (required):
    - invoices [list of Invoice objects]: list of Invoice objects to be created in the API
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkbank.user was set before function call
    ## Return:
    - list of Invoice objects with updated attributes
    """
    return rest.post_multi(resource=_resource, entities=holders, user=user)


def query(limit=None, after=None, before=None, status=None, sort=None, tags=None, ids=None, user=None):
    return rest.get_stream(
        resource=_resource,
        limit=limit,
        after=check_datetime(after),
        before=check_datetime(before),
        sort=sort,
        status=status,
        tags=tags,
        ids=ids,
        user=user,
    )


def page(limit=None, after=None, before=None, status=None, sort=None, tags=None, ids=None, cursor=None, user=None):
    return rest.get_page(
        resource=_resource,
        limit=limit,
        after=check_datetime(after),
        before=check_datetime(before),
        sort=sort,
        status=status,
        tags=tags,
        ids=ids,
        cursor=cursor,
        user=user,
    )


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


def update(id, status=None, name=None, rules=None, tags=None, user=None):
    """# Update Invoice entity
    Update an Invoice by passing id, if it hasn't been paid yet.
    ## Parameters (required):
    - id [string]: Invoice id. ex: '5656565656565656'
    ## Parameters (optional):
    - status [string]: You may cancel the invoice by passing 'canceled' in the status
    - amount [string]: Nominal amount charged by the invoice. ex: 100 (R$1.00)
    - due [datetime.datetime or string, default now + 2 days]: Invoice due date in UTC ISO format. ex: "2020-10-28T17:59:26.249976+00:00"
    - expiration [integer or datetime.timedelta, default None]: time interval in seconds between the due date and the expiration date. ex 123456789
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkbank.user was set before function call
    ## Return:
    - target Invoice with updated attributes
    """
    payload = {
        "status": status,
        "name": name,
        "rules": rules,
        "tags": tags,
    }
    return rest.patch_id(resource=_resource, id=id, user=user, **payload)


def delete(id, user=None):
    """# Delete a Boleto entity
    Delete a Boleto entity previously created in the Stark Bank API
    ## Parameters (required):
    - id [string]: Boleto unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkbank.user was set before function call
    ## Return:
    - deleted Boleto object
    """
    return rest.delete_id(resource=_resource, id=id, user=user)
