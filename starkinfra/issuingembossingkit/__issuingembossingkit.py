from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime
from ..issuingdesign.__issuingdesign import parse_designs
from ..utils import rest


class IssuingEmbossingKit(Resource):
    """# IssuingEmbossingKit object
    The IssuingEmbossingKit object displays information on the embossing kits available to your Workspace.
    ## Attributes (return-only):
    - id [string]: unique id returned when IssuingEmbossingKit is created. ex: "5656565656565656"
    - name [string]: embossing kit name. ex: "stark-plastic-dark-001"
    - designs [list of IssuingDesign objects]: list of IssuingDesign objects. ex: [IssuingDesign(), IssuingDesign()]
    - updated [datetime.datetime]: latest update datetime for the IssuingEmbossingKit. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - created [datetime.datetime]: creation datetime for the IssuingEmbossingKit. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, id=None, name=None, designs=None, created=None, updated=None):
        Resource.__init__(self, id=id)

        self.name = name
        self.designs = parse_designs(designs)
        self.created = check_datetime(created)
        self.updated = check_datetime(updated)


_resource = {"class": IssuingEmbossingKit, "name": "IssuingEmbossingKit"}


def query(limit=None, after=None, before=None, status=None, design_ids=None, ids=None, user=None):
    """# Retrieve IssuingEmbossingKits
    Receive a generator of IssuingEmbossingKit objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. ex: ["created", "processing", "success", "failed"]
    - design_ids [list of string, default None]: list of design_ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - generator of IssuingEmbossingKit objects with updated attributes
    """
    return rest.get_stream(
        resource=_resource,
        limit=limit,
        after=after,
        before=before,
        status=status,
        design_ids=design_ids,
        ids=ids,
        user=user
    )


def page(cursor=None, limit=None, after=None, before=None, status=None, design_ids=None, ids=None, user=None):
    """# Retrieve paged IssuingEmbossingKits
    Receive a list of up to 100 IssuingEmbossingKit objects previously created in the Stark Infra API and the cursor to the next page.
    Use this function instead of query if you want to manually page your requests.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - limit [integer, default 100]: maximum number of objects to be retrieved. Max = 100. ex: 35
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. ex: ["created", "processing", "success", "failed"]
    - design_ids [list of string, default None]: list of design_ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of IssuingEmbossingKit objects with updated attributes
    - cursor to retrieve the next page of IssuingEmbossingKit objects
    """
    return rest.get_page(
        resource=_resource,
        cursor=cursor,
        limit=limit,
        after=after,
        before=before,
        status=status,
        design_ids=design_ids,
        ids=ids,
        user=user
    )


def get(id, user=None):
    """# Retrieve a specific IssuingEmbossingKit
    Receive a single IssuingEmbossingKit object previously created in the Stark Infra API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - IssuingEmbossingKit object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)
