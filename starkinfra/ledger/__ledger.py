from ..utils import rest
from .rule.__rule import parse_rules
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime, check_date


class Ledger(Resource):
    """# Ledger object
    Ledgers are used to track the balance of a given amount by inserting LedgerTransactions to them.
    They can represent a bank account, a digital wallet, an inventory product, etc.
    ## Parameters (required):
    - external_id [string]: string that must be unique among all your Ledgers. ex: "my-internal-id-123456"
    ## Parameters (optional):
    - rules [list of Rule objects, default []]: list of Rule objects linked to the Ledger. Rules are used to limit the balance of the Ledger. ex: [Rule(key="minimumBalance", value=0)]
    - tags [list of strings, default []]: list of strings for reference when searching for Ledgers. ex: ["account/123", "savings"]
    - metadata [dictionary, default {}]: dictionary object used to store additional information about the Ledger object. ex: { "accountId": "123", "accountType": "savings" }.
    ## Attributes (return-only):
    - id [string]: unique id returned when the Ledger is created. ex: "5656565656565656"
    - created [datetime.datetime]: creation datetime for the Ledger. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - updated [datetime.datetime]: latest update datetime for the Ledger. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, external_id, id=None, rules=None, tags=None, metadata=None, created=None, updated=None):
        Resource.__init__(self, id=id)

        self.external_id = external_id
        self.rules = parse_rules(rules)
        self.tags  = tags
        self.metadata = metadata
        self.created = check_datetime(created)
        self.updated = check_datetime(updated)


_resource = {"class": Ledger, "name": "Ledger"}


def create(ledgers, user=None):
    """# Create Ledgers
    Send a list of Ledger objects for creation at the Stark Infra API
    ## Parameters (required):
    - ledgers [list of Ledger objects]: list of Ledger objects to be created in the Stark Infra API
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of Ledger objects with updated attributes
    """
    return rest.post_multi(resource=_resource, entities=ledgers, user=user)


def get(id, user=None):
    """# Retrieve a specific Ledger
    Receive a single Ledger object previously created in the Stark Infra API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - Ledger object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def query(limit=None, after=None, before=None, ids=None, external_ids=None, tags=None, user=None):
    """# Retrieve Ledgers
    Receive a generator of Ledger objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - ids [list of strings, default None]: list of Ledger ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - external_ids [list of strings, default None]: list of Ledger external ids to filter retrieved objects. ex: ["my-internal-id-123456", "my-internal-id-654321"]
    - tags [list of strings, default None]: list of tags to filter retrieved objects. ex: ["account/123", "savings"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - generator of Ledger objects with updated attributes
    """
    return rest.get_stream(
        resource=_resource,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        ids=ids,
        external_ids=external_ids,
        tags=tags,
        user=user,
    )


def page(limit=None, after=None, before=None, ids=None, external_ids=None, tags=None, cursor=None, user=None):
    """# Retrieve paged Ledgers
    Receive a list of up to 100 Ledger objects previously created in the Stark Infra API and the cursor to the next page.
    Use this function instead of query if you want to manually page your requests.
    ## Parameters (optional):
    - limit [integer, default 100]: maximum number of objects to be retrieved. Max = 100. ex: 35
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - ids [list of strings, default None]: list of Ledger ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - external_ids [list of strings, default None]: list of Ledger external ids to filter retrieved objects. ex: ["my-internal-id-123456", "my-internal-id-654321"]
    - tags [list of strings, default None]: list of tags to filter retrieved objects. ex: ["account/123", "savings"]
    - cursor [string, default None]: cursor returned on the previous page function call
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of Ledger objects with updated attributes
    - cursor to retrieve the next page of Ledger objects
    """
    return rest.get_page(
        resource=_resource,
        cursor=cursor,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        ids=ids,
        external_ids=external_ids,
        tags=tags,
        user=user,
    )


def update(id, rules=None, tags=None, metadata=None, user=None):
    """# Update Ledger
    Update a Ledger by passing id.
    ## Parameters (required):
    - id [string]: Ledger id. ex: "5656565656565656"
    ## Parameters (optional):
    - rules [list of Rule objects, default None]: list of Rule objects linked to the Ledger. Rules are used to limit the balance of the Ledger. ex: [Rule(key="minimumBalance", value=0)]
    - tags [list of strings, default None]: list of strings for reference when searching for Ledgers. ex: ["account/123", "savings"]
    - metadata [dictionary, default None]: dictionary object used to store additional information about the Ledger object. ex: { "accountId": "123", "accountType": "savings" }.
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - target Ledger object with updated attributes
    """
    payload = {
        "rules": rules,
        "tags": tags,
        "metadata": metadata,
    }
    return rest.patch_id(resource=_resource, id=id, user=user, payload=payload)
