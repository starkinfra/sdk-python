from ..utils import rest
from ..ledger.rule.__rule import parse_rules
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime, check_date


class LedgerTransaction(Resource):
    """# LedgerTransaction object
    LedgerTransactions are used to track the balance of a given amount by inserting LedgerTransactions to them.
    They can represent a bank account, a digital wallet, an inventory product, etc.
    ## Parameters (required):
    - amount [integer]: amount of the transaction. ex: 11234
    - ledger_id [string]: id of the Ledger containing the transaction. ex: "5656565656565656"
    - external_id [string]: string that must be unique among all your LedgerTransactions in a single Ledger. ex: "my-internal-id-123456"
    - source [string]: source of the LedgerTransaction. ex: "bank-transfer/123"
    ## Parameters (optional):
    - fee [integer]: fee applied to the LedgerTransaction. ex: 100
    - rules [list of Rule objects, default []]: list of Rule objects linked to the LedgerTransaction. Rules are used to overwrite the Ledger's rules for this transaction. ex: [Rule(key="minimumBalance", value=0)]
    - metadata [dictionary, default {}]: dictionary object used to store additional information about the LedgerTransaction object. ex: { "orderId": "123", "orderType": "purchase" }.
    - tags [list of strings, default []]: list of strings for reference when searching for LedgerTransactions. ex: ["transfer/123", "savings"]
    ## Attributes (return-only):
    - id [string]: unique id returned when the LedgerTransaction is created. ex: "5656565656565656"
    - balance [integer]: Ledger's balance after the transaction. ex: 11234
    - created [datetime.datetime]: creation datetime for the LedgerTransaction. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, amount, ledger_id, external_id, source, id=None, balance=None, fee=None, rules=None, metadata=None, tags=None, created=None):
        Resource.__init__(self, id=id)

        self.amount = amount
        self.ledger_id = ledger_id
        self.external_id = external_id
        self.source = source
        self.balance = balance
        self.fee = fee
        self.rules = parse_rules(rules)
        self.metadata = metadata
        self.tags = tags
        self.created = check_datetime(created)


_resource = {"class": LedgerTransaction, "name": "LedgerTransaction"}


def create(transactions, user=None):
    """# Create LedgerTransactions
    Send a list of LedgerTransaction objects for creation at the Stark Infra API
    ## Parameters (required):
    - transactions [list of LedgerTransaction objects]: list of LedgerTransaction objects to be created in the Stark Infra API
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of LedgerTransaction objects with updated attributes
    """
    return rest.post_multi(resource=_resource, entities=transactions, user=user)


def get(id, user=None):
    """# Retrieve a specific LedgerTransaction
    Receive a single LedgerTransaction object previously created in the Stark Infra API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - LedgerTransaction object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def query(ledger_id=None, flow=None, tags=None, external_ids=None, after=None, before=None,
          ids=None, limit=None, user=None):
    """# Retrieve LedgerTransactions
    Receive a generator of LedgerTransaction objects previously created in the Stark Infra API
    ## Parameters (conditionally-required):
    - ledger_id [string, default None]: id of the Ledger containing the transaction. Either ledger_id or ids must be provided. If both are sent, the query will be filtered by both. ex: "5656565656565656"
    - ids [list of strings, default None]: list of LedgerTransaction ids to filter retrieved objects. Either ledger_id or ids must be provided. If both are sent, the query will be filtered by both. ex: ["5656565656565656", "4545454545454545"]
    ## Parameters (optional):
    - flow [string, default None]: direction of the transaction. ex: "in" or "out"
    - tags [list of strings, default None]: list of tags to filter retrieved objects. ex: ["transfer/123", "savings"]
    - external_ids [list of strings, default None]: list of LedgerTransaction external ids to filter retrieved objects. ex: ["my-internal-id-123456", "my-internal-id-654321"]
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - limit [integer, default 100, maximum 1000]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - generator of LedgerTransaction objects with updated attributes
    """
    return rest.get_stream(
        resource=_resource,
        ledger_id=ledger_id,
        flow=flow,
        tags=tags,
        external_ids=external_ids,
        after=check_date(after),
        before=check_date(before),
        ids=ids,
        limit=limit,
        user=user,
    )


def page(ledger_id=None, flow=None, tags=None, external_ids=None, after=None, before=None,
         ids=None, limit=None, cursor=None, user=None):
    """# Retrieve paged LedgerTransactions
    Receive a list of LedgerTransaction objects previously created in the Stark Infra API and the cursor to the next page.
    Use this function instead of query if you want to manually page your requests.
    ## Parameters (conditionally-required):
    - ledger_id [string, default None]: id of the Ledger containing the transaction. Either ledger_id or ids must be provided. If both are sent, the query will be filtered by both. ex: "5656565656565656"
    - ids [list of strings, default None]: list of LedgerTransaction ids to filter retrieved objects. Either ledger_id or ids must be provided. If both are sent, the query will be filtered by both. ex: ["5656565656565656", "4545454545454545"]
    ## Parameters (optional):
    - flow [string, default None]: direction of the transaction. ex: "in" or "out"
    - tags [list of strings, default None]: list of tags to filter retrieved objects. ex: ["transfer/123", "savings"]
    - external_ids [list of strings, default None]: list of LedgerTransaction external ids to filter retrieved objects. ex: ["my-internal-id-123456", "my-internal-id-654321"]
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - limit [integer, default 100, maximum 1000]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - cursor [string, default None]: cursor returned on the previous page function call
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of LedgerTransaction objects with updated attributes
    - cursor to retrieve the next page of LedgerTransaction objects
    """
    return rest.get_page(
        resource=_resource,
        ledger_id=ledger_id,
        flow=flow,
        tags=tags,
        external_ids=external_ids,
        after=check_date(after),
        before=check_date(before),
        ids=ids,
        limit=limit,
        cursor=cursor,
        user=user,
    )
