from json import dumps
from starkcore.utils.api import api_json
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime, check_date
from ..utils import rest
from ..utils.parse import parse_and_verify


class PixReversal(Resource):
    """# PixReversal object
    PixReversals are instant payments used to revert PixRequests. You can only
    revert inbound PixRequests.
    When you initialize a PixReversal, the entity will not be automatically
    created in the Stark Infra API. The 'create' function sends the objects
    to the Stark Infra API and returns the list of created objects.
    ## Parameters (required):
    - amount [integer]: amount in cents to be reversed from the PixRequest. ex: 1234 (= R$ 12.34)
    - external_id [string]: string that must be unique among all your PixReversals. Duplicated external IDs will cause failures. By default, this parameter will block any PixReversal that repeats amount and receiver information on the same date. ex: "my-internal-id-123456"
    - end_to_end_id [string]: central bank's unique transaction ID. ex: "E79457883202101262140HHX553UPqeq"
    - reason [string]: reason why the PixRequest is being reversed. Options are "bankError", "fraud", "chashierError", "customerRequest"
    ## Parameters (optional):
    - tags [list of strings, default []]: list of strings for reference when searching for PixReversals. ex: ["employees", "monthly"]
    ## Attributes (return-only):
    - id [string]: unique id returned when the PixReversal is created. ex: "5656565656565656"
    - return_id [string]: central bank's unique reversal transaction ID. ex: "D20018183202202030109X3OoBHG74wo"
    - fee [string]: fee charged by this PixReversal. ex: 200 (= R$ 2.00)
    - status [string]: current PixReversal status. ex: "created", "processing", "success", "failed"
    - flow [string]: direction of money flow. ex: "in" or "out"
    - created [datetime.datetime]: creation datetime for the PixReversal. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - updated [datetime.datetime]: latest update datetime for the PixReversal. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, amount, external_id, end_to_end_id, reason, tags=None, id=None, return_id=None,
                 fee=None, status=None, flow=None, created=None, updated=None):
        Resource.__init__(self, id=id)
        
        self.amount = amount
        self.external_id = external_id
        self.end_to_end_id = end_to_end_id
        self.reason = reason
        self.tags = tags
        self.return_id = return_id
        self.fee = fee
        self.status = status
        self.flow = flow
        self.created = check_datetime(created)
        self.updated = check_datetime(updated)


_resource = {"class": PixReversal, "name": "PixReversal"}


def create(reversals, user=None):
    """# Create PixReversals
    Send a list of PixReversal objects for creation at the Stark Infra API
    ## Parameters (required):
    - reversals [list of PixReversal objects]: list of PixReversal objects to be created in the API
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of PixReversal objects with updated attributes
    """
    return rest.post_multi(resource=_resource, entities=reversals, user=user)


def get(id, user=None):
    """# Retrieve a specific PixReversal
    Receive a single PixReversal object previously created in the Stark Infra API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - PixReversal object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def query(limit=None, after=None, before=None, status=None, ids=None, return_ids=None,
          external_ids=None, tags=None, user=None):
    """# Retrieve PixReversals
    Receive a generator of PixReversal objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None]: date filter for objects created after a specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None]: date filter for objects created before a specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. ex: ["created", "processing", "success", "failed"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - return_ids [list of strings, default None]: central bank's unique reversal transaction IDs. ex: ["D20018183202202030109X3OoBHG74wo", "D20018183202202030109X3OoBHG72rd"].
    - external_ids [list of strings, default None]: url safe strings that must be unique among all your PixReversals. Duplicated external IDs will cause failures. By default, this parameter will block any PixReversal that repeats amount and receiver information on the same date. ex: ["my-internal-id-123456", "my-internal-id-654321"]
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - generator of PixReversal objects with updated attributes
    """

    return rest.get_stream(
        resource=_resource,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        status=status,
        ids=ids,
        return_ids=return_ids,
        external_ids=external_ids,
        tags=tags,
        user=user,
    )


def page(cursor=None, limit=None, after=None, before=None, status=None, ids=None,
         return_ids=None, external_ids=None, tags=None, user=None):
    """# Retrieve paged PixReversals
    Receive a list of up to 100 PixReversal objects previously created in the Stark Infra API and the cursor to the next page.
    Use this function instead of query if you want to manually page your reversals.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - limit [integer, default 100]: maximum number of objects to be retrieved. Max = 100. ex: 35
    - after [datetime.date or string, default None]: date filter for objects created after a specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None]: date filter for objects created before a specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. ex: ["created", "processing", "success", "failed"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - return_ids [list of strings, default None]: central bank's unique reversal transaction ID. ex: ["D20018183202202030109X3OoBHG74wo", "D20018183202202030109X3OoBHG72rd"].
    - external_ids [list of strings, default None]: url safe string that must be unique among all your PixReversals. Duplicated external IDs will cause failures. By default, this parameter will block any PixReversal that repeats amount and receiver information on the same date. ex: ["my-internal-id-123456", "my-internal-id-654321"]
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - list of PixReversal objects with updated attributes
    - cursor to retrieve the next page of PixReversal objects
    """
    return rest.get_page(
        resource=_resource,
        cursor=cursor,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        status=status,
        ids=ids,
        return_ids=return_ids,
        external_ids=external_ids,
        tags=tags,
        user=user,
    )


def parse(content, signature, user=None):
    """# Create a single verified PixReversal object from a content string
    Create a single PixReversal object from a content string received from a handler listening at the reversal url.
    If the provided digital signature does not check out with the StarkInfra public key, a
    starkinfra.error.InvalidSignatureError will be raised.
    ## Parameters (required):
    - content [string]: response content from request received at user endpoint (not parsed)
    - signature [string]: base-64 digital signature received at response header "Digital-Signature"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - Parsed PixReversal object
    """
    request = parse_and_verify(
        content=content,
        signature=signature,
        user=user,
        resource=_resource
    )

    request.fee = request.fee or 0
    request.tags = request.tags or []
    request.external_id = request.external_id or ""
    request.description = request.description or ""
    
    return request


def response(status, reason=None):
    """# Helps you respond to a PixReversal authorization
    ## Parameters (required):
    - status [string]: response to the authorization. ex: "approved" or "denied"
    ## Parameters (conditionally required):
    - reason [string, default None]: denial reason. Options: "invalidAccountNumber", "blockedAccount", "accountClosed", "invalidAccountType", "invalidTransactionType", "taxIdMismatch", "invalidTaxId", "orderRejected", "reversalTimeExpired", "settlementFailed"
    ## Return:
    - Dumped JSON string that must be returned to us
    """
    params = {
        "authorization": {
            "status": status,
            "reason": reason,
        }
    }
    return dumps(api_json(params))
