from ...utils import rest
from ...utils.api import from_api_json
from ...utils.resource import Resource
from ...utils.checks import check_datetime, check_date
from..__issuingcard import _resource as _issuing_card_resource


class Log(Resource):
    """# issuingcard.Log object
    Every time a IssuingCard entity is updated, a corresponding issuingcard.Log
    is generated for the entity. This log is never generated by the
    user, but it can be retrieved to check additional information
    on the IssuingCard.
    ## Attributes:
    - id [string]: unique id returned when the log is created. ex: "5656565656565656"
    - card [IssuingCard]: IssuingCard entity to which the log refers to.
    - errors [list of strings]: list of errors linked to this IssuingCard event
    - type [string]: type of the IssuingCard event which triggered the log creation. ex: "created" or "blocked"
    - created [datetime.datetime]: creation datetime for the log. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, id, created, type, card):
        Resource.__init__(self, id=id)

        self.type = type
        self.card = from_api_json(_issuing_card_resource, card)
        self.created = check_datetime(created)


_resource = {"class": Log, "name": "IssuingCardLog"}


def get(id, user=None):
    """# Retrieve a specific issuingcard.Log
    Receive a single issuingcard.Log object previously created by the Stark Infra API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - issuingcard.Log object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def query(ids=None, cardIds=None, types=None, after=None, before=None, limit=None, user=None):
    """# Retrieve issuingcard.Log
    Receive a generator of issuingcard.Log objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - types [list of strings, default None]: filter for log event types. ex: "paid" or "registered"
    - card_ids [list of strings, default None]: list of IssuingCard ids to filter logs. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - generator of issuingcard.Log objects with updated attributes
    """
    return rest.get_stream(
        resource=_resource,
        ids=ids,
        cardIds=cardIds,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        types=types,
        user=user,
    )


def page(ids=None, card_ids=None, types=None, after=None, before=None, cursor=None, limit=None, user=None):
    """# Retrieve paged issuingcard.Log
    Receive a list of up to 100 issuingcard.Log objects previously created in the Stark Infra API and the cursor to the next page.
    Use this function instead of query if you want to manually page your requests.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - limit [integer, default 100]: maximum number of objects to be retrieved. It must be an integer between 1 and 100. ex: 50
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - types [list of strings, default None]: filter for log event types. ex: "paid" or "registered"
    - card_ids [list of strings, default None]: list of IssuingCard ids to filter logs. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - list of issuingcard.Log objects with updated attributes
    - cursor to retrieve the next page of issuingcard.Log objects
    """
    return rest.get_page(
        resource=_resource,
        ids=ids,
        card_ids=card_ids,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        types=types,
        cursor=cursor,
        user=user,
    )
