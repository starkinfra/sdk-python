from ...utils import rest
from ...utils.api import from_api_json
from ...utils.checks import check_datetime, check_date
from ...utils.resource import Resource
from ..__pixreversal import _resource as _pixreversal_resource


class Log(Resource):
    """# PixReversal.Log object
    Every time a PixReversal entity is modified, a corresponding PixReversal.Log
    is generated for the entity. This log is never generated by the
    user.
    ## Attributes:
    - created [datetime.datetime]: creation datetime for the log. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """
    def __init__(self, id, created, type, errors, reversal):
        Resource.__init__(self, id=id)

        self.created = check_datetime(created)
        self.type = type
        self.errors = errors
        self.request = from_api_json(_pixreversal_resource, reversal)


_resource = {"class": Log, "name": "PixReversalLog"}


def get(id, user=None):
    """# Retrieve a specific PixReversal.Log
    Receive a single PixReversal.Log object previously created by the Stark Infra API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - PixReversal.Log object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def query(limit=None, after=None, before=None, types=None, transfer_ids=None, user=None):
    """# Retrieve PixReversal.Logs
    Receive a generator of PixReversal.Log objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    ## Return:
    - generator of PixReversal.Log objects with updated attributes
    """
    return rest.get_stream(
        resource=_resource,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        types=types,
        transfer_ids=transfer_ids,
        user=user,
    )


def page(cursor=None, limit=None, after=None, before=None, types=None, transfer_ids=None, user=None):
    """# Retrieve paged PixReversal.Logs
    Receive a list of up to 100 PixReversal.Log objects previously created in the Stark Infra API and the cursor to the next page.
    Use this function instead of query if you want to manually page your requests.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    ## Return:
    - list of PixReversal.Log objects with updated attributes
    """
    return rest.get_page(
        resource=_resource,
        cursor=cursor,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        types=types,
        transfer_ids=transfer_ids,
        user=user,
    )
