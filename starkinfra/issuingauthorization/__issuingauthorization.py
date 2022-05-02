from json import dumps
from starkcore.utils.resource import Resource
from starkinfra.utils.parse import parse_and_verify


class IssuingAuthorization(Resource):
    """# IssuingAuthorization object
    An IssuingAuthorization presents purchase data to be analysed and answered with an approval or a declination.
    ## Attributes:
    - end_to_end_id [string]: central bank's unique transaction ID. ex: "E79457883202101262140HHX553UPqeq"
    - amount [integer]: IssuingPurchase value in cents. Minimum = 0. ex: 1234 (= R$ 12.34)
    - tax [integer]: IOF amount taxed for international purchases. ex: 1234 (= R$ 12.34)
    - card_id [string]: unique id returned when IssuingCard is created. ex: "5656565656565656"
    - issuer_amount [integer]: issuer amount. ex: 1234 (= R$ 12.34)
    - issuer_currency_code [string]: issuer currency code. ex: "USD"
    - merchant_amount [integer]: merchant amount. ex: 1234 (= R$ 12.34)
    - merchant_currency_code [string]: merchant currency code. ex: "USD"
    - merchant_category_code [string]: merchant category code. ex: "fastFoodRestaurants"
    - merchant_country_code [string]: merchant country code. ex: "USA"
    - acquirer_id [string]: acquirer ID. ex: "5656565656565656"
    - merchant_id [string]: merchant ID. ex: "5656565656565656"
    - merchant_name [string]: merchant name. ex: "Google Cloud Platform"
    - merchant_fee [integer]: merchant fee charged. ex: 200 (= R$ 2.00)
    - wallet_id [string]: virtual wallet ID. ex: "googlePay"
    - method_code [string]: method code. ex: "chip", "token", "server", "manual", "magstripe" or "contactless"
    - score [float]: internal score calculated for the authenticity of the purchase. None in case of insufficient data. ex: 7.6
    - is_partial_allowed [bool]: true if the the merchant allows partial purchases. ex: False
    - purpose [string]: purchase purpose. ex: "purchase"
    - card_tags [list of strings]: tags of the IssuingCard responsible for this purchase. ex: ["travel", "food"]
    - holder_tags [list of strings]: tags of the IssuingHolder responsible for this purchase. ex: ["technology", "john snow"]
    """

    def __init__(self, end_to_end_id, amount, tax, card_id, issuer_amount, issuer_currency_code, merchant_amount,
                 merchant_currency_code, merchant_category_code, merchant_country_code, acquirer_id, merchant_id,
                 merchant_name, merchant_fee, wallet_id, method_code, score, is_partial_allowed, purpose, card_tags,
                 holder_tags, id):
        Resource.__init__(self, id=id)
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
    If the provided digital signature does not check out with the StarkInfra public key, a
    stark.exception.InvalidSignatureException will be raised.
    ## Parameters (required):
    - content [string]: response content from request received at user endpoint (not parsed)
    - signature [string]: base-64 digital signature received at response header "Digital-Signature"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - Parsed IssuingAuthorization object
    """
    return parse_and_verify(
        content=content,
        signature=signature,
        user=user,
        resource=_resource,
        key="",
    )


def response(status, amount=None, reason=None, tags=None):
    """# Helps you respond IssuingAuthorization requests.
    ## Parameters (required):
    - status [string]: sub-issuer response to the authorization. ex: "accepted" or "denied"
    ## Parameters (optional):
    - amount [integer, default 0]: amount in cents that was authorized. ex: 1234 (= R$ 12.34)
    - reason [string, default ""]: denial reason. ex: "other"
    - tags [list of strings, default []]: tags to filter retrieved object. ex: ["tony", "stark"]
    ## Return:
    - Dumped JSON string that must be returned to us on the IssuingAuthorization request
    """
    return dumps({"authorization": {
        "status": status,
        "amount": amount or 0,
        "reason": reason or "",
        "tags": tags or [],
    }})
