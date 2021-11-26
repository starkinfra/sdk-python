from starkbank.utils.resource import Resource
from starkbank.utils.checks import check_datetime

from starkbank.utils import rest


class IssuingCard(Resource):
    """# IssuingCard object
    The IssuingCard object displays the informations of Cards created to your Workspace.
    ## Attributes (return-only):
    - id [string, default None]: unique id returned when Balance is created. ex: "5656565656565656"
    - holder_id [string, default None]: card holder unique id.
    - holder_name [string, default None]: card holder name.
    - type [string, default None]: card type. ex: "virtual"
    - display_name [string, default None]: card displayed name
    - status [string, default None]: card status
    - rules [list of dictionaries, default None]: list of dictionaries with "amount": int, "currencyCode": string, "id": string, "interval": string, "name": string pairs
    - street_line_1 [string, default None]:
    - street_line_2 [string, default None]:
    - city [string, default None]:
    - state_code [string, default None]:
    - zip_code [string, default None]:
    - tags [string, default None]:
    - number [string, default None]:
    - security_code [string, default None]:
    - expiration [string, default None]:
    - updated [datetime.datetime, default None]: latest update datetime for the bin. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - created [datetime.datetime, default None]: creation datetime for the bin. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, id=None, holder_id=None, holder_name=None, type=None, display_name=None, status=None,
                 rules=None, street_line_1=None, street_line_2=None, city=None, state_code=None, zip_code=None,
                 tags=None, created=None, updated=None, number=None, security_code=None, expiration=None):
        super().__init__(id)
        self.id = id
        self.holder_id = holder_id
        self.holder_name = holder_name
        self.type = type
        self.display_name = display_name
        self.status = status
        self.rules = rules
        self.street_line_1 = street_line_1
        self.street_line_2 = street_line_2
        self.city = city
        self.state_code = state_code
        self.zip_code = zip_code
        self.tags = tags
        self.created = check_datetime(created)
        self.updated = check_datetime(updated)
        self.number = number
        self.security_code = security_code
        self.expiration = expiration


_resource = {"class": IssuingCard, "name": "IssuingCard"}


def create(cards, user=None):
    """# Create Invoices
    Send a list of Invoice objects for creation in the Stark Bank API
    ## Parameters (required):
    - invoices [list of Invoice objects]: list of Invoice objects to be created in the API
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkbank.user was set before function call
    ## Return:
    - list of Invoice objects with updated attributes
    """
    return rest.post_multi(resource=_resource, entities=cards, user=user)


def query(status=None, types=None, holder_ids=None, after=None, before=None, tags=None, ids=None, limit=None, expand=None, user=None):
    return rest.get_stream(
        resource=_resource,
        status=status,
        types=types,
        holder_ids=holder_ids,
        after=check_datetime(after),
        before=check_datetime(before),
        tags=tags,
        ids=ids,
        limit=limit,
        expand=expand,
        user=user,
    )


def page(status=None, types=None, holder_ids=None, after=None, before=None, tags=None, ids=None,
         limit=None, cursor=None, expand=None, user=None):
    return rest.get_page(
        resource=_resource,
        status=status,
        types=types,
        holder_ids=holder_ids,
        after=check_datetime(after),
        before=check_datetime(before),
        tags=tags,
        ids=ids,
        limit=limit,
        cursor=cursor,
        expand=expand,
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


def update(id, status=None, display_name=None, rules=None, tags=None, user=None):
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
        "display_name": display_name,
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
