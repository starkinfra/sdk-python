from ..utils import rest
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime, check_date


class PixKeyHolmes(Resource):
    """# PixKeyHolmes object
    PixKeyHolmes are used to investigate the registration status of a Pix Key
    in the Central Bank's DICT.
    When you initialize a PixKeyHolmes, the entity will not be automatically
    created in the Stark Infra API. The 'create' function sends the objects
    to the Stark Infra API and returns the list of created objects.
    ## Parameters (required):
    - key_id [string]: Pix Key to be investigated. ex: "+5511989898989", "11.222.333/0001-00", "valid@sandbox.com"
    ## Parameters (optional):
    - tags [list of strings, default []]: list of strings for reference when searching for PixKeyHolmes. ex: ["employees", "monthly"]
    ## Attributes (return-only):
    - id [string]: unique id returned when the PixKeyHolmes is created. ex: "5656565656565656"
    - result [string]: result of the investigation after the case is solved. ex: "registered", "unregistered"
    - status [string]: current PixKeyHolmes status. ex: "created", "solving", "solved", "failed"
    - created [datetime.datetime]: creation datetime for the PixKeyHolmes. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - updated [datetime.datetime]: latest update datetime for the PixKeyHolmes. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, key_id, tags=None, id=None, result=None, status=None, created=None, updated=None):
        Resource.__init__(self, id=id)

        self.key_id = key_id
        self.tags = tags
        self.result = result
        self.status = status
        self.created = check_datetime(created)
        self.updated = check_datetime(updated)


_resource = {"class": PixKeyHolmes, "name": "PixKeyHolmes"}


def create(holmes, user=None):
    """# Create PixKeyHolmes
    Send a list of PixKeyHolmes objects for creation at the Stark Infra API
    ## Parameters (required):
    - holmes [list of PixKeyHolmes objects]: list of PixKeyHolmes objects to be created in the API
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of PixKeyHolmes objects with updated attributes
    """
    return rest.post_multi(resource=_resource, entities=holmes, user=user)


def query(limit=None, after=None, before=None, status=None, tags=None, ids=None, user=None):
    """# Retrieve PixKeyHolmes
    Receive a generator of PixKeyHolmes objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None]: date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None]: date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. ex: ["created", "solving", "solved", "failed"]
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - generator of PixKeyHolmes objects with updated attributes
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


def page(cursor=None, limit=None, after=None, before=None, status=None, tags=None, ids=None, user=None):
    """# Retrieve paged PixKeyHolmes
    Receive a list of up to 100 PixKeyHolmes objects previously created in the Stark Infra API and the cursor to the next page.
    Use this function instead of query if you want to manually page your requests.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - limit [integer, default 100]: maximum number of objects to be retrieved. It must be an integer between 1 and 100. ex: 50
    - after [datetime.date or string, default None]: date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None]: date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. ex: ["created", "solving", "solved", "failed"]
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of PixKeyHolmes objects with updated attributes
    - cursor to retrieve the next page of PixKeyHolmes objects
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
