from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_date, check_datetime
from ..utils import rest


class IssuingStock(Resource):
    """# IssuingStock object
    The IssuingStock object represents the current stock of a certain IssuingDesign linked to an Embosser available to your workspace.
    ## Attributes (return-only):
    - id [string]: unique id returned when IssuingStock is created. ex: "5656565656565656"
    - balance [integer]: [EXPANDABLE] current stock balance. ex: 1000
    - design_id [string]: IssuingDesign unique id. ex: "5656565656565656"
    - embosser_id [string]: Embosser unique id. ex: "5656565656565656"
    - updated [datetime.datetime]: latest update datetime for the IssuingStock. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - created [datetime.datetime]: creation datetime for the IssuingStock. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, balance=None, design_id=None, embosser_id=None, id=None, created=None, updated=None):
        Resource.__init__(self, id=id)

        self.balance = balance
        self.design_id = design_id
        self.embosser_id = embosser_id
        self.created = check_datetime(created)
        self.updated = check_datetime(updated)


_resource = {"class": IssuingStock, "name": "IssuingStock"}


def query(limit=None, after=None, before=None, design_ids=None, embosser_ids=None, ids=None,
          expand=None, user=None):
    """# Retrieve IssuingStocks
    Receive a generator of IssuingStock objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - design_ids [list of strings, default None]: IssuingDesign unique ids. ex: ["5656565656565656", "4545454545454545"]
    - embosser_ids [list of strings, default None]: Embosser unique ids. ex: ["5656565656565656", "4545454545454545"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - expand [list of strings, default None]: fields to expand information. ex: ["balance"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - generator of IssuingStock objects with updated attributes
    """
    return rest.get_stream(
        resource=_resource,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        design_ids=design_ids,
        embosser_ids=embosser_ids,
        ids=ids,
        expand=expand,
        user=user,
    )


def page(cursor=None, limit=None, after=None, before=None, design_ids=None, embosser_ids=None, 
         ids=None, expand=None, user=None):
    """# Retrieve paged IssuingStocks
    Receive a list of up to 100 IssuingStock objects previously created in the Stark Infra API and the cursor to the next page.
    Use this function instead of query if you want to manually page your requests.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - limit [integer, default 100]: maximum number of objects to be retrieved. Max = 100. ex: 35
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - design_ids [list of strings, default None]: IssuingDesign unique ids. ex: ["5656565656565656", "4545454545454545"]
    - embosser_ids [list of strings, default None]: Embosser unique ids. ex: ["5656565656565656", "4545454545454545"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - expand [list of strings, default None]: fields to expand information. ex: ["balance"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of IssuingStock objects with updated attributes
    - cursor to retrieve the next page of IssuingStock objects
    """
    return rest.get_page(
        resource=_resource,
        cursor=cursor,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        design_ids=design_ids,
        embosser_ids=embosser_ids,
        ids=ids,
        expand=expand,
        user=user,
    )


def get(id, expand=None, user=None):
    """# Retrieve a specific IssuingStock
    Receive a single IssuingStock object previously created in the Stark Infra API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - expand [list of strings, default None]: fields to expand information. ex: ["balance"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - IssuingStock object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, expand=expand, user=user)
