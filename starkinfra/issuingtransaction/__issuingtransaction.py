from starkbank.utils.resource import Resource
from starkbank.utils.checks import check_datetime

from starkbank.utils import rest


class IssuingTransaction(Resource):

    def __init__(self, id, amount, sub_issuer_id, balance, created, description, source, tags):
        super().__init__(id)
        self.amount = amount
        self.sub_issuer_id = sub_issuer_id
        self.balance = balance
        self.description = description
        self.source = source
        self.tags = tags
        self.created = created


_resource = {"class": IssuingTransaction, "name": "IssuingTransaction"}


def get(id, user=None):
    """# Retrieve a specific Invoice
    Receive a single Invoice object previously created in the Stark Bank API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkbank.user was set before function call
    ## Return:
    - Invoice object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def query(source=None, tags=None, external_ids=None, after=None, before=None,
          ids=None, limit=None, fields=None, user=None):
    return rest.get_stream(
        resource=_resource,
        source=source,
        tags=tags,
        external_ids=external_ids,
        after=check_datetime(after),
        before=check_datetime(before),
        ids=ids,
        limit=limit,
        fields=fields,
        user=user,
    )


def page(source=None, tags=None, external_ids=None, after=None, before=None,
         ids=None, limit=None, fields=None, cursor=None, user=None):
    return rest.get_page(
        resource=_resource,
        source=source,
        tags=tags,
        external_ids=external_ids,
        after=check_datetime(after),
        before=check_datetime(before),
        ids=ids,
        limit=limit,
        fields=fields,
        cursor=cursor,
        user=user,
    )


