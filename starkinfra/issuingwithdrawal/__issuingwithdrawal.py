from ..utils import rest
from ..utils.resource import Resource
from ..utils.checks import check_datetime


class IssuingWithdrawal(Resource):
    """# Issuing Withdrawal object
    Displays the Issuing Withdrawal objects created to your Workspace.
    ## Parameters (required):
    - amount [integer]: Issuing Invoice value in cents. Minimum = 0 (any value will be accepted). ex: 1234 (= R$ 12.34)
    - external_id [string] Issuing Withdrawal external ID. ex: "12345"
    - description [string]: Issuing Withdrawal description. ex: "sending money back"
    ## Parameters (optional):
    - tags [list of strings]: list of strings for tagging. ex: ["tony", "stark"]
    ## Attributes (return-only):
    - id [string, default None]: unique id returned when Issuing Withdrawal is created. ex: "5656565656565656"
    - transaction_id [string, default None]: Stark Bank ledger transaction ids linked to this Issuing Withdrawal
    - issuing_transaction_id [string, default None]: issuing ledger transaction ids linked to this Issuing Withdrawal
    - updated [datetime.datetime, default None]: latest update datetime for the bin. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - created [datetime.datetime, default None]: creation datetime for the bin. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, amount, external_id, description, id=None, transaction_id=None, issuing_transaction_id=None,
                 tags=None, updated=None, created=None):
        super().__init__(id)
        self.amount = amount
        self.description = description
        self.transaction_id = transaction_id
        self.issuing_transaction_id = issuing_transaction_id
        self.external_id = external_id
        self.tags = tags
        self.updated = check_datetime(updated)
        self.created = check_datetime(created)


_resource = {"class": IssuingWithdrawal, "name": "IssuingWithdrawal"}


def create(withdrawals, user=None):
    """# Create Issuing Withdrawal
    Send a list of Issuing Withdrawal objects for creation in the Stark Bank API
    ## Parameters (required):
    - withdrawals [list of Issuing Withdrawal objects]: list of Issuing Withdrawal objects to be created in the API
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - list of Issuing Withdrawal objects with updated attributes
    """
    return rest.post_single(resource=_resource, entity=withdrawals, user=user)


def get(id, user=None):
    """# Retrieve a specific Issuing Withdrawal
    Receive a single Issuing Withdrawal object previously created in the Stark Bank API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - Issuing Withdrawal object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def query(external_ids=None, after=None, before=None, limit=None, tags=None, user=None):
    """# Retrieve Issuing Withdrawal
    Receive a generator of Issuing Withdrawal objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - external_ids [list of strings, default []]: external IDs. ex: ["5656565656565656", "4545454545454545"]
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - generator of Issuing Invoices objects with updated attributes
    """
    return rest.get_stream(
        resource=_resource,
        external_ids=external_ids,
        after=check_datetime(after),
        before=check_datetime(before),
        tags=tags,
        limit=limit,
        user=user,
    )


def page(external_ids=None, after=None, before=None, limit=None, tags=None, cursor=None, user=None):
    """# Retrieve Issuing Withdrawal
    Receive a list of Issuing Withdrawal objects previously created in the Stark Infra API and the cursor to the next page.
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - external_ids [list of strings, default []]: external IDs. ex: ["5656565656565656", "4545454545454545"]
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - list of Issuing Withdrawal objects with updated attributes
    - cursor to retrieve the next page of Issuing Withdrawal objects
    """
    return rest.get_page(
        resource=_resource,
        external_ids=external_ids,
        after=check_datetime(after),
        before=check_datetime(before),
        tags=tags,
        limit=limit,
        cursor=cursor,
        user=user,
    )
