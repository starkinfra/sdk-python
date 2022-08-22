from json import dumps
from ..utils import rest
from ..utils import parse
from starkcore.utils.api import api_json
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime, check_date


class DynamicBrcode(Resource):
    """# DynamicBrcode object
    BR codes store information represented by Pix QR Codes, which are used to
    send or receive Pix transactions in a convenient way.
    DynamicBrcodes represent charges with information that can change at any time,
    since all data needed for the payment is requested dynamically to an URL stored
    in the BR Code. Stark Infra will receive the GET request and forward it to your
    registered endpoint with a GET request containing the UUID of the BR code for
    identification.
    When you initialize a DynamicBrcode, the entity will not be automatically
    created in the Stark Infra API. The 'create' function sends the objects
    to the Stark Infra API and returns the created object.
    ## Parameters (required):
    - name [string]: receiver's name. ex: "Tony Stark"
    - city [string]: receiver's city name. ex: "Rio de Janeiro"
    - external_id [string]: string that must be unique among all your DynamicBrcodes. Duplicated external ids will cause failures. ex: "my-internal-id-123456"
    ## Parameters (optional):
    - type [string, default "instant"]: type of the DynamicBrcode. Options: "instant", "due"
    - tags [list of strings, default []]: list of strings for tagging. ex: ["travel", "food"]
    ## Attributes (return-only):
    - id [string]: id returned on creation, this is the BR code. ex: "00020126360014br.gov.bcb.pix0114+552840092118152040000530398654040.095802BR5915Jamie Lannister6009Sao Paulo620705038566304FC6C"
    - uuid [string]: unique uuid returned when the DynamicBrcode is created. ex: "4e2eab725ddd495f9c98ffd97440702d"
    - url [string]: url link to the BR code image. ex: "https://brcode-h.development.starkinfra.com/dynamic-qrcode/901e71f2447c43c886f58366a5432c4b.png"
    - updated [datetime.datetime]: latest update datetime for the DynamicBrcode. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - created [datetime.datetime]: creation datetime for the DynamicBrcode. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, name, city, external_id, id=None, type=None, tags=None, uuid=None, url=None, 
                    updated=None, created=None):
        Resource.__init__(self, id=id)

        self.name = name
        self.city = city
        self.external_id = external_id
        self.type = type
        self.tags = tags
        self.uuid = uuid
        self.url = url
        self.updated = check_datetime(updated)
        self.created = check_datetime(created)


_resource = {"class": DynamicBrcode, "name": "DynamicBrcode"}


def create(brcodes, user=None):
    """# Create DynamicBrcodes
    Send a list of DynamicBrcode objects for creation at the Stark Infra API
    ## Parameters (required):
    - brcodes [list of DynamicBrcode objects]: list of DynamicBrcode objects to be created in the API.
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - list of DynamicBrcode objects with updated attributes
    """
    return rest.post_multi(resource=_resource, entities=brcodes, user=user)


def get(uuid, user=None):
    """# Retrieve a specific DynamicBrcode
    Receive a single DynamicBrcode object previously created in the Stark Infra API by its uuid
    ## Parameters (required):
    - uuid [string]: object's unique uuid. ex: "901e71f2447c43c886f58366a5432c4b"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - DynamicBrcode object with updated attributes
    """
    return rest.get_id(resource=_resource, id=uuid, user=user)


def query(limit=None, after=None, before=None, external_id=None, uuids=None, tags=None, user=None):
    """# Retrieve DynamicBrcodes
    Receive a generator of DynamicBrcode objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - external_ids [list of strings, default None]: list of external_ids to filter retrieved objects. ex: ["my_external_id1", "my_external_id2"]
    - uuids [list of strings, default None]: list of uuids to filter retrieved objects. ex: ["901e71f2447c43c886f58366a5432c4b", "4e2eab725ddd495f9c98ffd97440702d"]
    - tags [list of strings, default None]: list of tags to filter retrieved objects. ex: ["travel", "food"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - generator of DynamicBrcode objects with updated attributes
    """
    return rest.get_stream(
        resource=_resource,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        external_id=external_id,
        uuids=uuids,
        tags=tags,
        user=user,
    )


def page(cursor=None, limit=None, after=None, before=None, external_id=None, uuids=None, tags=None, user=None):
    """# Retrieve DynamicBrcodes
    Receive a list of DynamicBrcode objects previously created in the Stark Infra API and the cursor to the next page.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - limit [integer, default 100]: maximum number of objects to be retrieved. Max = 100. ex: 35
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - external_ids [list of strings, default None]: list of external_ids to filter retrieved objects. ex: ["my_external_id1", "my_external_id2"]
    - uuids [list of strings, default None]: list of uuids to filter retrieved objects. ex: ["901e71f2447c43c886f58366a5432c4b", "4e2eab725ddd495f9c98ffd97440702d"]
    - tags [list of strings, default None]: list of tags to filter retrieved objects. ex: ["travel", "food"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - list of DynamicBrcode objects with updated attributes
    - cursor to retrieve the next page of DynamicBrcode objects
    """
    return rest.get_page(
        resource=_resource,
        cursor=cursor,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        external_id=external_id,
        uuids=uuids,
        tags=tags,
        user=user,
    )


def response_due(version, created, due, key_id, status, reconciliation_id, nominal_amount, sender_name, receiver_name,
                 receiver_street_line, receiver_city, receiver_state_code, receiver_zip_code, expiration=None,
                 sender_tax_id=None, receiver_tax_id=None, fine=None, interest=None, discounts=None,
                 description=None):
    """# Helps you respond to a due DynamicBrcode Read
    When a Due DynamicBrcode is read by your user, a GET request containing the Brcode's 
    UUID will be made to your registered URL to retrieve additional information needed 
    to complete the transaction.
    The get request must be answered in the following format, within 5 seconds, and with 
    an HTTP status code 200.
    ## Parameters (required):
    - version [integer]: integer that represents how many times the BR code was updated.
    - created [datetime.datetime or string]: creation datetime in ISO format of the DynamicBrcode. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - due [datetime.datetime or string]: requested payment due datetime in ISO format. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - key_id [string]: receiver's PixKey id. Can be a tax_id (CPF/CNPJ), a phone number, an email or an alphanumeric sequence (EVP). ex: "+5511989898989"
    - status [string]: BR code status. Options: "created", "overdue", "paid", "canceled" or "expired"
    - reconciliation_id [string]: id to be used for conciliation of the resulting Pix transaction. This id must have from to 26 to 35 alphanumeric characters ex: "cd65c78aeb6543eaaa0170f68bd741ee"
    - nominal_amount [integer]: positive integer that represents the amount in cents of the resulting Pix transaction. ex: 1234 (= R$ 12.34)
    - sender_name [string]: sender's full name. ex: "Anthony Edward Stark"
    - receiver_name [string]: receiver's full name. ex: "Jamie Lannister"
    - receiver_street_line [string]: receiver's main address. ex: "Av. Paulista, 200"
    - receiver_city [string]: receiver's address city name. ex: "Sao Paulo"
    - receiver_state_code [string]: receiver's address state code. ex: "SP"
    - receiver_zip_code [string]: receiver's address zip code. ex: "01234-567"
    ## Parameters (optional):
    - expiration [datime.timedelta or integer, default 86400 (1 day)]: time in seconds counted from the creation datetime until the DynamicBrcode expires. After expiration, the BR code cannot be paid anymore.
    - sender_tax_id [string, default None]: sender's CPF (11 digits formatted or unformatted) or CNPJ (14 digits formatted or unformatted). ex: "01.001.001/0001-01"
    - receiver_tax_id [string, default None]: receiver's CPF (11 digits formatted or unformatted) or CNPJ (14 digits formatted or unformatted). ex: "012.345.678-90"
    - fine [float, default 2.0]: Percentage charged if the sender pays after the due datetime.
    - interest [float, default 1.0]: Interest percentage charged if the sender pays after the due datetime.
    - discounts [list of dictionaries, default None]: list of dictionaries with "percentage":float and "due":date.datetime or string pairs.
    - description [string, default None]: additional information to be shown to the sender at the moment of payment.
    ## Return:
    - Dumped JSON string that must be returned to us
    """
    params = {
        "version": version,
        "created": created,
        "due": due,
        "keyId": key_id,
        "status": status,
        "reconciliationId": reconciliation_id,
        "nominalAmount": nominal_amount,
        "senderName": sender_name,
        "receiverName": receiver_name,
        "receiverStreetLine": receiver_street_line,
        "receiverCity": receiver_city,
        "receiverStateCode": receiver_state_code,
        "receiverZipCode": receiver_zip_code,
        "expiration": expiration,
        "senderTaxId": sender_tax_id,
        "receiverTaxId": receiver_tax_id,
        "fine": fine,
        "interest": interest,
        "discounts": discounts,
        "description": description,
    }
    return dumps(api_json(params))


def response_instant(version, created, key_id, status, reconciliation_id, amount, expiration=None, sender_name=None, sender_tax_id=None,
                    description=None, amount_type=None, cash_amount=None, cashier_type=None, cashier_bank_code=None):
    """# Helps you respond to an instant DynamicBrcode Read
    When an instant DynamicBrcode is read by your user, a GET request containing the BR code's UUID will be made
    to your registered URL to retrieve additional information needed to complete the transaction.
    The get request must be answered in the following format within 5 seconds and with an HTTP status code 200.
    ## Parameters (required):
    - version [integer]: integer that represents how many times the BR code was updated.
    - created [datetime.datetime or string]: creation datetime of the DynamicBrcode. ex: "2022-05-17"
    - key_id [string]: receiver's PixKey id. Can be a tax_id (CPF/CNPJ), a phone number, an email or an alphanumeric sequence (EVP). ex: "+5511989898989"
    - status [string]: BR code status. Options: "created", "overdue", "paid", "canceled" or "expired"
    - reconciliation_id [string]: id to be used for conciliation of the resulting Pix transaction. ex: "cd65c78aeb6543eaaa0170f68bd741ee"
    - amount [integer]: positive integer that represents the amount in cents of the resulting Pix transaction. ex: 1234 (= R$ 12.34)
    ## Parameters (conditionally-required):
    - cashier_type [string, default None]: cashier's type. Required if the cashAmount is different from 0. Options: "merchant", "participant" and "other"
    - cashier_bank_code [string, default None]: cashier's bank code. Required if the cashAmount is different from 0. ex: "20018183"
    ## Parameters (optional):
    - cash_amount [integer, default 0]: amount to be withdrawn from the cashier in cents. ex: 1000 (= R$ 10.00)
    - expiration [datetime.timedelta or integer, default 86400 (1 day)]: time in seconds counted from the creation datetime until the DynamicBrcode expires. After expiration, the BR code cannot be paid anymore. Default value: 86400 (1 day)
    - sender_name [string, default None]: sender's full name. ex: "Anthony Edward Stark"
    - sender_tax_id [string, default None]: sender's CPF (11 digits formatted or unformatted) or CNPJ (14 digits formatted or unformatted). ex: "01.001.001/0001-01"
    - amount_type [string, default "fixed"]: amount type of the Brcode. If the amount type is "custom" the Brcode's amount can be changed by the sender at the moment of payment. Options: "fixed"or "custom"
    - description [string, default None]: additional information to be shown to the sender at the moment of payment.
    ## Return:
    - Dumped JSON string that must be returned to us
    """
    params = {
        "version": version,
        "created": created,
        "keyId": key_id,
        "status": status,
        "reconciliationId": reconciliation_id,
        "amount": amount,
        "cashierType": cashier_type,
        "cashierBankCode": cashier_bank_code,
        "cashAmount": cash_amount,
        "expiration": expiration,
        "senderName": sender_name,
        "senderTaxId": sender_tax_id,
        "amountType": amount_type,
        "description": description,
    }
    return dumps(api_json(params))


def verify(uuid, signature, user=None):
    """# Verify a DynamicBrcode Read 
    When a DynamicBrcode is read by your user, a GET request will be made to your registered URL to
    retrieve additional information needed to complete the transaction.
    Use this method to verify the authenticity of a GET request received at your registered endpoint.
    If the provided digital signature does not check out with the StarkInfra public key,
    a stark.exception.InvalidSignatureException will be raised.
    ## Parameters (required):
    - uuid [string]: unique uuid returned when a DynamicBrcode is created. ex: "4e2eab725ddd495f9c98ffd97440702d"
    - signature [string]: base-64 digital signature received at response header "Digital-Signature"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - verified Brcode's uuid.
    """
    return parse.verify(
        content=uuid,
        signature=signature,
        user=user,
    )
