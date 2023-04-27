from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_date, check_datetime
from ..utils import rest


class IssuingEmbossingRequest(Resource):
    """# IssuingEmbossingRequest object
    The IssuingEmbossingRequest object displays the information of embossing requests in your Workspace.
    ## Parameters (required):
    - card_id [string]: id of the IssuingCard to be embossed. ex "5656565656565656"
    - kit_id [string]: card embossing kit id. ex "5656565656565656"
    - display_name_1 [string]: card displayed name. ex: "ANTHONY STARK"
    - shipping_city [string]: shipping city. ex: "NEW YORK"
    - shipping_country_code [string]: shipping country code. ex: "US"
    - shipping_district [string]: shipping district. ex: "NY"
    - shipping_state_code [string]: shipping state code. ex: "NY"
    - shipping_street_line_1 [string]: shipping main address. ex: "AVENUE OF THE AMERICAS"
    - shipping_street_line_2 [string]: shipping address complement. ex: "Apt. 6"
    - shipping_service [string]: shipping service. ex: "loggi"
    - shipping_tracking_number [string]: shipping tracking number. ex: "5656565656565656"
    - shipping_zip_code [string]: shipping zip code. ex: "12345-678"
    ## Parameters (optional):
    - embosser_id [string]: id of the card embosser. ex: "5656565656565656"
    - display_name_2 [string]: card displayed name. ex: "IT Services"
    - display_name_3 [string]: card displayed name. ex: "StarkBank S.A."
    - shipping_phone [string]: shipping phone. ex: "+5511999999999"
    - tags [list of strings, default None]: list of strings for tagging. ex: ["card", "corporate"]
    ## Attributes (return-only):
    - id [string]: unique id returned when IssuingEmbossingRequest is created. ex: "5656565656565656"
    - fee [integer]: fee charged when IssuingEmbossingRequest is created. ex: 1000
    - status [string]: status of the IssuingEmbossingRequest. ex: "created", "processing", "success", "failed"
    - updated [datetime.datetime]: latest update datetime for the IssuingEmbossingRequest. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - created [datetime.datetime]: creation datetime for the IssuingEmbossingRequest. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, card_id, kit_id, display_name_1, shipping_city,
                 shipping_country_code, shipping_district, shipping_state_code, shipping_street_line_1, 
                 shipping_street_line_2, shipping_service, shipping_tracking_number, shipping_zip_code, 
                 embosser_id=None, display_name_2=None, display_name_3=None, shipping_phone=None, 
                 tags=None, id=None, fee=None, status=None, updated=None, created=None):
        Resource.__init__(self, id=id)

        self.card_id = card_id
        self.kit_id = kit_id
        self.display_name_1 = display_name_1
        self.shipping_city = shipping_city
        self.shipping_country_code = shipping_country_code
        self.shipping_district = shipping_district
        self.shipping_state_code = shipping_state_code
        self.shipping_street_line_1 = shipping_street_line_1
        self.shipping_street_line_2 = shipping_street_line_2
        self.shipping_service = shipping_service
        self.shipping_tracking_number = shipping_tracking_number
        self.shipping_zip_code = shipping_zip_code
        self.embosser_id = embosser_id
        self.display_name_2 = display_name_2
        self.display_name_3 = display_name_3
        self.shipping_phone = shipping_phone
        self.tags = tags
        self.fee = fee
        self.status = status
        self.created = check_datetime(created)
        self.updated = check_datetime(updated)


_resource = {"class": IssuingEmbossingRequest, "name": "IssuingEmbossingRequest"}


def create(requests, user=None):
    """# Create IssuingEmbossingRequests
    Send a list of IssuingEmbossingRequest objects for creation at the Stark Infra API
    ## Parameters (required):
    - requests [list of IssuingEmbossingRequest objects]: list of IssuingEmbossingRequest objects to be created in the API
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of IssuingEmbossingRequest objects with updated attributes
    """
    return rest.post_multi(resource=_resource, entities=requests, user=user)


def query(limit=None, after=None, before=None, status=None, card_ids=None, ids=None, tags=None, user=None):
    """# Retrieve IssuingEmbossingRequests
    Receive a generator of IssuingEmbossingRequest objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. ex: ["created", "processing", "success", "failed"]
    - card_ids [list of string, default None]: list of card_ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - generator of IssuingEmbossingRequest objects with updated attributes
    """
    return rest.get_stream(
        resource=_resource,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        status=status,
        card_ids=card_ids,
        ids=ids,
        tags=tags,
        user=user,
    )


def page(cursor=None, limit=None, after=None, before=None, status=None, card_ids=None, ids=None, tags=None, user=None):
    """# Retrieve paged IssuingEmbossingRequests
    Receive a list of up to 100 IssuingEmbossingRequest objects previously created in the Stark Infra API and the cursor to the next page.
    Use this function instead of query if you want to manually page your requests.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - limit [integer, default 100]: maximum number of objects to be retrieved. Max = 100. ex: 35
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. ex: ["created", "processing", "success", "failed"]
    - card_ids [list of string, default None]: list of card_ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of IssuingEmbossingRequest objects with updated attributes
    - cursor to retrieve the next page of IssuingEmbossingRequest objects
    """
    return rest.get_page(
        resource=_resource,
        cursor=cursor,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        status=status,
        card_ids=card_ids,
        ids=ids,
        tags=tags,
        user=user,
    )


def get(id, user=None):
    """# Retrieve a specific IssuingEmbossingRequest
    Receive a single IssuingEmbossingRequest object previously created in the Stark Infra API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - IssuingEmbossingRequest object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)
