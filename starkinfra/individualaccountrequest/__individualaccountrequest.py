from copy import deepcopy
from ..utils import rest
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime, check_date
from starkcore.utils.api import from_api_json
from .__address import Address
from .__address import resource as _address_resource


class IndividualAccountRequest(Resource):
    """# IndividualAccountRequest object
    An IndividualAccountRequest represents an individual account request. It can be created to request
    the opening of an account for a specific individual by providing their required information.
    When you initialize an IndividualAccountRequest, the entity will not be automatically
    created in the Stark Infra API. The 'create' function sends the objects
    to the Stark Infra API and returns the list of created objects.
    ## Parameters (required):
    - name [string]: individual's full name. ex: "Edward Stark".
    - tax_id [string]: individual's tax ID (CPF). ex: "012.345.678-90"
    - address [individualaccountrequest.Address object]: individual's structured residential address. ex: Address(street="Rua do Estilo Barroco", number="648", neighborhood="Santo Amaro", city="Sao Paulo", state="SP", zip_code="05724005")
    - income [integer]: individual's income in cents. ex: 1000000 (= R$ 10,000.00)
    ## Parameters (optional):
    - tags [list of strings, default []]: list of strings for reference when searching for IndividualAccountRequests. ex: ["employees", "monthly"]
    ## Attributes (return-only):
    - id [string]: unique id returned when the IndividualAccountRequest is created. ex: "5656565656565656"
    - account_type [string]: type of account requested. ex: "individual"
    - flags [list of strings]: list of flags associated with the IndividualAccountRequest.
    - status [string]: current status of the IndividualAccountRequest. ex: "approved", "created", "denied", "processing", "updated"
    - created [datetime.datetime]: creation datetime for the IndividualAccountRequest. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - updated [datetime.datetime]: latest update datetime for the IndividualAccountRequest. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, name, tax_id, address, income, tags=None, id=None, account_type=None, flags=None, status=None,
                 created=None, updated=None):
        Resource.__init__(self, id=id)

        self.name = name
        self.tax_id = tax_id
        self.address = _parse_address(address)
        self.income = income
        self.tags = tags
        self.account_type = account_type
        self.flags = flags
        self.status = status
        self.created = check_datetime(created)
        self.updated = check_datetime(updated)


_resource = {"class": IndividualAccountRequest, "name": "IndividualAccountRequest"}


def _parse_address(address):
    if address is None:
        return None
    if isinstance(address, Address):
        return address
    return from_api_json(_address_resource, address)


def create(requests, user=None):
    """# Create IndividualAccountRequests
    Send a list of IndividualAccountRequest objects for creation at the Stark Infra API
    ## Parameters (required):
    - requests [list of IndividualAccountRequest objects]: list of IndividualAccountRequest objects to be created in the API
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of IndividualAccountRequest objects with updated attributes
    """
    # Output-only fields are populated by the API on response. They are accepted by
    # the constructor (so a response round-trips) but the API rejects them on POST
    # with "Unknown parameters in JSON: ...", so they are nulled here before the
    # payload is built (the core serializer drops None-valued keys). A deep copy
    # keeps the caller's objects intact.
    output_only_fields = ["id", "account_type", "flags", "status", "created", "updated"]
    stripped = []
    for request in requests:
        request = deepcopy(request)
        for field in output_only_fields:
            setattr(request, field, None)
        stripped.append(request)
    return rest.post_multi(resource=_resource, entities=stripped, user=user)


def get(id, user=None):
    """# Retrieve a specific IndividualAccountRequest
    Receive a single IndividualAccountRequest object previously created in the Stark Infra API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - IndividualAccountRequest object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def query(limit=None, status=None, tags=None, ids=None, after=None, before=None, user=None):
    """# Retrieve IndividualAccountRequests
    Receive a generator of IndividualAccountRequest objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. ex: ["created", "canceled", "processing", "failed", "success"]
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - generator of IndividualAccountRequest objects with updated attributes
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
    """# Retrieve paged IndividualAccountRequests
    Receive a list of up to 100 IndividualAccountRequest objects previously created in the Stark Infra API and the cursor to the next page.
    Use this function instead of query if you want to manually page your requests.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - limit [integer, default 100]: maximum number of objects to be retrieved. It must be an integer between 1 and 100. ex: 50
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. ex: ["created", "canceled", "processing", "failed", "success"]
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of IndividualAccountRequest objects with updated attributes
    - cursor to retrieve the next page of IndividualAccountRequest objects
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


def update(id, status=None, name=None, tax_id=None, address=None, income=None, tags=None, user=None):
    """# Update IndividualAccountRequest entity
    Update an IndividualAccountRequest by passing id.
    ## Parameters (required):
    - id [string]: IndividualAccountRequest id. ex: '5656565656565656'
    ## Parameters (optional):
    - status [string]: You may send IndividualAccountRequests to validation by passing 'processing' in the status
    - name [string]: individual's full name. ex: "Edward Stark"
    - tax_id [string]: individual's tax ID (CPF). ex: "012.345.678-90"
    - address [individualaccountrequest.Address object]: individual's structured residential address. Replaces the address object as a whole. ex: Address(street="Avenida Paulista", number="1000", neighborhood="Bela Vista", city="Sao Paulo", state="SP", zip_code="01310100")
    - income [integer]: individual's income in cents. ex: 1000000 (= R$ 10,000.00)
    - tags [list of strings]: list of strings for reference when searching for IndividualAccountRequests. ex: ["employees", "monthly"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - target IndividualAccountRequest with updated attributes
    """
    payload = {
        "status": status,
        "name": name,
        "tax_id": tax_id,
        "address": address,
        "income": income,
        "tags": tags,
    }
    return rest.patch_id(resource=_resource, id=id, user=user, payload=payload)
