from starkcore.utils.api import from_api_json
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime
from ..utils import rest


class IssuingDesign(Resource):
    """# IssuingDesign object
    The IssuingDesign object displays information on the card and card package designs available to your Workspace.
    ## Attributes (return-only):
    - id [string]: unique id returned when IssuingDesign is created. ex: "5656565656565656"
    - name [string]: card or package design name. ex: "stark-plastic-dark-001"
    - embosser_ids [list of strings]: list of embosser unique ids. ex: ["5136459887542272", "5136459887542273"]
    - type [string]: card or package design type. Options: "card", "envelope"
    - updated [datetime.datetime]: latest update datetime for the IssuingDesign. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - created [datetime.datetime]: creation datetime for the IssuingDesign. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, id=None, name=None, embosser_ids=None, type=None, created=None, updated=None):
        Resource.__init__(self, id=id)

        self.name = name
        self.embosser_ids = embosser_ids
        self.type = type
        self.created = check_datetime(created)
        self.updated = check_datetime(updated)


_resource = {"class": IssuingDesign, "name": "IssuingDesign"}


def parse_designs(designs):
    parsed_designs = []
    if designs is None:
        return designs
    for design in designs:
        if isinstance(design, IssuingDesign):
            parsed_designs.append(design)
            continue
        parsed_designs.append(from_api_json(_resource, design))
    return parsed_designs


def query(limit=None, ids=None, user=None):
    """# Retrieve IssuingDesigns
    Receive a generator of IssuingDesign objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - generator of IssuingDesign objects with updated attributes
    """
    return rest.get_stream(
        resource=_resource,
        limit=limit,
        ids=ids,
        user=user,
    )


def page(cursor=None, limit=None, ids=None, user=None):
    """# Retrieve paged IssuingDesigns
    Receive a list of up to 100 IssuingDesign objects previously created in the Stark Infra API and the cursor to the next page.
    Use this function instead of query if you want to manually page your requests.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - limit [integer, default 100]: maximum number of objects to be retrieved. Max = 100. ex: 35
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of IssuingDesign objects with updated attributes
    - cursor to retrieve the next page of IssuingDesign objects
    """
    return rest.get_page(
        resource=_resource,
        cursor=cursor,
        limit=limit,
        ids=ids,
        user=user,
    )


def get(id, user=None):
    """# Retrieve a specific IssuingDesign
    Receive a single IssuingDesign object previously created in the Stark Infra API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - IssuingDesign object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def pdf(id, user=None):
    """# Retrieve a specific IssuingDesign pdf file
    Receive a single IssuingDesign pdf file generated in the Stark Infra API by its id.
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - IssuingDesign pdf file
    """
    return rest.get_content(resource=_resource, id=id, user=user, sub_resource_name="pdf")
