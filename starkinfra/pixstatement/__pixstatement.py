from ..utils import rest
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime, check_date


class PixStatement(Resource):
    """# PixStatement object
    The PixStatement object stores information about all the transactions that
    happened on a specific day at your settlment account according to the Central Bank.
    It must be created by the user before it can be accessed.
    This feature is only available for direct participants.
    When you initialize a PixStatement, the entity will not be automatically
    created in the Stark Infra API. The 'create' function sends the objects
    to the Stark Infra API and returns the created object.
    ## Parameters (required):
    - after [datetime.date]: transactions that happened at this date are stored in the PixStatement, must be the same as before. ex: datetime.date(2020, 3, 10)
    - before [datetime.date]: transactions that happened at this date are stored in the PixStatement, must be the same as after. ex: datetime.date(2020, 3, 10)
    - type [string]: types of entities to include in statement. Options: ["interchange", "interchangeTotal", "transaction"]
    ## Attributes (return-only):
    - id [string]: unique id returned when the PixStatement is created. ex: "5656565656565656"
    - status [string]: current PixStatement status. ex: ["success", "failed"]
    - transaction_count [integer]: number of transactions that happened during the day that the PixStatement was requested. ex: 11
    - created [datetime.datetime]: creation datetime for the PixStatement. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - updated [datetime.datetime]: latest update datetime for the PixStatement. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, after, before, type, id=None, status=None, transaction_count=None, created=None, updated=None):
        Resource.__init__(self, id=id)

        self.after = check_date(after)
        self.before = check_date(before)
        self.type = type
        self.status = status
        self.transaction_count = transaction_count
        self.created = check_datetime(created)
        self.updated = check_datetime(updated)


_resource = {"class": PixStatement, "name": "PixStatement"}


def create(statement, user=None):
    """# Create a PixStatement object
    Create a PixStatement linked to your Workspace in the Stark Infra API
    ## Parameters (optional):
    - statement [PixStatement object]: PixStatement object to be created in the API.
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - PixStatement object with updated attributes.
    """
    return rest.post_single(resource=_resource, entity=statement, user=user)


def get(id, user=None):
    """# Retrieve a PixStatement object
    Retrieve the PixStatement object linked to your Workspace in the Stark Infra API by its id.
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - PixStatement object that corresponds to the given id.
    """
    return rest.get_id(id=id, resource=_resource, user=user)


def query(limit=None, ids=None, user=None):
    """# Retrieve PixStatements
    Receive a generator of PixStatement objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - generator of PixStatement objects with updated attributes
    """

    return rest.get_stream(
        resource=_resource,
        limit=limit,
        ids=ids,
        user=user,
    )


def page(cursor=None, limit=None, ids=None, user=None):
    """# Retrieve paged PixStatements
    Receive a list of up to 100 PixStatement objects previously created in the Stark Infra API
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - limit [integer, default 100]: maximum number of objects to be retrieved. Max = 100. ex: 35
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of PixStatement objects with updated attributes
    - cursor to retrieve the next page of PixStatement objects
    """
    return rest.get_page(
        resource=_resource,
        cursor=cursor,
        limit=limit,
        ids=ids,
        user=user,
    )


def csv(id, user=None):
    """# Retrieve a .csv PixStatement
    Retrieve a specific PixStatement by its ID in a .csv file.
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - .zip file containing a PixStatement in .csv format
    """
    return rest.get_content(resource=_resource, id=id, user=user, sub_resource_name="csv")
