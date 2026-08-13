from ..utils import rest
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime, check_date
from starkcore.utils.api import from_api_json
from .__address import Address
from .__address import resource as _address_resource
from .__owner import Owner
from .__owner import resource as _owner_resource


class BusinessAccountRequest(Resource):
    """# BusinessAccountRequest object
    You can create a business account request to request an account for a specific company, opening the
    account with identity verification by webview for each of its owners.
    When you initialize a BusinessAccountRequest, the entity will not be automatically
    created in the Stark Infra API. The 'create' function sends the objects
    to the Stark Infra API and returns the list of created objects.
    ## Parameters (required):
    - address [businessaccountrequest.Address object]: company's structured address. ex: Address(street="Av. Faria Lima", number="2000", neighborhood="Itaim Bibi", city="Sao Paulo", state="SP", zip_code="04538-132")
    - revenue [integer]: company's annual revenue in cents. ex: 100000000 (= R$ 1,000,000.00)
    - name [string]: company's legal name (minimum 5 characters). ex: "Stark Bank S.A."
    - tax_id [string]: company's tax ID (CNPJ). ex: "20.018.183/0001-80"
    - owners [list of businessaccountrequest.Owner objects]: list of 1 to 10 company owners. ex: [Owner(tax_id="012.345.678-90", name="Jamie Lannister", role="partner")]
    ## Parameters (optional):
    - tags [list of strings, default None]: list of strings for reference when searching for BusinessAccountRequests. ex: ["employees", "monthly"]
    ## Attributes (return-only):
    - id [string]: unique id returned when the BusinessAccountRequest is created. ex: "5656565656565656"
    - account_type [string]: type of the account. ex: "business"
    - flags [list of dictionaries]: flags that motivated the decision, populated when the request is denied. Each flag has a code and a message.
    - status [string]: current status of the BusinessAccountRequest. Options: "created", "processing", "approved", "denied"
    - created [datetime.datetime]: creation datetime for the BusinessAccountRequest. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - updated [datetime.datetime]: latest update datetime for the BusinessAccountRequest. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, address, revenue, name, tax_id, owners, tags=None, id=None, account_type=None,
                 flags=None, status=None, created=None, updated=None):
        Resource.__init__(self, id=id)

        self.address = _parse_address(address)
        self.revenue = revenue
        self.name = name
        self.tax_id = tax_id
        self.owners = _parse_owners(owners)
        self.tags = tags
        self.account_type = account_type
        self.flags = flags
        self.status = status
        self.created = check_datetime(created)
        self.updated = check_datetime(updated)


_resource = {"class": BusinessAccountRequest, "name": "BusinessAccountRequest"}


def _parse_address(address):
    if address is None:
        return None
    if isinstance(address, Address):
        return address
    return from_api_json(_address_resource, address)


def _parse_owner(owner):
    if isinstance(owner, Owner):
        return owner
    return from_api_json(_owner_resource, owner)


def _parse_owners(owners):
    if owners is None:
        return None
    return [_parse_owner(owner) for owner in owners]


def create(requests, user=None):
    """# Create BusinessAccountRequests
    Send a list of BusinessAccountRequest objects for creation at the Stark Infra API
    ## Parameters (required):
    - requests [list of BusinessAccountRequest objects]: list of BusinessAccountRequest objects to be created in the API
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of BusinessAccountRequest objects with updated attributes
    """
    return rest.post_multi(resource=_resource, entities=requests, user=user)


def get(id, user=None):
    """# Retrieve a specific BusinessAccountRequest
    Receive a single BusinessAccountRequest object previously created in the Stark Infra API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - BusinessAccountRequest object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def query(limit=None, status=None, tags=None, ids=None, after=None, before=None, user=None):
    """# Retrieve BusinessAccountRequests
    Receive a generator of BusinessAccountRequest objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings or string, default None]: filter for status of retrieved objects. A single value is also accepted. ex: ["created", "processing"] or "approved"
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - generator of BusinessAccountRequest objects with updated attributes
    """
    return rest.get_stream(
        resource=_resource,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        status=status,
        tags=tags,
        ids=ids,
        user=user,
    )


def page(cursor=None, limit=None, status=None, tags=None, ids=None, after=None, before=None, user=None):
    """# Retrieve paged BusinessAccountRequests
    Receive a list of up to 100 BusinessAccountRequest objects previously created in the Stark Infra API and the cursor to the next page.
    Use this function instead of query if you want to manually page your requests.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - limit [integer, default 100]: maximum number of objects to be retrieved. It must be an integer between 1 and 100. ex: 50
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings or string, default None]: filter for status of retrieved objects. A single value is also accepted. ex: ["created", "processing"] or "approved"
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of BusinessAccountRequest objects with updated attributes
    - cursor to retrieve the next page of BusinessAccountRequest objects
    """
    return rest.get_page(
        resource=_resource,
        cursor=cursor,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        status=status,
        tags=tags,
        ids=ids,
        user=user,
    )
