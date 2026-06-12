from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_date, check_datetime
from ..utils import rest


class IssuingStockRule(Resource):
    """# IssuingStockRule object
    The IssuingStockRule object displays the notification rules of a specific IssuingStock.
    When the stock balance reaches the minimum balance, the recipients informed in the rule are notified.
    ## Parameters (required):
    - minimum_balance [integer]: stock balance threshold that triggers a notification. ex: 10000
    - stock_id [string]: IssuingStock unique id to which the rule is linked. ex: "5656565656565656"
    ## Parameters (optional):
    - tags [list of strings, default None]: list of strings for tagging. ex: ["card", "corporate"]
    - emails [list of strings, default None]: list of emails to be notified when the stock reaches the minimum balance. ex: ["john.doe@enterprise.com"]
    - phones [list of strings, default None]: list of phones to be notified when the stock reaches the minimum balance. ex: ["+55 (11) 91234 5678"]
    ## Attributes (return-only):
    - id [string]: unique id returned when IssuingStockRule is created. ex: "5656565656565656"
    - status [string]: current IssuingStockRule status. ex: "active", "canceled"
    - updated [datetime.datetime]: latest update datetime for the IssuingStockRule. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - created [datetime.datetime]: creation datetime for the IssuingStockRule. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, minimum_balance, stock_id, tags=None, emails=None, phones=None, id=None,
                 status=None, created=None, updated=None):
        Resource.__init__(self, id=id)

        self.minimum_balance = minimum_balance
        self.stock_id = stock_id
        self.tags = tags
        self.emails = emails
        self.phones = phones
        self.status = status
        self.updated = check_datetime(updated)
        self.created = check_datetime(created)


_resource = {"class": IssuingStockRule, "name": "IssuingStockRule"}


def create(rules, user=None):
    """# Create IssuingStockRules
    Send a list of IssuingStockRule objects for creation at the Stark Infra API
    ## Parameters (required):
    - rules [list of IssuingStockRule objects]: list of IssuingStockRule objects to be created in the API
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of IssuingStockRule objects with updated attributes
    """
    return rest.post_multi(resource=_resource, entities=rules, user=user)


def get(id, user=None):
    """# Retrieve a specific IssuingStockRule
    Receive a single IssuingStockRule object previously created in the Stark Infra API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - IssuingStockRule object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def query(limit=None, after=None, before=None, status=None, stock_ids=None, ids=None,
          tags=None, user=None):
    """# Retrieve IssuingStockRules
    Receive a generator of IssuingStockRule objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. ex: ["active", "canceled"]
    - stock_ids [list of strings, default None]: list of stock_ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["card", "corporate"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - generator of IssuingStockRule objects with updated attributes
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
    """# Retrieve paged IssuingStockRules
    Receive a list of up to 100 IssuingStockRule objects previously created in the Stark Infra API and the cursor to the next page.
    Use this function instead of query if you want to manually page your requests.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call.
    - limit [integer, default 100]: maximum number of objects to be retrieved. Max = 100. ex: 35
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. ex: ["active", "canceled"]
    - stock_ids [list of strings, default None]: list of stock_ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["card", "corporate"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of IssuingStockRule objects with updated attributes
    - cursor to retrieve the next page of IssuingStockRule objects
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


def update(id, minimum_balance=None, tags=None, emails=None, phones=None, user=None):
    """# Update IssuingStockRule entity
    Update an IssuingStockRule by passing its id.
    ## Parameters (required):
    - id [string]: IssuingStockRule id. ex: '5656565656565656'
    ## Parameters (optional):
    - minimum_balance [integer, default None]: stock balance threshold that triggers a notification. ex: 10000
    - tags [list of strings, default None]: list of strings for tagging. ex: ["card", "corporate"]
    - emails [list of strings, default None]: list of emails to be notified when the stock reaches the minimum balance. ex: ["john.doe@enterprise.com"]
    - phones [list of strings, default None]: list of phones to be notified when the stock reaches the minimum balance. ex: ["+55 (11) 91234 5678"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - target IssuingStockRule with updated attributes
    """
    payload = {
        "minimum_balance": minimum_balance,
        "tags": tags,
        "emails": emails,
        "phones": phones,
    }
    return rest.patch_id(resource=_resource, id=id, user=user, payload=payload)


def cancel(id, user=None):
    """# Cancel an IssuingStockRule entity
    Cancel an IssuingStockRule entity previously created in the Stark Infra API
    ## Parameters (required):
    - id [string]: IssuingStockRule unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - canceled IssuingStockRule object
    """
    return rest.delete_id(resource=_resource, id=id, user=user)
