from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_date, check_datetime
from ..utils import rest


class IssuingRestock(Resource):
    """# IssuingRestock object
    The IssuingRestock object displays the information of the restock orders created in your Workspace. 
    This resource place a restock order for a specific IssuingStock object.
    ## Parameters (required):
    - count [integer]: number of restocks to be restocked. ex: 100
    - stock_id [string]: IssuingStock unique id ex: "5136459887542272"
    ## Parameters (optional):
    - tags [list of strings, default None]: list of strings for tagging. ex: ["card", "corporate"]
    ## Attributes (return-only):
    - id [string]: unique id returned when IssuingRestock is created. ex: "5656565656565656"
    - status [string]: current IssuingRestock status. ex: "created", "processing", "confirmed"
    - updated [datetime.datetime]: latest update datetime for the IssuingRestock. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - created [datetime.datetime]: creation datetime for the IssuingRestock. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, count, stock_id, tags=None, id=None, status=None, created=None, updated=None):
        Resource.__init__(self, id=id)

        self.count = count
        self.stock_id = stock_id
        self.tags = tags
        self.status = status
        self.updated = check_datetime(updated)
        self.created = check_datetime(created)


_resource = {"class": IssuingRestock, "name": "IssuingRestock"}


def create(restocks, user=None):
    """# Create IssuingRestocks
    Send a list of IssuingRestock objects for creation at the Stark Infra API
    ## Parameters (required):
    - restocks [list of IssuingRestock objects]: list of IssuingRestock objects to be created in the API
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of IssuingRestock objects with updated attributes
    """
    return rest.post_multi(resource=_resource, entities=restocks, user=user)


def query(limit=None, after=None, before=None, status=None, stock_ids=None, ids=None, 
          tags=None, user=None):
    """# Retrieve IssuingRestocks
    Receive a generator of IssuingRestock objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. ex: ["created", "processing", "confirmed"]
    - stock_ids [list of string, default None]: list of stock_ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["card", "corporate"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - generator of IssuingRestock objects with updated attributes
    """
    return rest.get_stream(
        resource=_resource,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        status=status,
        stock_ids=stock_ids,
        ids=ids,
        tags=tags,
        user=user,
    )


def page(cursor=None, limit=None, after=None, before=None, status=None, stock_ids=None, 
         ids=None, tags=None, user=None):
    """# Retrieve paged IssuingRestocks
    Receive a list of up to 100 IssuingRestock objects previously created in the Stark Infra API and the cursor to the next page.
    Use this function instead of query if you want to manually page your requests.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call.
    - limit [integer, default 100]: maximum number of objects to be retrieved. Max = 100. ex: 35
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. ex: ["created", "processing", "confirmed"]
    - stock_ids [list of string, default None]: list of stock_ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["card", "corporate"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of IssuingRestock objects with updated attributes
    - cursor to retrieve the next page of IssuingRestock objects
    """
    return rest.get_page(
        resource=_resource,
        cursor=cursor,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        status=status,
        stock_ids=stock_ids,
        ids=ids,
        tags=tags,
        user=user,
    )


def get(id, user=None):
    """# Retrieve a specific IssuingRestock
    Receive a single IssuingRestock object previously created in the Stark Infra API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - IssuingRestock object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)
