from ..utils import rest
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime, check_date


class PixFraud(Resource):
    """# PixFraud object
    PixFrauds are used to report a PixKey or taxId when a fraud
    has been confirmed.
    When you initialize a PixFraud, the entity will not be automatically
    created in the Stark Infra API. The 'create' function sends the objects
    to the Stark Infra API and returns the created object.
    ## Parameters (required):
    - external_id [string]: end_to_end_id or return_id of the transaction being reported. ex: "my_external_id"
    - type [string]: type of PixFraud. Options: "identity", "mule", "scam", "other"
    - tax_id [string]: user tax ID (CPF or CNPJ) with or without formatting. ex: "01234567890" or "20.018.183/0001-80"
    ## Parameters (optional):
    - key_id [string]: marked PixKey id. ex: "+5511989898989"
    - tags [list of strings, default []]: list of strings for tagging. ex: ["fraudulent"]
    ## Attributes (return-only):
    - id [string]: unique id returned when the PixFraud is created. ex: "5656565656565656"
    - bacen_id [string]: unique transaction id returned from Central Bank. ex: "ccf9bd9c-e99d-999e-bab9-b999ca999f99"
    - status [string]: current PixFraud status. Options: "created", "failed", "registered", "canceled".
    - created [string]: creation datetime for the PixFraud. ex: "2020-03-10 10:30:00.000000+00:00"
    - updated [string]: latest update datetime for the PixFraud. ex: "2020-03-10 10:30:00.000000+00:00"
    """

    def __init__(self,  external_id, type, tax_id, key_id=None, tags=None, id=None,
                 bacen_id=None, status=None, created=None, updated=None):
        Resource.__init__(self, id=id)

        self.external_id = external_id
        self.type = type
        self.tax_id = tax_id
        self.key_id = key_id
        self.tags = tags
        self.bacen_id = bacen_id
        self.status = status
        self.created = check_datetime(created)
        self.updated = check_datetime(updated)


_resource = {"class": PixFraud, "name": "PixFraud"}


def create(frauds, user=None):
    """# Create PixFrauds objects
    Create PixFrauds in the Stark Infra API
    ## Parameters (required):
    - frauds [list of PixFrauds]: list of PixFraud objects to be created in the API.
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of PixFraud objects with updated attributes
    """
    return rest.post_multi(resource=_resource, entities=frauds, user=user)


def get(id, user=None):
    """# Retrieve a PixFraud object
    Retrieve the PixFraud object linked to your Workspace in the Stark Infra API using its id.
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - PixFraud object that corresponds to the given id.
    """
    return rest.get_id(id=id, resource=_resource, user=user)


def query(limit=None, after=None, before=None, status=None, ids=None, bacen_id=None, type=None, flow=None, tags=None, user=None):
    """# Retrieve PixFrauds
    Receive a generator of PixFraud objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None]: date filter for objects created after a specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None]: date filter for objects created before a specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. Options: ["created", "failed", "registered", "canceled"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - bacen_id [string, default None]: unique transaction id returned from Central Bank. ex: "ccf9bd9c-e99d-999e-bab9-b999ca999f99"
    - type [list of strings, default None]: filter for the type of retrieved PixFrauds. Options: "reversal", "reversalChargeback"
    - tags [list of strings, default None]: list of strings for tagging. ex: ["fraudulent"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - generator of PixFraud objects with updated attributes
    """
    return rest.get_stream(
        resource=_resource,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        status=status,
        ids=ids,
        bacen_id=bacen_id,
        type=type,
        flow=flow,
        tags=tags,
        user=user,
    )


def page(cursor=None, limit=None, after=None, before=None, status=None, ids=None, bacen_id=None, type=None, flow=None, tags=None,
         user=None):
    """# Retrieve paged PixFraud
    Receive a list of up to 100 PixFraud objects previously created in the Stark Infra API and the cursor to the next page.
    Use this function instead of query if you want to manually page your requests.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call.
    - limit [integer, default 100]: maximum number of objects to be retrieved. Max = 100. ex: 35
    - after [datetime.date or string, default None]: date filter for objects created after a specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None]: date filter for objects created before a specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. Options: ["created", "failed", "registered", "canceled"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - bacen_id [string, default None]: unique transaction id returned from Central Bank. ex: "ccf9bd9c-e99d-999e-bab9-b999ca999f99"
    - type [list of strings, default None]: filter for the type of retrieved PixFrauds. Options: "reversal", "reversalChargeback"
    - tags [list of strings, default None]: list of strings for tagging. ex: ["fraudulent"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of PixFraud objects with updated attributes and cursor to retrieve the next page of PixFraud objects
    """
    return rest.get_page(
        resource=_resource,
        cursor=cursor,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        status=status,
        ids=ids,
        bacen_id=bacen_id,
        type=type,
        flow=flow,
        tags=tags,
        user=user,
    )


def cancel(id, user=None):
    """# Cancel a PixFraud entity
    Cancel a PixFraud entity previously created in the Stark Infra API
    ## Parameters (required):
    - id [string]: PixFraud unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - canceled PixFraud object
    """
    return rest.delete_id(resource=_resource, id=id, user=user)

