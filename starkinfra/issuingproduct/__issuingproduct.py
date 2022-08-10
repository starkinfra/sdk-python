from starkcore.utils.resource import Resource
from ..utils import rest


class IssuingProduct(Resource):
    """# IssuingProduct object
    The IssuingProduct object displays information of registered card products to your Workspace.
    They represent a group of cards that begin with the same numbers (id) and offer the same product to end customers.
    ## Attributes (return-only):
    - id [string]: unique card product number (BIN) registered within the card network. ex: "53810200"
    - network [string]: card network flag. ex: "mastercard"
    - funding_type [string]: type of funding used for payment. ex: "credit", "debit"
    - holder_type [string]: holder type. ex: "business", "individual"
    - code [string]: internal code from card flag informing the product. ex: "MRW", "MCO", "MWB", "MCS"
    - created [datetime.datetime]: creation datetime for the IssuingProduct. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, id=None, network=None, funding_type=None, holder_type=None, code=None, created=None):
        Resource.__init__(self, id=id)

        self.network = network
        self.funding_type = funding_type
        self.holder_type = holder_type
        self.code = code
        self.created = created


_resource = {"class": IssuingProduct, "name": "IssuingProduct"}


def query(limit=None, user=None):
    """# Retrieve IssuingProducts
    Receive a generator of IssuingProduct objects previously registered in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - generator of IssuingProduct objects with updated attributes
    """
    return rest.get_stream(
        resource=_resource,
        limit=limit,
        user=user,
    )


def page(limit=None, cursor=None, user=None):
    """# Retrieve paged IssuingProducts
    Receive a list of up to 100 IssuingProduct objects previously registered in the Stark Infra API and the cursor to the next page.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - limit [integer, default 100]: maximum number of objects to be retrieved. Max = 100. ex: 35
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - list of IssuingProduct objects with updated attributes
    - cursor to retrieve the next page of IssuingProduct objects
    """
    return rest.get_page(
        resource=_resource,
        limit=limit,
        cursor=cursor,
        user=user,
    )
