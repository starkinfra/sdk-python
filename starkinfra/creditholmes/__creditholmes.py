from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime, check_date
from ..utils import rest


class CreditHolmes(Resource):
    """# CreditHolmes object
    CreditHolmes are used to obtain debt information on your customers.
    Before you create a CreditHolmes, make sure you have your customer's express
    authorization to verify their information in the Central Bank's SCR.
    When you initialize a CreditHolmes, the entity will not be automatically
    created in the Stark Infra API. The 'create' function sends the objects
    to the Stark Infra API and returns the list of created objects.
    ## Parameters (required):
    - tax_id [string]: customer's tax ID (CPF or CNPJ) for whom the credit operations will be verified. ex: "20.018.183/0001-80"
    Parameters (optional):
    - competence [string, default 'two months before current date']: competence month of the operation verification, format: "YYYY-MM". ex: "2021-04"
    - tags [list of strings, default []]: list of strings for reference when searching for CreditHolmes. ex: [credit", "operation"]
    Attributes (return-only):
    - id [string]: unique id returned when the CreditHolmes is created. ex: "5656565656565656"
    - result [dictionary]: result of the investigation after the case is solved.
    - status [string]: current status of the CreditHolmes. ex: "created", "failed", "success"
    - created [datetime.datetime]: creation datetime for the CreditHolmes. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - updated [datetime.datetime]: latest update datetime for the CreditHolmes. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, tax_id, competence, result=None, tags=None, id=None, status=None, created=None, updated=None):
        Resource.__init__(self, id=id)

        self.tax_id = tax_id
        self.competence = competence
        self.status = status
        self.tags = tags
        self.result = result
        self.created = check_datetime(created)
        self.updated = check_datetime(updated)


_resource = {"class": CreditHolmes, "name": "CreditHolmes"}


def create(holmes, user=None):
    """# Create CreditHolmes
    Send a list of CreditHolmes objects for creation at the Stark Infra API
    ## Parameters (required):
    - holmes [list of CreditHolmes objects]: list of CreditHolmes objects to be created in the API
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of CreditHolmes objects with updated attributes
    """
    return rest.post_multi(resource=_resource, entities=holmes, user=user)


def get(id, user=None):
    """# Retrieve a specific CreditHolmes
    Receive a single CreditHolmes object previously created in the Stark Infra API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - CreditHolmes object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def query(limit=None, status=None, tags=None, ids=None, after=None, before=None, user=None):
    """# Retrieve CreditHolmes
    Receive a generator of CreditHolmes objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. ex: "created", "failed", "success"
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - generator of CreditHolmes objects with updated attributes
    """
    return rest.get_stream(
        resource=_resource,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        status=status,
        tags=tags,
        ids=ids,
        user=user,
    )


def page(cursor=None, limit=None, status=None, tags=None, ids=None, after=None, before=None, user=None):
    """# Retrieve paged CreditHolmes
    Receive a list of up to 100 CreditHolmes objects previously created in the Stark Infra API and the cursor to the next page.
    Use this function instead of query if you want to manually page your requests.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - limit [integer, default 100]: maximum number of objects to be retrieved. It must be an integer between 1 and 100. ex: 50
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. ex: "created", "failed", "success"
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of CreditHolmes objects with updated attributes
    - cursor to retrieve the next page of CreditHolmes objects
    """
    return rest.get_page(
        resource=_resource,
        cursor=cursor,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        status=status,
        tags=tags,
        ids=ids,
        user=user,
    )
