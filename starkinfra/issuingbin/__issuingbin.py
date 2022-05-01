from starkcore.utils.resource import Resource
from ..utils import rest


class IssuingBin(Resource):
    """# IssuingBin object
    The IssuingBin object displays the informations of BINs registered to your Workspace.
    They represent a group of cards that begin with the same numbers (BIN) and offer the same product to end customers.
    ## Attributes (return-only):
    - id [string]: unique BIN number registered within the card network. ex: "53810200"
    - network [string]: card network flag. ex: "mastercard"
    - settlement [string]: settlement type. ex: "credit"
    - category [string]: purchase category. ex: "prepaid"
    - client [string]: client type. ex: "business"
    - updated [datetime.datetime]: latest update datetime for the Bin. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - created [datetime.datetime]: creation datetime for the Bin. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, id=None, updated=None, created=None, network=None, settlement=None, category=None, client=None):
        Resource.__init__(self, id=id)
        self.network = network
        self.settlement = settlement
        self.category = category
        self.client = client
        self.updated = updated
        self.created = created


_resource = {"class": IssuingBin, "name": "IssuingBin"}


def query(limit=None, user=None):
    """# Retrieve IssuingBins
    Receive a generator of IssuingBin objects previously registered in the Stark Bank API
    ## Parameters (optional):
    - limit [integer, default 100]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - generator of IssuingBin objects with updated attributes
    """
    return rest.get_stream(
        resource=_resource,
        limit=limit,
        user=user,
    )


def page(limit=None, cursor=None, user=None):
    """# Retrieve paged IssuingBins
    Receive a list of up to 100 IssuingBin objects previously registered in the Stark Bank API and the cursor to the next page.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - limit [integer, default 100]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - list of IssuingBin objects with updated attributes
    - cursor to retrieve the next page of IssuingBin objects
    """
    return rest.get_page(
        resource=_resource,
        limit=limit,
        cursor=cursor,
        user=user,
    )
