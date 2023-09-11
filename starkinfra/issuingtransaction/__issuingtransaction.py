from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime, check_date
from ..utils import rest


class IssuingTransaction(Resource):
    """# IssuingTransaction object
    The IssuingTransaction object created in your Workspace to represent each balance shift.
    ## Attributes (return-only):
    - id [string]: unique id returned when IssuingTransaction is created. ex: "5656565656565656"
    - amount [integer]: IssuingTransaction value in cents. ex: 1234 (= R$ 12.34)
    - balance [integer]: balance amount of the Workspace at the instant of the Transaction in cents. ex: 200 (= R$ 2.00)
    - description [string]: IssuingTransaction description. ex: "Buying food"
    - source [string]: source of the transaction. ex: "issuing-purchase/5656565656565656"
    - tags [string]: list of strings inherited from the source resource. ex: ["tony", "stark"]
    - created [datetime.datetime]: creation datetime for the IssuingTransaction. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, id, amount, balance, description, source, tags, created):
        Resource.__init__(self, id=id)

        self.amount = amount
        self.balance = balance
        self.description = description
        self.source = source
        self.tags = tags
        self.created = created


_resource = {"class": IssuingTransaction, "name": "IssuingTransaction"}


def get(id, user=None):
    """# Retrieve a specific IssuingTransaction
    Receive a single IssuingTransaction object previously created in the Stark Infra API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - IssuingTransaction object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def query(source=None, tags=None, external_ids=None, after=None, before=None,
          ids=None, limit=None, user=None):
    """# Retrieve IssuingTransactions
    Receive a generator of IssuingTransaction objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default 100]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - external_ids [list of strings, default None]: external IDs. ex: ["5656565656565656", "4545454545454545"]
    - status [string, default None]: filter for status of retrieved objects. ex: "approved", "canceled", "denied", "confirmed" or "voided"
    - ids [list of strings, default None, default None]: purchase IDs
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - generator of IssuingTransaction objects with updated attributes
    """
    return rest.get_stream(
        resource=_resource,
        source=source,
        tags=tags,
        external_ids=external_ids,
        after=check_date(after),
        before=check_date(before),
        ids=ids,
        limit=limit,
        user=user,
    )


def page(source=None, tags=None, external_ids=None, after=None, before=None,
         ids=None, limit=None, cursor=None, user=None):
    """# Retrieve paged IssuingTransaction
    Receive a list of IssuingTransaction objects previously created in the Stark Infra API and the cursor to the next page.
    ## Parameters (optional):
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - external_ids [list of strings, default None]: external IDs. ex: ["5656565656565656", "4545454545454545"]
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - status [string, default None]: filter for status of retrieved objects. ex: "approved", "canceled", "denied", "confirmed" or "voided"
    - ids [list of strings,default None]: purchase IDs
    - limit [integer, default 100]: maximum number of objects to be retrieved. Max = 100. ex: 35
    - cursor [string, default None]: cursor returned on the previous page function call
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of IssuingTransaction objects with updated attributes
    - cursor to retrieve the next page of IssuingPurchase objects
    """
    return rest.get_page(
        resource=_resource,
        source=source,
        tags=tags,
        external_ids=external_ids,
        after=check_date(after),
        before=check_date(before),
        ids=ids,
        limit=limit,
        cursor=cursor,
        user=user,
    )
