from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime, check_date
from ..utils import rest


class IssuingWithdrawal(Resource):
    """# IssuingWithdrawal object
    The IssuingWithdrawal objects created in your Workspace return cash from your Issuing balance to your
    Banking balance.
    ## Parameters (required):
    - amount [integer]: IssuingWithdrawal value in cents. Minimum = 0 (any value will be accepted). ex: 1234 (= R$ 12.34)
    - external_id [string] IssuingWithdrawal external ID. ex: "12345"
    - description [string]: IssuingWithdrawal description. ex: "sending money back"
    ## Parameters (optional):
    - tags [list of strings, default []]: list of strings for tagging. ex: ["tony", "stark"]
    ## Attributes (return-only):
    - id [string]: unique id returned when IssuingWithdrawal is created. ex: "5656565656565656"
    - transaction_id [string]: Stark Bank ledger transaction ids linked to this IssuingWithdrawal
    - issuing_transaction_id [string]: issuing ledger transaction ids linked to this IssuingWithdrawal
    - updated [datetime.datetime]: latest update datetime for the IssuingWithdrawal. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - created [datetime.datetime]: creation datetime for the IssuingWithdrawal. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, amount, external_id, description, tags=None, id=None, transaction_id=None,
                 issuing_transaction_id=None, updated=None, created=None):
        Resource.__init__(self, id=id)

        self.amount = amount
        self.external_id = external_id
        self.description = description
        self.tags = tags
        self.transaction_id = transaction_id
        self.issuing_transaction_id = issuing_transaction_id
        self.updated = check_datetime(updated)
        self.created = check_datetime(created)


_resource = {"class": IssuingWithdrawal, "name": "IssuingWithdrawal"}


def create(withdrawal, user=None):
    """# Create an IssuingWithdrawal
    Send a single IssuingWithdrawal object for creation at the Stark Infra API
    ## Parameters (required):
    - withdrawal [IssuingWithdrawal object]: IssuingWithdrawal object to be created in the API.
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - IssuingWithdrawal object with updated attributes
    """
    return rest.post_single(resource=_resource, entity=withdrawal, user=user)


def get(id, user=None):
    """# Retrieve a specific IssuingWithdrawal
    Receive a single IssuingWithdrawal object previously created in the Stark Infra API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - IssuingWithdrawal object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def query(external_ids=None, after=None, before=None, limit=None, tags=None, user=None):
    """# Retrieve IssuingWithdrawals
    Receive a generator of IssuingWithdrawal objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - external_ids [list of strings, default []]: external IDs. ex: ["5656565656565656", "4545454545454545"]
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - generator of IssuingWithdrawal objects with updated attributes
    """
    return rest.get_stream(
        resource=_resource,
        external_ids=external_ids,
        after=check_date(after),
        before=check_date(before),
        tags=tags,
        limit=limit,
        user=user,
    )


def page(external_ids=None, after=None, before=None, limit=None, tags=None, cursor=None, user=None):
    """# Retrieve paged IssuingWithdrawals
    Receive a list of IssuingWithdrawal objects previously created in the Stark Infra API and the cursor to the next page.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - limit [integer, default 100]: maximum number of objects to be retrieved. Max = 100. ex: 35
    - external_ids [list of strings, default []]: external IDs. ex: ["5656565656565656", "4545454545454545"]
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of IssuingWithdrawal objects with updated attributes
    - cursor to retrieve the next page of IssuingWithdrawal objects
    """
    return rest.get_page(
        resource=_resource,
        external_ids=external_ids,
        after=check_date(after),
        before=check_date(before),
        tags=tags,
        limit=limit,
        cursor=cursor,
        user=user,
    )
