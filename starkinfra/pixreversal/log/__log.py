from ...utils import rest
from starkcore.utils.resource import Resource
from starkcore.utils.api import from_api_json
from starkcore.utils.checks import check_datetime, check_date
from ..__pixreversal import _resource as _pixreversal_resource


class Log(Resource):
    """# PixReversal.Log object
    Every time a PixReversal entity is modified, a corresponding PixReversal.Log
    is generated for the entity. This log is never generated by the user.
    ## Attributes:
    - id [string]: unique id returned when the log is created. ex: "5656565656565656"
    - reversal [PixReversal object]: PixReversal entity to which the log refers to.
    - type [string]: type of the PixReversal event which triggered the log creation. ex: "sent", "denied", "failed", "created", "success", "approved", "credited", "refunded", "processing"
    - errors [list of strings]: list of errors linked to this PixReversal event
    - created [datetime.datetime]: creation datetime for the log. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """
    def __init__(self, id, reversal, type, errors, created):
        Resource.__init__(self, id=id)

        self.reversal = from_api_json(_pixreversal_resource, reversal)
        self.type = type
        self.errors = errors
        self.created = check_datetime(created)


_resource = {"class": Log, "name": "PixReversalLog"}


def get(id, user=None):
    """# Retrieve a specific PixReversal.Log by its id
    Receive a single PixReversal.Log object previously created by the Stark Infra API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - PixReversal.Log object that corresponds to the given id.
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def query(limit=None, after=None, before=None, types=None, reversal_ids=None, user=None):
    """# Retrieve PixReversal.Log objects
    Receive a generator of PixReversal.Log objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None]: date filter for objects created after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None]: date filter for objects created before a specified date. ex: datetime.date(2020, 3, 10)
    - types [list of strings, default None]: filter retrieved objects by types. Options: ["sent", "denied", "failed", "created", "success", "approved", "credited", "refunded", "processing"]
    - reversal_ids [list of strings, default None]: list of PixReversal IDs to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - generator of PixReversal.Log objects with updated attributes
    """
    return rest.get_stream(
        resource=_resource,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        types=types,
        reversal_ids=reversal_ids,
        user=user,
    )


def page(cursor=None, limit=None, after=None, before=None, types=None, reversal_ids=None, user=None):
    """# Retrieve paged PixReversal.Log objects
    Receive a list of up to 100 PixReversal.Log objects previously created in the Stark Infra API and the cursor to the next page.
    Use this function instead of query if you want to manually page your reversals.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - limit [integer, default 100]: maximum number of objects to be retrieved. Max = 100. ex: 35
    - after [datetime.date or string, default None]: date filter for objects created after a specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None]: date filter for objects created before a specified date. ex: datetime.date(2020, 3, 10)
    - types [list of strings, default None]: filter retrieved objects by types. Options: ["sent", "denied", "failed", "created", "success", "approved", "credited", "refunded", "processing"]
    - reversal_ids [list of strings, default None]: list of PixReversal IDs to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of pixreversal.Log objects with updated attributes
    - cursor to retrieve the next page of pixreversal.Log objects
    """
    return rest.get_page(
        resource=_resource,
        cursor=cursor,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        types=types,
        reversal_ids=reversal_ids,
        user=user,
    )
