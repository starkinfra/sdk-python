from starkcore.utils.checks import check_datetime, check_date
from ..__reversalrequest import _resource as _reversalrequest_resource
from starkcore.utils.resource import Resource
from starkcore.utils.api import from_api_json
from ...utils import rest


class Log(Resource):
    """# ReversalRequest.Log object
    Every time a ReversalRequest entity is modified, a corresponding ReversalRequest.Log
    is generated for the entity. This log is never generated by the user.
    ## Attributes:
    - id [string]: unique id returned when the log is created. ex: "5656565656565656"
    - created [datetime.datetime]: creation datetime for the log. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - type [string]: type of the ReversalRequest event which triggered the log creation. 
    - errors [list of strings]: list of errors linked to this ReversalRequest event
    - request [ReversalRequest]: ReversalRequest entity to which the log refers to.
    """
    def __init__(self, id, created, type, errors, request):
        Resource.__init__(self, id=id)

        self.created = check_datetime(created)
        self.type = type
        self.errors = errors
        self.request = from_api_json(_reversalrequest_resource, request)


_resource = {"class": Log, "name": "ReversalRequestLog"}


def get(id, user=None):
    """# Retrieve a specific ReversalRequest.Log
    Receive a single ReversalRequest.Log object previously created by the Stark Infra API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - ReversalRequest.Log object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def query(ids=None, limit=None, after=None, before=None, types=None, request_ids=None, user=None):
    """# Retrieve ReversalRequest.Logs
    Receive a generator of ReversalRequest.Log objects previously created in the Stark Infra API
    ## Parameters (optional):
    - ids [list of strings, default None]: Log ids to filter ReversalRequest Logs. ex: ["5656565656565656"]
    - limit [integer, default None]: maximum number of objects to be retrieved. Max = 100. ex: 35
    - after [datetime.date or string, default None]: date filter for objects created after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None]: date filter for objects created before a specified date. ex: datetime.date(2020, 3, 10)
    - types [list of strings, default None]: filter retrieved objects by types. ex: "success" or "failed"
    - request_ids [list of strings, default None]: list of ReversalRequest IDs to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - generator of ReversalRequest.Log objects with updated attributes
    """
    return rest.get_stream(
        resource=_resource,
        ids=ids,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        types=types,
        request_ids=request_ids,
        user=user,
    )


def page(cursor=None, ids=None, limit=None, after=None, before=None, types=None, request_ids=None, user=None):
    """# Retrieve paged ReversalRequest.Logs
    Receive a list of up to 100 ReversalRequest.Log objects previously created in the Stark Infra API and the cursor to the next page.
    Use this function instead of query if you want to manually page your requests.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - ids [list of strings, default None]: Log ids to filter ReversalRequest Logs. ex: ["5656565656565656"]
    - limit [integer, default None]: maximum number of objects to be retrieved. Max = 100. ex: 35
    - after [datetime.date or string, default None]: date filter for objects created after a specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None]: date filter for objects created before a specified date. ex: datetime.date(2020, 3, 10)
    - types [list of strings, default None]: filter retrieved objects by types. ex: "success" or "failed"
    - request_ids [list of strings, default None]: list of ReversalRequest IDs to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - list of ReversalRequest.Log objects with updated attributes
    - cursor to retrieve the next page of ReversalRequest.Log objects
    """
    return rest.get_page(
        resource=_resource,
        cursor=cursor,
        ids=ids,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        types=types,
        request_ids=request_ids,
        user=user,
    )
