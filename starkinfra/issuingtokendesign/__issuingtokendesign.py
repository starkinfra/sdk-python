from starkinfra.utils import rest
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime, check_date


class IssuingTokenDesign(Resource):
    """# IssuingTokenDesign object
    The IssuingTokenDesign object displays the information of the token designs created in your Workspace.
    This resource represents the existent designs for the cards which will be tokenized.
    ## Attributes (return-only):
    - id [string]: unique id returned when IssuingTokenDesign is created. ex: "5656565656565656"
    - name [string]: Design name. ex: "Stark Bank - White Metal"
    - created [datetime.datetime]: creation datetime for the IssuingTokenDesign. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - updated [datetime.datetime]: latest update datetime for the IssuingTokenDesign. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, id=None, name=None, created=None, updated=None):
        Resource.__init__(self, id=id)

        self.name = name
        self.created = created
        self.updated = updated


_resource = {"class": IssuingTokenDesign, "name": "IssuingTokenDesign"}


def get(id, user=None):
    """# Retrieve a specific IssuingTokenDesign
    Receive a single IssuingTokenDesign object previously created in the Stark Infra API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - IssuingTokenDesign object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def query(limit=None, ids=None, user=None):
    """# Retrieve IssuingTokenDesigns
    Receive a generator of IssuingTokenDesign objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Max = 100. ex:
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - generator of IssuingTokenDesigns objects with updated attributes
    """
    return rest.get_stream(
        resource=_resource,
        limit=limit,
        ids=ids,
        user=user,
    )


def page(cursor=None, limit=None, ids=None, user=None):
    """# Retrieve paged IssuingTokenDesign
    Receive a list of IssuingTokenDesign objects previously created in the Stark Infra API and the cursor to the next page.
    Use this function instead of query if you want to manually page your requests.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - limit [integer, default 100]: maximum number of objects to be retrieved. Max = 100. ex: 35
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - list of IssuingTokenDesign objects with updated attributes
    - cursor to retrieve the next page of IssuingTokenDesign objects
    """
    return rest.get_page(
        resource=_resource,
        cursor=cursor,
        limit=limit,
        ids=ids,
        user=user,
    )


def pdf(id, user=None):
    """# Retrieve a specific IssuingTokenDesign pdf file
    Receive a single IssuingTokenDesign pdf file generated in the Stark Infra API by its id.
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - IssuingTokenDesign pdf file
    """
    return rest.get_content(resource=_resource, id=id, user=user, sub_resource_name="pdf")
