from ..utils.resource import Resource
from ..utils import rest


class IssuingBin(Resource):
    """# IssuingBin object
    The IssuingBalance object displays the informations of BINs registered to your Workspace.
    ## Attributes (return-only):
    - id [string, default None]: unique BIN number registered within the card network. ex: "53810200"
    - network [string, default None]: card network flag. ex: "mastercard"
    - settlement [string, default None]: settlement type. ex: "credit"
    - category [string, default None]: purchase category. ex: "prepaid"
    - client [string, default None]: client type. ex: "business"
    - updated [datetime.datetime, default None]: latest update datetime for the Bin. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - created [datetime.datetime, default None]: creation datetime for the Bin. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, id=None, updated=None, created=None, network=None, settlement=None, category=None, client=None):
        super().__init__(id)
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
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
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
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
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
