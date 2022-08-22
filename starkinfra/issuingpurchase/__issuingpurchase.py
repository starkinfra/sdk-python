from json import dumps
from ..utils import rest
from ..utils.parse import parse_and_verify
from starkcore.utils.api import api_json
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime, check_date


class IssuingPurchase(Resource):
    """# IssuingPurchase object
    Displays the IssuingPurchase objects created in your Workspace.
    ## Attributes (return-only):
    - id [string]: unique id returned when IssuingPurchase is created. ex: "5656565656565656"
    - holder_name [string]: card holder name. ex: "Tony Stark"
    - card_id [string]: unique id returned when IssuingCard is created. ex: "5656565656565656"
    - card_ending [string]: last 4 digits of the card number. ex: "1234"
    - purpose [string]: purchase purpose. ex: "purchase"
    - amount [integer]: IssuingPurchase value in cents. Minimum = 0. ex: 1234 (= R$ 12.34)
    - tax [integer]: IOF amount taxed for international purchases. ex: 1234 (= R$ 12.34)
    - issuer_amount [integer]: issuer amount. ex: 1234 (= R$ 12.34)
    - issuer_currency_code [string]: issuer currency code. ex: "USD"
    - issuer_currency_symbol [string]: issuer currency symbol. ex: "$"
    - merchant_amount [integer]: merchant amount. ex: 1234 (= R$ 12.34)
    - merchant_currency_code [string]: merchant currency code. ex: "USD"
    - merchant_currency_symbol [string]: merchant currency symbol. ex: "$"
    - merchant_category_code [string]: merchant category code. ex: "fastFoodRestaurants"
    - merchant_country_code [string]: merchant country code. ex: "USA"
    - acquirer_id [string]: acquirer ID. ex: "5656565656565656"
    - merchant_id [string]: merchant ID. ex: "5656565656565656"
    - merchant_name [string]: merchant name. ex: "Google Cloud Platform"
    - merchant_fee [integer]: fee charged by the merchant to cover specific costs, such as ATM withdrawal logistics, etc. ex: 200 (= R$ 2.00)
    - wallet_id [string]: virtual wallet ID. ex: "5656565656565656"
    - method_code [string]: method code. Options: "chip", "token", "server", "manual", "magstripe" or "contactless"
    - score [float]: internal score calculated for the authenticity of the purchase. None in case of insufficient data. ex: 7.6
    - end_to_end_id [string]: Unique id used to identify the transaction through all of its life cycle, even before the purchase is denied or approved and gets its usual id. ex: "679cd385-642b-49d0-96b7-89491e1249a5"
    - tags [string]: list of strings for tagging returned by the sub-issuer during the authorization. ex: ["travel", "food"]
    - zip_code [string]: zip code of the merchant location. ex: "02101234"
    ## Attributes (IssuingPurchase only):
    - issuing_transaction_ids [string]: ledger transaction ids linked to this Purchase
    - status [string]: current IssuingCard status. Options: "approved", "canceled", "denied", "confirmed", "voided"
    - updated [datetime.datetime]: latest update datetime for the IssuingPurchase. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - created [datetime.datetime]: creation datetime for the IssuingPurchase. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    ## Attributes (authorization request only):
    - is_partial_allowed [bool]: true if the merchant allows partial purchases. ex: False
    - card_tags [list of strings]: tags of the IssuingCard responsible for this purchase. ex: ["travel", "food"]
    - holder_tags [list of strings]: tags of the IssuingHolder responsible for this purchase. ex: ["technology", "john snow"]
    """

    def __init__(self, id=None, holder_name=None, card_id=None, card_ending=None, purpose=None, amount=None, tax=None, 
                issuer_amount=None, issuer_currency_code=None, issuer_currency_symbol=None, merchant_amount=None, 
                merchant_currency_code=None, merchant_currency_symbol=None, merchant_category_code=None, merchant_country_code=None, 
                acquirer_id=None, merchant_id=None, merchant_name=None, merchant_fee=None, wallet_id=None, method_code=None, 
                score=None, end_to_end_id=None, tags=None, zip_code=None, issuing_transaction_ids=None, status=None, updated=None, 
                created=None, is_partial_allowed=None, card_tags=None, holder_tags=None):
        Resource.__init__(self, id=id)

        self.holder_name = holder_name
        self.card_id = card_id
        self.card_ending = card_ending
        self.purpose = purpose
        self.amount = amount
        self.tax = tax
        self.issuer_amount = issuer_amount
        self.issuer_currency_code = issuer_currency_code
        self.issuer_currency_symbol = issuer_currency_symbol
        self.merchant_amount = merchant_amount
        self.merchant_currency_code = merchant_currency_code
        self.merchant_currency_symbol = merchant_currency_symbol
        self.merchant_category_code = merchant_category_code
        self.merchant_country_code = merchant_country_code
        self.acquirer_id = acquirer_id
        self.merchant_id = merchant_id
        self.merchant_name = merchant_name
        self.merchant_fee = merchant_fee
        self.wallet_id = wallet_id
        self.method_code = method_code
        self.score = score
        self.end_to_end_id = end_to_end_id
        self.tags = tags
        self.zip_code = zip_code
        self.issuing_transaction_ids = issuing_transaction_ids
        self.status = status
        self.updated = check_datetime(updated)
        self.created = check_datetime(created)
        self.is_partial_allowed = is_partial_allowed
        self.card_tags = card_tags
        self.holder_tags = holder_tags


