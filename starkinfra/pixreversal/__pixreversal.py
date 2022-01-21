from ..utils import rest
from ..utils.checks import check_datetime, check_date
from ..utils.resource import Resource


class PixReversal(Resource):

    def __init__(self, amount, end_to_end_id, external_id, reason, transaction_id=None, id=None, fee=None,
                 return_id=None, tags=None, bank_code=None, created=None, updated=None):
        Resource.__init__(self, id=id)
        
        self.amount = amount
        self.transaction_id = transaction_id
        self.reason = reason
        self.end_to_end_id = end_to_end_id
        self.external_id = external_id
        self.fee = fee
        self.return_id = return_id
        self.tags = tags
        self.bank_code = bank_code
        self.created = check_datetime(created)
        self.updated = check_datetime(updated)


_resource = {"class": PixReversal, "name": "PixReversal"}


def create(reversals, user=None):
    """# Create PixReversals
    Send a list of PixReversal objects for creation in the Stark Infra API
    ## Parameters (required):
    - transfers [list of PixReversal objects]: list of PixReversal objects to be created in the API
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkbank.user was set before function call
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
    Use this function instead of query if you want to manually page your requests.
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
