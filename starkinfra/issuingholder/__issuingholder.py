from ..utils import rest
from ..utils.resource import Resource
from ..utils.checks import check_datetime


class IssuingHolder(Resource):
    """# Issuing Holder object
    The Issuing Holder object displays the informations of Cards created to your Workspace.
    ## Parameters (required):
    - name [string]: card holder name.
    - tax_id [string]: card holder tax ID
    - external_id [string] card holder external ID
    ## Parameters (optional):
    - rules [list of IssuingRule, default None]: [EXPANDABLE] list of holder spending rules
    - tags [list of strings]: list of strings for tagging. ex: ["travel", "food"]
    ## Attributes (return-only):
    - id [string, default None]: unique id returned when Issuing Holder is created. ex: "5656565656565656"
    - status [string, default None]: current Issuing Holder status. ex: "active", "blocked" or "canceled"
    - updated [datetime.datetime, default None]: latest update datetime for the bin. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - created [datetime.datetime, default None]: creation datetime for the bin. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, id=None, external_id=None, name=None, rules=None, status=None, tags=None, tax_id=None,
                 updated=None, created=None):
        super().__init__(id)
        self.name = name
        self.tax_id = tax_id
        self.external_id = external_id
        self.status = status
        self.rules = rules
        self.tags = tags
        self.updated = check_datetime(updated)
        self.created = check_datetime(created)


_resource = {"class": IssuingHolder, "name": "IssuingHolder"}


def create(holders, user=None):
    """# Create Issuing Holder
    Send a list of Issuing Holder objects for creation in the Stark Infra API
    ## Parameters (required):
    - holders [list of Issuing Holder objects]: list of Issuing Holder objects to be created in the API
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - list of Issuing Holder objects with updated attributes
    """
    return rest.post_multi(resource=_resource, entities=holders, user=user)


def get(id, user=None):
    """# Retrieve a specific Issuing Holder
    Receive a single Issuing Holder object previously created in the Stark Infra API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - Issuing Holder object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def query(limit=None, after=None, before=None, status=None, tags=None, ids=None, expand=None, user=None):
    """# Retrieve Issuing Holders
    Receive a generator of Issuing Holder objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - status [string, default None]: filter for status of retrieved objects. ex: "paid" or "registered"
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - expand [string, default None]: fields to to expand information. ex: "rules"
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - generator of Issuing Holder objects with updated attributes
    """
    return rest.get_stream(
        resource=_resource,
        limit=limit,
        after=check_datetime(after),
        before=check_datetime(before),
        status=status,
        tags=tags,
        ids=ids,
        expand=expand,
        user=user,
    )


def page(limit=None, after=None, before=None, status=None, sort=None, tags=None, ids=None, expand=None, cursor=None, user=None):
    """# Retrieve Issuing Holders
    Receive a list of Issuing Holder objects previously created in the Stark Infra API and the cursor to the next page.
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - status [string, default None]: filter for status of retrieved objects. ex: "paid" or "registered"
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - expand [string, default None]: fields to to expand information. ex: "rules, securityCode, number, expiration"
    - cursor [string, default None]: cursor returned on the previous page function call
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - list of Issuing Holder objects with updated attributes
    - cursor to retrieve the next page of Issuing Cards objects
    """
    return rest.get_page(
        resource=_resource,
        limit=limit,
        after=check_datetime(after),
        before=check_datetime(before),
        sort=sort,
        status=status,
        tags=tags,
        ids=ids,
        expand=expand,
        cursor=cursor,
        user=user,
    )


def update(id, status=None, name=None, rules=None, tags=None, user=None):
    """# Update Issuing Holder entity
    Update an Issuing Holder by passing id, if it hasn't been paid yet.
    ## Parameters (required):
    - id [string]: Issuing Holder id. ex: '5656565656565656'
    ## Parameters (optional):
    - status [string]: You may block the Issuing Holder by passing 'blocked' in the status
    - name [string]: card holder name.
    - tags [list of strings]: list of strings for tagging
    - rules [list of dictionaries, default None]: list of dictionaries with "amount": int, "currencyCode": string, "id": string, "interval": string, "name": string pairs
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - target Issuing Holder with updated attributes
    """
    payload = {
        "status": status,
        "name": name,
        "rules": rules,
        "tags": tags,
    }
    return rest.patch_id(resource=_resource, id=id, user=user, **payload)


def delete(id, user=None):
    """# Delete a Issuing Holder entity
    Delete a Issuing Holder entity previously created in the Stark Infra API
    ## Parameters (required):
    - id [string]: Issuing Holder unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - deleted Issuing Holder object
    """
    return rest.delete_id(resource=_resource, id=id, user=user)