_resource = {"class": IssuingPurchase, "name": "IssuingPurchase"}


def get(id, user=None):
    """# Retrieve a specific IssuingPurchase
    Receive a single IssuingPurchase object previously created in the Stark Infra API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - IssuingPurchase object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def query(ids=None, limit=None, after=None, before=None, end_to_end_ids=None, holder_ids=None, card_ids=None,
          status=None, user=None):
    """# Retrieve IssuingPurchase
    Receive a generator of IssuingPurchase objects previously created in the Stark Infra API
    ## Parameters (optional):
    - ids [list of strings, default [], default None]: purchase IDs
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - end_to_end_ids [list of strings, default []]: central bank's unique transaction ID. ex: "E79457883202101262140HHX553UPqeq"
    - holder_ids [list of strings, default []]: card holder IDs. ex: ["5656565656565656", "4545454545454545"]
    - card_ids [list of strings, default []]: card  IDs. ex: ["5656565656565656", "4545454545454545"]
    - status [list of strings, default None]: filter for status of retrieved objects. ex: ["approved", "canceled", "denied", "confirmed", "voided"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - generator of IssuingPurchase objects with updated attributes
    """
    return rest.get_stream(
        resource=_resource,
        ids=ids,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        end_to_end_ids=end_to_end_ids,
        holder_ids=holder_ids,
        card_ids=card_ids,
        status=status,
        user=user,
    )


def page(end_to_end_ids=None, holder_ids=None, card_ids=None, status=None, after=None, before=None, ids=None,
        cursor=None, limit=None, user=None):
    """# Retrieve paged IssuingPurchase
    Receive a list of IssuingPurchase objects previously created in the Stark Infra API and the cursor to the next page.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - ids [list of strings, default [], default None]: purchase IDs
    - limit [integer, default 100]: maximum number of objects to be retrieved. Max = 100. ex: 35
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - end_to_end_ids [list of strings, default []]: central bank's unique transaction ID. ex: "E79457883202101262140HHX553UPqeq"
    - holder_ids [list of strings, default []]: card holder IDs. ex: ["5656565656565656", "4545454545454545"]
    - card_ids [list of strings, default []]: card  IDs. ex: ["5656565656565656", "4545454545454545"]
    - status [list of strings, default None]: filter for status of retrieved objects. ex: ["approved", "canceled", "denied", "confirmed", "voided"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - list of IssuingPurchase objects with updated attributes
    - cursor to retrieve the next page of IssuingPurchase objects
    """
    return rest.get_page(
        resource=_resource,
        cursor=cursor,
        ids=ids,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        end_to_end_ids=end_to_end_ids,
        holder_ids=holder_ids,
        card_ids=card_ids,
        status=status,
        user=user,
    )


def parse(content, signature, user=None):
    """# Create a single verified IssuingPurchase authorization request from a content string
    Use this method to parse and verify the authenticity of the authorization request received at the informed endpoint.
    Authorization requests are posted to your registered endpoint whenever IssuingPurchases are received.
    They present IssuingPurchase data that must be analyzed and answered with approval or declination.
    If the provided digital signature does not check out with the StarkInfra public key, a stark.exception.InvalidSignatureException will be raised.
    If the authorization request is not answered within 2 seconds or is not answered with an HTTP status code 200 the IssuingPurchase will go through the pre-configured stand-in validation.
    ## Parameters (required):
    - content [string]: response content from request received at user endpoint (not parsed)
    - signature [string]: base-64 digital signature received at response header "Digital-Signature"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - Parsed IssuingPurchase object
    """
    return parse_and_verify(
        content=content,
        signature=signature,
        user=user,
        resource=_resource,
        key="",
    )


def response(status, amount=None, reason=None, tags=None):
    """# Helps you respond IssuingPurchase requests
    ## Parameters (required):
    - status [string]: sub-issuer response to the authorization. ex: "approved" or "denied"
    ## Parameters (conditionally required):
    - reason [string]: denial reason. Options: "other", "blocked", "lostCard", "stolenCard", "invalidPin", "invalidCard", "cardExpired", "issuerError", "concurrency", "standInDenial", "subIssuerError", "invalidPurpose", "invalidZipCode", "invalidWalletId", "inconsistentCard", "settlementFailed", "cardRuleMismatch", "invalidExpiration", "prepaidInstallment", "holderRuleMismatch", "insufficientBalance", "tooManyTransactions", "invalidSecurityCode", "invalidPaymentMethod", "confirmationDeadline", "withdrawalAmountLimit", "insufficientCardLimit", "insufficientHolderLimit"
    ## Parameters (optional):
    - amount [integer, default None]: amount in cents that was authorized. ex: 1234 (= R$ 12.34)
    - tags [list of strings, default []]: tags to filter retrieved object. ex: ["tony", "stark"]
    ## Return:
    - Dumped JSON string that must be returned to us on the IssuingPurchase request
    """
    params = {"authorization": {
        "status": status,
        "amount": amount,
        "reason": reason,
        "tags": tags,
    }}
    return dumps(api_json(params))
