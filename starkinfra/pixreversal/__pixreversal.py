from ..utils import rest
from ..utils.checks import check_datetime, check_date
from ..utils.resource import Resource
from ..utils.parse import parse_and_verify


class PixReversal(Resource):
    """# PixReversal object
   When you initialize a PixReversal, the entity will not be automatically
   created in the Stark Infra API. The 'create' function sends the objects
   to the Stark Infra API and returns the list of created objects.
   ## Parameters (required):
   - amount [integer]: amount in cents to be reversed from PixRequest. ex: 1234 (= R$ 12.34)
   - external_id [string]: url safe string that must be unique among all your PixReversals. Duplicated external IDs will cause failures. By default, this parameter will block any PixReversal that repeats amount and receiver information on the same date. ex: "my-internal-id-123456"
   - end_to_end_id [string]: central bank's unique transaction ID. ex: "E79457883202101262140HHX553UPqeq"
   - reason [string]: reason why the PixRequest is being reversed. Options are "bankError", "fraud", "pixWithdrawError", "refundByEndCustomer"
   ## Parameters (optional):
   - tags [list of strings, default None]: list of strings for reference when searching for PixReversals. ex: ["employees", "monthly"]
   ## Attributes (return-only):
   - id [string, default None]: unique id returned when the PixReversal is created. ex: "5656565656565656".
   - return_id [string, default None]: central bank's unique reversal transaction ID. ex: "D20018183202202030109X3OoBHG74wo".
   - bank_code [string, default None]: code of the bank institution in Brazil. ex: "20018183" or "341"
   - fee [string, default None]: fee charged by this PixReversal. ex: 200 (= R$ 2.00)
   - status [string, default None]: current PixReversal status. ex: "registered" or "paid"
   - flow [string, default None]: direction of money flow. ex: "in" or "out"
   - created [datetime.datetime, default None]: creation datetime for the PixReversal. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
   - updated [datetime.datetime, default None]: latest update datetime for the PixReversal. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
   """

    def __init__(self, amount, external_id, end_to_end_id, reason, tags=None, id=None, return_id=None, bank_code=None,
                 fee=None, status=None, flow=None, created=None, updated=None):
        Resource.__init__(self, id=id)
        
        self.amount = amount
        self.external_id = external_id
        self.end_to_end_id = end_to_end_id
        self.reason = reason
        self.tags = tags
        self.return_id = return_id
        self.bank_code = bank_code
        self.fee = fee
        self.status = status
        self.flow = flow
        self.created = check_datetime(created)
        self.updated = check_datetime(updated)


_resource = {"class": PixReversal, "name": "PixReversal"}


def create(reversals, user=None):
    """# Create PixReversals
    Send a list of PixReversal objects for creation in the Stark Infra API
    ## Parameters (required):
    - reversals [list of PixReversal objects]: list of PixReversal objects to be created in the API
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
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
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - PixReversal object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def query(fields=None, limit=None, after=None, before=None, status=None, tags=None, ids=None, return_id=None,
          external_id=None, user=None):
    """# Retrieve PixReversals
    Receive a generator of PixReversal objects previously created in the Stark Infra API
    ## Parameters (optional):
    - fields [list of strings, default None]: parameters to be retrieved from PixRequest objects. ex: ["amount", "id"]
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None]: date filter for objects created or updated only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None]: date filter for objects created or updated only before specified date. ex: datetime.date(2020, 3, 10)
    - status [string, default None]: filter for status of retrieved objects. ex: "success" or "failed"
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - return_ids [list of strings, default None]: central bank's unique reversal transaction IDs. ex: ["D20018183202202030109X3OoBHG74wo", "D20018183202202030109X3OoBHG72rd"].
    - external_ids [list of strings, default None]: url safe strings that must be unique among all your PixReversals. Duplicated external IDs will cause failures. By default, this parameter will block any PixReversal that repeats amount and receiver information on the same date. ex: ["my-internal-id-123456", "my-internal-id-654321"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - generator of PixReversal objects with updated attributes
    """

    return rest.get_stream(
        resource=_resource,
        fields=fields,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        status=status,
        tags=tags,
        ids=ids,
        return_id=return_id,
        external_id=external_id,
        user=user,
    )


def page(cursor=None, fields=None, limit=None, after=None, before=None, status=None, tags=None, ids=None, return_id=None,
         external_id=None, user=None):
    """# Retrieve paged PixReversals
    Receive a list of up to 100 PixReversal objects previously created in the Stark Infra API and the cursor to the next page.
    Use this function instead of query if you want to manually page your reversals.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - fields [list of strings, default None]: parameters to be retrieved from PixRequest objects. ex: ["amount", "id"]
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None]: date filter for objects created or updated only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None]: date filter for objects created or updated only before specified date. ex: datetime.date(2020, 3, 10)
    - status [string, default None]: filter for status of retrieved objects. ex: "success" or "failed"
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - return_ids [list of strings, default None]: central bank's unique reversal transaction ID. ex: ["D20018183202202030109X3OoBHG74wo", "D20018183202202030109X3OoBHG72rd"].
    - external_ids [list of strings, default None]: url safe string that must be unique among all your PixReversals. Duplicated external IDs will cause failures. By default, this parameter will block any PixReversal that repeats amount and receiver information on the same date. ex: ["my-internal-id-123456", "my-internal-id-654321"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - list of PixReversal objects with updated attributes
    - cursor to retrieve the next page of PixReversal objects
    """
    return rest.get_page(
        resource=_resource,
        cursor=cursor,
        fields=fields,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        status=status,
        tags=tags,
        ids=ids,
        return_id=return_id,
        external_id=external_id,
        user=user,
    )


def parse(content, signature, user=None):
    """# Create single authorized PixRequest object from a content string
    Create a single PixRequest object from a content string received from a handler listening at a subscribed user endpoint.
    If the provided digital signature does not check out with the StarkInfra public key, a
    starkinfra.exception.InvalidSignatureException will be raised.
    ## Parameters (required):
    - content [string]: response content from request received at user endpoint (not parsed)
    - signature [string]: base-64 digital signature received at response header "Digital-Signature"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - Parsed PixRequest object
    """

    return parse_and_verify(content, signature, user, _resource)
