from ..utils import rest
from starkcore.utils.api import from_api_json
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime, check_date
from .transaction.__transaction import Transaction
from .transaction.__transaction import _sub_resource as _transaction_resource


class PixDispute(Resource):
    """# PixDispute object
    Pix disputes can be created when a fraud is detected creating a chain of transactions
    in order to reverse the funds to the origin. When you initialize a PixDispute,
    the entity will not be automatically created in the Stark Infra API. The 'create'
    function sends the objects to the Stark Infra API and returns the created object.
    ## Parameters (required):
    - reference_id [string]: endToEndId of the transaction being reported. ex: "E20018183202201201450u34sDGd19lz"
    - method [string]: method used to perform the fraudulent action. Options: "scam", "unauthorized", "coercion", "invasion", "other"
    - operator_email [string]: contact email of the operator responsible for the dispute.
    - operator_phone [string]: contact phone number of the operator responsible for the dispute.
    ## Parameters (conditionally-required):
    - description [string, default null]: description including any details that can help with the dispute investigation. The description parameter is required when method is "other".
    ## Parameters (optional):
    - tags [list of strings]: list of strings for tagging. ex: ["travel", "food"]
    - min_transaction_amount [integer]: minimum transaction amount to be considered for the graph creation.
    - max_transaction_count [integer]: maximum number of transactions to be considered for the graph creation.
    - max_hop_interval [integer]: mean time between transactions to be considered for the graph creation.
    - max_hop_count [integer]: depth to be considered for the graph creation.
    ## Attributes (return-only):
    - id [string]: unique id returned when the PixDispute is created. ex: "5656565656565656"
    - bacen_id [string]: Central Bank's unique dispute id. ex: "817fc523-9e9d-40ab-9e53-dacb71454a05"
    - flow [string]: indicates the flow of the Pix Dispute. Options: "in" if you received the PixDispute, "out" if you created the PixDispute.
    - status [string]: current PixDispute status. Options: "created", "delivered", "analysed", "processing", "closed", "failed", "canceled".
    - transactions [list of PixDispute.Transaction objects]: list of transactions related to the dispute.
    - created [datetime.datetime]: creation datetime for the PixDispute. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - updated [datetime.datetime]: latest update datetime for the PixDispute. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, reference_id, method, operator_email, operator_phone, description=None,
                 tags=None, min_transaction_amount=None, max_transaction_count=None, max_hop_interval=None,
                 max_hop_count=None, bacen_id=None, flow=None, status=None, transactions=None,
                 created=None, updated=None, id=None):
        Resource.__init__(self, id=id)

        self.reference_id = reference_id
        self.method = method
        self.operator_email = operator_email 
        self.operator_phone = operator_phone
        self.description = description
        self.tags = tags
        self.min_transaction_amount = min_transaction_amount
        self.max_transaction_count = max_transaction_count
        self.max_hop_interval = max_hop_interval
        self.max_hop_count = max_hop_count
        self.bacen_id = bacen_id
        self.flow = flow
        self.status = status
        self.transactions = _parse_transactions(transactions)
        self.created = check_datetime(created)
        self.updated = check_datetime(updated)


_resource = {"class": PixDispute, "name": "PixDispute"}


def create(requests, user=None):
    """# Create PixDisputes
    Send a list of PixDispute objects for creation at the Stark Infra API
    ## Parameters (required):
    - requests [list of PixDispute objects]: list of PixDispute objects to be created in the API
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of PixDispute objects with updated attributes
    """
    return rest.post_multi(resource=_resource, entities=requests, user=user)


def get(id, user=None):
    """# Retrieve a specific PixDispute
    Receive a single PixDispute object previously created in the Stark Infra API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - PixDispute object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def query(limit=None, after=None, before=None, status=None, ids=None, tags=None, user=None):
    """# Retrieve PixDisputes
    Receive a generator of PixDispute objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None]: date filter for objects created after a specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None]: date filter for objects created before a specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. ex: ["created", "processing", "success", "failed"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - generator of PixDispute objects with updated attributes
    """
    return rest.get_stream(
        resource=_resource,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        status=status,
        ids=ids,
        tags=tags,
        user=user,
    )


def page(cursor=None, limit=None, after=None, before=None, status=None, ids=None, tags=None, user=None):
    """# Retrieve paged PixDisputes
    Receive a list of up to 100 PixDispute objects previously created in the Stark Infra API and the cursor to the next page.
    Use this function instead of query if you want to manually page your requests.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - limit [integer, default 100]: maximum number of objects to be retrieved. Max = 100. ex: 35
    - after [datetime.date or string, default None]: date filter for objects created after a specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None]: date filter for objects created before a specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. ex: ["created", "processing", "success", "failed"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of PixDispute objects with updated attributes
    - cursor to retrieve the next page of PixDispute objects
    """
    return rest.get_page(
        resource=_resource,
        cursor=cursor,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        status=status,
        ids=ids,
        tags=tags,
        user=user,
    )


def cancel(id, user=None):
    """# Cancel a PixDispute entity
    Cancel a PixDispute entity previously created in the Stark Infra API
    ## Parameters (required):
    - id [string]: PixDispute unique id. ex: "6306109539221504"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - canceled PixDispute object
    """
    return rest.delete_id(resource=_resource, id=id, user=user)


def _parse_transactions(transactions):
    if transactions is None:
        return None
    parsed_transactions = []
    for transaction in transactions:
        if isinstance(transaction, Transaction):
            parsed_transactions.append(transaction)
            continue
        parsed_transactions.append(from_api_json(_transaction_resource, transaction))
    return parsed_transactions
