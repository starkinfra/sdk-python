from starkcore.error import Error
from starkcore.utils.api import from_api_json
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime, check_date
from ...utils import rest
from ..__issuingpurchase import _resource as _issuing_purchase_resource


class Log(Resource):
    """# issuingpurchase.Log object
    Every time an IssuingPurchase entity is updated, a corresponding issuingpurchase.Log
    is generated for the entity. This log is never generated by the
    user, but it can be retrieved to check additional information
    on the IssuingPurchase.
    ## Attributes (return-only):
    - id [string]: unique id returned when the log is created. ex: "5656565656565656"
    - purchase [IssuingPurchase]: IssuingPurchase entity to which the log refers to.
    - installment [integer]: number of the installment that is being confirmed.
    - issuing_transaction_id [string]: transaction ID related to the IssuingCard.
    - errors [list of StarkCore.Error]: list of errors linked to this IssuingPurchase event.
    - type [string]: type of the IssuingPurchase event which triggered the log creation. ex: "approved", "canceled", "confirmed", "denied", "reversed", "voided"
    - created [datetime.datetime]: creation datetime for the log. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, id, purchase, installment, issuing_transaction_id, errors, type, created):
        Resource.__init__(self, id=id)

        self.purchase = from_api_json(_issuing_purchase_resource, purchase)
        self.issuing_transaction_id = issuing_transaction_id
        self.installment = installment
        self.errors = _parse_errors(errors)
        self.type = type
        self.created = check_datetime(created)


_resource = {"class": Log, "name": "IssuingPurchaseLog"}


def get(id, user=None):
    """# Retrieve a specific issuingpurchase.Log
    Receive a single issuingpurchase.Log object previously created by the Stark Infra API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - issuingpurchase.Log object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def query(ids=None, limit=None, after=None, before=None, types=None, purchase_ids=None, user=None):
    """# Retrieve issuingpurchase.Log
    Receive a generator of issuingpurchase.Log objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - types [list of strings, default None]: filter for log event types. ex: ["approved", "canceled", "confirmed", "denied", "reversed", "voided"]
    - purchase_ids [list of strings, default None]: list of Purchase ids to filter logs. ex: ["5656565656565656", "4545454545454545"]
    - ids [list of strings, default None]: list of IssuingPurchase ids to filter logs. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - generator of issuingpurchase.Log objects with updated attributes
    """
    return rest.get_stream(
        resource=_resource,
        ids=ids,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        types=types,
        purchase_ids=purchase_ids,
        user=user,
    )


def page(cursor=None, ids=None, limit=None, after=None, before=None, types=None, purchase_ids=None, user=None):
    """# Retrieve paged issuingpurchase.Log
    Receive a list of up to 100 issuingpurchase.Log objects previously created in the Stark Infra API and the cursor to the next page.
    Use this function instead of query if you want to manually page your requests.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - limit [integer, default 100]: maximum number of objects to be retrieved. Max = 100. ex: 35
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - types [list of strings, default None]: filter for log event types. ex: ["approved", "canceled", "confirmed", "denied", "reversed", "voided"]
    - purchase_ids [list of strings, default None]: list of Purchase ids to filter logs. ex: ["5656565656565656", "4545454545454545"]
    - ids [list of strings, default None]: list of IssuingPurchase ids to filter logs. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - list of issuingpurchase.Log objects with updated attributes
    - cursor to retrieve the next page of issuingpurchase.Log objects
    """
    return rest.get_page(
        resource=_resource,
        cursor=cursor,
        ids=ids,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        types=types,
        purchase_ids=purchase_ids,
        user=user,
    )


def _parse_errors(errors):
    parsed_errors = []
    for error in errors:
        if isinstance(error, Error):
            parsed_errors.append(error)
            continue
        parsed_errors.append(Error(code=error['code'], message=error['message']))
    return parsed_errors
