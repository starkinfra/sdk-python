from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime, check_date
from ..utils import rest


class StaticBrcode(Resource):
    """# StaticBrcode object
    A StaticBrcode stores account information in the form of a PixKey and can be used to create 
    Pix transactions easily.
    When you initialize a StaticBrcode, the entity will not be automatically
    created in the Stark Infra API. The 'create' function sends the objects
    ## Parameters (required):
    - name [string]: receiver's name. ex: "Tony Stark"
    - key_id [string]: receiver's Pixkey id. ex: "+5541999999999"
    - city [string]: receiver's city name. ex: "Rio de Janeiro"
    ## Parameters (optional):
    - amount [integer, default 0]: positive integer that represents the amount in cents of the resulting Pix transaction. ex: 1234 (= R$ 12.34)
    - cashier_bank_code [string, default None]: Cashier's bank code. ex: "20018183".
    - reconciliation_id [string, default None]: id to be used for conciliation of the resulting Pix transaction. This id must have up to 25 alphanumeric characters ex: "ah27s53agj6493hjds6836v49"
    - description [string, default None]: optional description to override default description to be shown in the bank statement. ex: "Payment for service #1234"
    - tags [list of strings, default []]: list of strings for tagging. ex: ["travel", "food"]
    ## Attributes (return-only):
    - id [string]: id returned on creation, this is the BR code. ex: "00020126360014br.gov.bcb.pix0114+552840092118152040000530398654040.095802BR5915Jamie Lannister6009Sao Paulo620705038566304FC6C"
    - uuid [string]: unique uuid returned when a StaticBrcode is created. ex: "97756273400d42ce9086404fe10ea0d6"
    - url [string]: url link to the BR code image. ex: "https://brcode-h.development.starkinfra.com/static-qrcode/97756273400d42ce9086404fe10ea0d6.png"
    - updated [datetime.datetime]: latest update datetime for the StaticBrcode. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - created [datetime.datetime]: creation datetime for the StaticBrcode. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, name, key_id, city, amount=None, cashier_bank_code=None, reconciliation_id=None, tags=None,
                 id=None, description=None, uuid=None, url=None, updated=None, created=None):
        Resource.__init__(self, id=id)

        self.name = name
        self.key_id = key_id
        self.city = city
        self.amount = amount
        self.cashier_bank_code = cashier_bank_code
        self.reconciliation_id = reconciliation_id
        self.description = description
        self.tags = tags
        self.uuid = uuid
        self.url = url
        self.updated = check_datetime(updated)
        self.created = check_datetime(created)


_resource = {"class": StaticBrcode, "name": "StaticBrcode"}


def create(brcodes, user=None):
    """# Create StaticBrcodes
    Send a list of StaticBrcode objects for creation at the Stark Infra API
    ## Parameters (required):
    - brcodes [list of StaticBrcode objects]: list of StaticBrcode objects to be created in the API.
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - list of StaticBrcode objects with updated attributes
    """
    return rest.post_multi(resource=_resource, entities=brcodes, user=user)


def get(uuid, user=None):
    """# Retrieve a specific StaticBrcode
    Receive a single StaticBrcode object previously created in the Stark Infra API by its uuid
    ## Parameters (required):
    - uuid [string]: object's unique uuid. ex: "97756273400d42ce9086404fe10ea0d6"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - StaticBrcode object with updated attributes
    """
    return rest.get_id(resource=_resource, id=uuid, user=user)


def query(limit=None, after=None, before=None, uuids=None, tags=None, user=None):
    """# Retrieve StaticBrcodes
    Receive a generator of StaticBrcode objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - uuids [list of strings, default None]: list of uuids to filter retrieved objects. ex: ["97756273400d42ce9086404fe10ea0d6", "e3da0b6d56fa4045b9b295b2be82436e"]
    - tags [list of strings, default None]: list of tags to filter retrieved objects. ex: ["travel", "food"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - generator of StaticBrcode objects with updated attributes
    """
    return rest.get_stream(
        resource=_resource,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        uuids=uuids,
        tags=tags,
        user=user,
    )


def page(cursor=None, limit=None, after=None, before=None, uuids=None, tags=None, user=None):
    """# Retrieve paged StaticBrcodes
    Receive a list of up to 100 StaticBrcode objects previously created in the Stark Infra API and the cursor to the next page.
    Use this function instead of query if you want to manually page your requests.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - limit [integer, default 100]: maximum number of objects to be retrieved. Max = 100. ex: 35
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - uuids [list of strings, default None]: list of uuids to filter retrieved objects. ex: ["97756273400d42ce9086404fe10ea0d6", "e3da0b6d56fa4045b9b295b2be82436e"]
    - tags [list of strings, default None]: list of tags to filter retrieved objects. ex: ["travel", "food"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - list of StaticBrcode objects with updated attributes
    - cursor to retrieve the next page of StaticBrcode objects
    """
    return rest.get_page(
        resource=_resource,
        cursor=cursor,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        uuids=uuids,
        tags=tags,
        user=user,
    )
