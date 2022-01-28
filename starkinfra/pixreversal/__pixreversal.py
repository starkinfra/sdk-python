from ..utils import rest
from ..utils.checks import check_datetime, check_date
from ..utils.resource import Resource


class PixReversal(Resource):
    """# PixReversal object
   When you initialize a PixReversal, the entity will not be automatically
   created in the Stark Infra API. The 'create' function sends the objects
   to the Stark Infra API and returns the list of created objects.
   ## Parameters (required):
   - amount [integer]: amount in cents to be transferred. ex: 1234 (= R$ 12.34)
   - external_id [string, default None]: url safe string that must be unique among all your transfers. Duplicated external_ids will cause failures. By default, this parameter will block any transfer that repeats amount and receiver information on the same date. ex: "my-internal-id-123456"
   - end_to_end_id [string]: central bank's unique transaction ID. ex: "E79457883202101262140HHX553UPqeq"
   - reason [string]: reason why the pix request is being reversed. Options are "bankError", "fraud", "pixWithdrawError", "refund3ByEndCustomer"
   ## Parameters (optional):
   - return_id [string]:
   - bank_code [string]: code of the bank institution in Brazil. If an ISPB (8 digits) is informed. ex: "20018183" or "341"
   - tags [string]: [list of strings]: list of strings for reference when searching for transfers. ex: ["employees", "monthly"]
   ## Attributes (return-only):
   - id [string, default None]: unique id returned when the pix reversal is created. ex: "5656565656565656"
   - fee [string]: fee charged by this Invoice. ex: 200 (= R$ 2.00)
   - status [string]: current PixReversal status. ex: "registered" or "paid"
   - transaction_id [string]: ledger transaction ids linked to this pix reversal. ex: ["19827356981273"]
   - created [datetime.datetime, default None]: creation datetime for the transfer. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
   - updated [datetime.datetime, default None]: latest update datetime for the transfer. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
   """

    def __init__(self, amount, end_to_end_id, external_id, reason, return_id=None, bank_code=None,
                 tags=None, id=None, fee=None, status=None, transaction_id=None, created=None, updated=None):
        Resource.__init__(self, id=id)
        
        self.amount = amount
        self.reason = reason
        self.end_to_end_id = end_to_end_id
        self.external_id = external_id
        self.return_id = return_id
        self.bank_code = bank_code
        self.tags = tags
        self.fee = fee
        self.status = status
        self.transaction_id = transaction_id
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


def query(limit=None, after=None, before=None, transaction_ids=None, status=None, tags=None, ids=None, user=None):
    """# Retrieve PixReversals
    Receive a generator of PixReversal objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    ## Return:
    - generator of PixReversal objects with updated attributes
    """
    return rest.get_stream(
        resource=_resource,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        transaction_ids=transaction_ids,
        status=status,
        tags=tags,
        ids=ids,
        user=user,
    )


def page(cursor=None, limit=None, after=None, before=None, transaction_ids=None, status=None, tags=None, ids=None, user=None):
    """# Retrieve paged PixReversals
    Receive a list of up to 100 PixReversal objects previously created in the Stark Infra API and the cursor to the next page.
    Use this function instead of query if you want to manually page your reversals.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
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
        transaction_ids=transaction_ids,
        status=status,
        tags=tags,
        ids=ids,
        user=user,
    )
