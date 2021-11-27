from ..utils import rest
from ..utils.resource import Resource
from ..utils.checks import check_datetime



class IssuingCard(Resource):
    """# IssuingCard object
    The IssuingCard object displays the informations of Cards created to your Workspace.
    ## Parameters (required):
    - holder_name [string]: card holder name.
    - holder_tax_id [string]: card holder tax ID
    - holder_external_id [string] card holder external ID
    ## Parameters (optional):
    - display_name [string, default None]: card displayed name
    - rules [list of dictionaries, default None]: list of dictionaries with "amount": int, "currencyCode": string, "id": string, "interval": string, "name": string pairs
    - bin_id [string, default None]: BIN ID. ex: 12810201
    - tags [list of strings]: list of strings for tagging
    - street_line_1 [string, default None]: card holder main address. ex: Av. Paulista, 200
    - street_line_2 [string, default None]: card holder address complement. ex: Apto. 123
    - district [string]: card holder address district / neighbourhood. ex: Bela Vista
    - city [string, default None]: card holder address city. ex: Rio de Janeiro
    - state_code [string, default None]: card holder address state. ex: GO
    - zip_code [string]: card holder address zip code. ex: 01311-200
    ## Attributes (return-only):
    - id [string, default None]: unique id returned when Issuing Card is created. ex: "5656565656565656"
    - holder_id [string, default None]: card holder unique id.
    - type [string, default None]: card type. ex: "virtual"
    - status [string, default None]: current Issuing Card status. ex: "canceled" or "active"
    - number [string, default None]: card number. ex: "1234 5678 1234 5678"
    - security_code [string, default None]: card verification value (cvv). ex: "123"
    - expiration [string, default None]: expiration datetime for the Card. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - updated [datetime.datetime, default None]: latest update datetime for the bin. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - created [datetime.datetime, default None]: creation datetime for the bin. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, holder_name, holder_tax_id, holder_external_id, id=None, holder_id=None, type=None, display_name=None, status=None,
                 rules=None, bin_id=None, street_line_1=None, street_line_2=None, district=None, city=None, state_code=None, zip_code=None,
                 tags=None, created=None, updated=None, number=None, security_code=None, expiration=None):
        super().__init__(id)
        self.id = id
        self.holder_id = holder_id
        self.holder_name = holder_name
        self.holder_tax_id = holder_tax_id
        self.holder_external_id = holder_external_id
        self.type = type
        self.display_name = display_name
        self.status = status
        self.rules = rules
        self.bin_id = bin_id
        self.street_line_1 = street_line_1
        self.street_line_2 = street_line_2
        self.district = district
        self.city = city
        self.state_code = state_code
        self.zip_code = zip_code
        self.tags = tags
        self.created = check_datetime(created)
        self.updated = check_datetime(updated)
        self.number = number
        self.security_code = security_code
        self.expiration = expiration


_resource = {"class": IssuingCard, "name": "IssuingCard"}


def create(cards, user=None):
    """# Create Issuing Cards
    Send a list of Issuing Card objects for creation in the Stark Infra API
    ## Parameters (required):
    - cards [list of IssuingCard objects]: list of Issuing Card objects to be created in the API
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - list of Issuing Card objects with updated attributes
    """
    return rest.post_multi(resource=_resource, entities=cards, user=user)


def query(status=None, types=None, holder_ids=None, after=None, before=None, tags=None, ids=None, limit=None, expand=None, user=None):
    """# Retrieve Issuing Cards
    Receive a generator of Issuing Cards objects previously created in the Stark Infra API
    ## Parameters (optional):
    - status [string, default None]: filter for status of retrieved objects. ex: "paid" or "registered"
    - types [string, default None]: card type. ex: "virtual"
    - holder_ids [list of strings]: card holder IDs. ex: ["5656565656565656", "4545454545454545"]
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - expand [string, default None]: fields to to expand information. ex: "rules, securityCode, number, expiration"
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - generator of Issuing Cards objects with updated attributes
    """
    return rest.get_stream(
        resource=_resource,
        status=status,
        types=types,
        holder_ids=holder_ids,
        after=check_datetime(after),
        before=check_datetime(before),
        tags=tags,
        ids=ids,
        limit=limit,
        expand=expand,
        user=user,
    )


def page(status=None, types=None, holder_ids=None, after=None, before=None, tags=None, ids=None,
         limit=None, cursor=None, expand=None, user=None):
    """# Retrieve paged Issuing Cards
    Receive a list of Issuing Cards objects previously created in the Stark Infra API and the cursor to the next page.
    ## Parameters (optional):
    - status [string, default None]: filter for status of retrieved objects. ex: "paid" or "registered"
    - types [string, default None]: card type. ex: "virtual"
    - holder_ids [list of strings]: card holder IDs. ex: ["5656565656565656", "4545454545454545"]
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - cursor [string, default None]: cursor returned on the previous page function call
    - expand [string, default None]: fields to to expand information. ex: "rules, securityCode, number, expiration"
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - list of Issuing Cards objects with updated attributes
    - cursor to retrieve the next page of Issuing Cards objects
    """
    return rest.get_page(
        resource=_resource,
        status=status,
        types=types,
        holder_ids=holder_ids,
        after=check_datetime(after),
        before=check_datetime(before),
        tags=tags,
        ids=ids,
        limit=limit,
        cursor=cursor,
        expand=expand,
        user=user,
    )


def get(id, user=None):
    """# Retrieve a specific Issuing Cards
    Receive a single Issuing Cards object previously created in the Stark Infra API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - Issuing Cards object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def update(id, status=None, display_name=None, rules=None, tags=None, user=None):
    """# Update Issuing Card entity
    Update an Issuing Card by passing id.
    ## Parameters (required):
    - id [string]: Issuing Card id. ex: '5656565656565656'
    ## Parameters (optional):
    - status [string]: You may block the Issuing Card by passing 'blocked' in the status
    - display_name [string, default None]: card displayed name
    - rules [list of dictionaries, default None]: list of dictionaries with "amount": int, "currencyCode": string, "id": string, "interval": string, "name": string pairs.
    - tags [list of strings]: list of strings for tagging
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - target Issuing Card with updated attributes
    """
    payload = {
        "status": status,
        "display_name": display_name,
        "rules": rules,
        "tags": tags,
    }
    return rest.patch_id(resource=_resource, id=id, user=user, **payload)


def delete(id, user=None):
    """# Delete a Issuing Card entity
    Delete a Issuing Card entity previously created in the Stark Infra API
    ## Parameters (required):
    - id [string]: Issuing Card unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - deleted Issuing Card object
    """
    return rest.delete_id(resource=_resource, id=id, user=user)
