from ..utils import rest
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime, check_date


class IndividualIdentity(Resource):
    """# IndividualIdentity object
    An IndividualDocument represents an individual to be validated. It can have several individual documents attached
    to it, which are used to validate the identity of the individual. Once an individual identity is created, individual
    documents must be attached to it using the created method of the individual document resource. When all the required
    individual documents are attached to an individual identity it can be sent to validation by patching its status to 
    processing.
    When you initialize a IndividualIdentity, the entity will not be automatically
    created in the Stark Infra API. The 'create' function sends the objects
    to the Stark Infra API and returns the list of created objects.
    ## Parameters (required):
    - name [string]: individual's full name. ex: "Edward Stark".
    - tax_id [string]: individual's tax ID (CPF). ex: "594.739.480-42"
    ## Parameters (optional):
    - tags [list of strings, default []]: list of strings for reference when searching for IndividualIdentities. ex: ["employees", "monthly"]
    ## Attributes (return-only):
    - id [string]: unique id returned when the IndividualIdentity is created. ex: "5656565656565656"
    - status [string]: current status of the IndividualIdentity. ex: "created", "canceled", "processing", "failed", "success"
    - created [datetime.datetime]: creation datetime for the IndividualIdentity. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, name, tax_id, tags=None, id=None, status=None, created=None):
        Resource.__init__(self, id=id)

        self.name = name
        self.tax_id = tax_id
        self.tags = tags
        self.status = status
        self.created = check_datetime(created)


_resource = {"class": IndividualIdentity, "name": "IndividualIdentity"}


def create(identities, user=None):
    """# Create IndividualIdentities
    Send a list of IndividualIdentity objects for creation at the Stark Infra API
    ## Parameters (required):
    - identities [list of IndividualIdentity objects]: list of IndividualIdentity objects to be created in the API
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of IndividualIdentity objects with updated attributes
    """
    return rest.post_multi(resource=_resource, entities=identities, user=user)


def get(id, user=None):
    """# Retrieve a specific IndividualIdentity
    Receive a single IndividualIdentity object previously created in the Stark Infra API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - IndividualIdentity object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def query(limit=None, status=None, tags=None, ids=None, after=None, before=None, user=None):
    """# Retrieve IndividualIdentities
    Receive a generator of IndividualIdentity objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. ex: ["created", "canceled", "processing", "failed", "success"]
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - generator of IndividualIdentity objects with updated attributes
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
    """# Retrieve paged IndividualIdentities
    Receive a list of up to 100 IndividualIdentity objects previously created in the Stark Infra API and the cursor to the next page.
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
    - list of IndividualIdentity objects with updated attributes
    - cursor to retrieve the next page of IndividualIdentity objects
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


def update(id, status, user=None):
    """# Update IndividualIdentity entity
    Update an IndividualIdentity by passing id.
    ## Parameters (required):
    - id [string]: IndividualIdentity id. ex: '5656565656565656'
    - status [string]: You may send IndividualDocuments to validation by passing 'processing' in the status
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - target IndividualIdentity with updated attributes
    """
    payload = {
        "status": status
    }
    return rest.patch_id(resource=_resource, id=id, user=user, payload=payload)


def cancel(id, user=None):
    """# Cancel a IndividualIdentity entity
    Cancel a IndividualIdentity entity previously created in the Stark Infra API
    ## Parameters (required):
    - id [string]: IndividualIdentity unique id. ex: "6306109539221504"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - canceled IndividualIdentity object
    """
    return rest.delete_id(resource=_resource, id=id, user=user)
