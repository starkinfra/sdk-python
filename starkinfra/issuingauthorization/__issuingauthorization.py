from json import loads, dumps
from requests import get as get_request
from starkbank.error import InvalidSignatureError
from ellipticcurve import Ecdsa, Signature, PublicKey
from ..utils import cache
from ..utils.request import fetch
from ..utils.resource import Resource
from ..utils.api import from_api_json


class IssuingAuthorization(Resource):
    """# IssuingAuthorization object
    An IssuingAuthorization is the received purchase data to be analysed and answered with the approval or decline.
    ## Attributes:
    - end_to_end_id [string, default None]: central bank's unique transaction ID. ex: "E79457883202101262140HHX553UPqeq"
    - amount [integer, default None]: IssuingPurchase value in cents. Minimum = 0 (any value will be accepted). ex: 1234 (= R$ 12.34)
    - tax [integer, default 0]: IOF amount taxed for international purchases. ex: 1234 (= R$ 12.34)
    - card_id [string, default None]: unique id returned when IssuingCard is created. ex: "5656565656565656"
    - issuer_amount [integer, default None]: issuer amount. ex: 1234 (= R$ 12.34)
    - issuer_currency_code [string, default None]: issuer currency code. ex: "USD"
    - merchant_amount [integer, default None]: merchant amount. ex: 1234 (= R$ 12.34)
    - merchant_currency_code [string, default None]: merchant currency code. ex: "USD"
    - merchant_category_code [string, default None]: merchant category code. ex: "eatingPlacesRestaurants"
    - merchant_country_code [string, default None]: merchant country code. ex: "USA"
    - acquirer_id [string, default None]: acquirer ID. ex: "5656565656565656"
    - merchant_id [string, default None]: merchant ID. ex: "5656565656565656"
    - merchant_name [string, default None]: merchant name. ex: "Google Cloud Platform"
    - merchant_fee [integer, default None]: merchant fee charged. ex: 200 (= R$ 2.00)
    - wallet_id [string, default None]: virtual wallet ID. ex: "5656565656565656"
    - method_code [string, default None]: method code. ex: "chip", "token", "server", "manual", "magstripe" or "contactless"
    - score [float, default 0.0]: internal score calculated for the authenticity of the purchase. ex: 7.6
    - is_partial_allowed [bool, default False]: true if the the merchant allows partial purchases. ex: False
    - purpose [string, default None]: purchase purpose. ex: "purchase"
    - card_tags [list of strings, default None]: list of tags of the IssuingCard. ex: ["travel", "food"]
    - holder_tags [list of strings, default None]: list of tags of the IssuingHolder. ex: ["travel", "food"]
    """

    def __init__(self, end_to_end_id, amount, tax, card_id, issuer_amount, issuer_currency_code, merchant_amount,
                 merchant_currency_code, merchant_category_code, merchant_country_code, acquirer_id, merchant_id,
                 merchant_name, merchant_fee, wallet_id, method_code, score, is_partial_allowed, purpose, card_tags,
                 holder_tags, id):
        super().__init__(id)
        self.end_to_end_id = end_to_end_id
        self.amount = amount
        self.tax = tax
        self.card_id = card_id
        self.issuer_amount = issuer_amount
        self.issuer_currency_code = issuer_currency_code
        self.merchant_amount = merchant_amount
        self.merchant_currency_code = merchant_currency_code
        self.merchant_category_code = merchant_category_code
        self.merchant_country_code = merchant_country_code
        self.acquirer_id = acquirer_id
        self.merchant_id = merchant_id
        self.merchant_name = merchant_name
        self.merchant_fee = merchant_fee
        self.wallet_id = wallet_id
        self.method_code = method_code
        self.score = score
        self.is_partial_allowed = is_partial_allowed
        self.purpose = purpose
        self.card_tags = card_tags
        self.holder_tags = holder_tags


_resource = {"class": IssuingAuthorization, "name": "IssuingAuthorization"}


def parse(content, signature, user=None):
    """# Create single IssuingAuthorization from a content string
    Create a single IssuingAuthorization object received from IssuingAuthorization at the informed endpoint.
    If the provided digital signature does not check out with the StarkBank public key, a
    starkbank.exception.InvalidSignatureException will be raised.
    ## Parameters (required):
    - content [string]: response content from request received at user endpoint (not parsed)
    - signature [string]: base-64 digital signature received at response header "Digital-Signature"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkbank.user was set before function call
    ## Return:
    - Parsed IssuingAuthorization object
    """
    authorization = from_api_json(_resource, loads(content))

    try:
        signature = Signature.fromBase64(signature)
    except:
        raise InvalidSignatureError("The provided signature is not valid")

    public_key = _get_public_key(user=user)
    if _is_valid(content=content, signature=signature, public_key=public_key):
        return authorization

    public_key = _get_public_key(user=user, refresh=True)
    if _is_valid(content=content, signature=signature, public_key=public_key):
        return authorization

    raise InvalidSignatureError("The provided signature and content do not match the Stark Infra public key")


def _is_valid(content, signature, public_key):
    if Ecdsa.verify(message=content, signature=signature, publicKey=public_key):
        return True

    normalized = dumps(loads(content), sort_keys=True)
    if Ecdsa.verify(message=normalized, signature=signature, publicKey=public_key):
        return True

    return False


def _get_public_key(user, refresh=False):
    public_key = cache.get("starkinfra-public-key")
    if public_key and not refresh:
        return public_key

    pem = fetch(method=get_request, path="/public-key", query={"limit": 1}, user=user).json()["publicKeys"][0][
        "content"]
    public_key = PublicKey.fromPem(pem)
    cache["starkinfra-public-key"] = public_key
    return public_key
