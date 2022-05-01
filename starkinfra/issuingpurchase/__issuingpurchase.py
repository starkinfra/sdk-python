from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime
from ..utils import rest


class IssuingPurchase(Resource):
    """# IssuingPurchase object
    Displays the IssuingPurchase objects created in your Workspace.
    ## Attributes (return-only):
    - id [string]: unique id returned when IssuingPurchase is created. ex: "5656565656565656"
    - holder_name [string]: card holder name. ex: "Tony Stark"
    - card_id [string]: unique id returned when IssuingCard is created. ex: "5656565656565656"
    - card_ending [string]: last 4 digits of the card number. ex: "1234"
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
    - wallet_id [string]: virtual wallet ID. ex: "5656565656565656"
    - method_code [string]: method code. ex: "chip", "token", "server", "manual", "magstripe" or "contactless"
    - score [float]: internal score calculated for the authenticity of the purchase. None in case of insufficient data. ex: 7.6
    - issuing_transaction_ids [string]: ledger transaction ids linked to this Purchase
    - end_to_end_id [string]: central bank's unique transaction ID. ex: "E79457883202101262140HHX553UPqeq"
    - status [string]: current IssuingCard status. ex: "approved", "canceled", "denied", "confirmed" or "voided"
    - tags [string]: list of strings for tagging returned by the sub-issuer during the authorization. ex: ["travel", "food"]
    - updated [datetime.datetime]: latest update datetime for the IssuingPurchase. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - created [datetime.datetime]: creation datetime for the IssuingPurchase. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, id, holder_name, card_id, card_ending, amount, tax, issuer_amount, issuer_currency_code,
                 issuer_currency_symbol, merchant_amount, merchant_currency_code, merchant_currency_symbol,
                 merchant_category_code, merchant_country_code, acquirer_id, merchant_id, merchant_name, wallet_id,
                 method_code, score, issuing_transaction_ids, end_to_end_id, status, tags, created, updated):
        Resource.__init__(self, id=id)
        self.holder_name = holder_name
        self.card_id = card_id
        self.card_ending = card_ending
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
        self.wallet_id = wallet_id
        self.method_code = method_code
        self.score = score
        self.issuing_transaction_ids = issuing_transaction_ids
        self.end_to_end_id = end_to_end_id
        self.status = status
        self.tags = tags
        self.updated = check_datetime(updated)
        self.created = check_datetime(created)


_resource = {"class": IssuingPurchase, "name": "IssuingPurchase"}


def get(id, user=None):
    """# Retrieve a specific IssuingPurchase
    Receive a single IssuingPurchase object previously created in the Stark Bank API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - IssuingPurchase object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def query(end_to_end_ids=None, holder_ids=None, card_ids=None, status=None, after=None, before=None, ids=None,
          limit=None, user=None):
    """# Retrieve IssuingPurchase
    Receive a generator of IssuingPurchases objects previously created in the Stark Infra API
    ## Parameters (optional):
    - end_to_end_ids [list of strings, default []]: central bank's unique transaction ID. ex: "E79457883202101262140HHX553UPqeq"
    - holder_ids [list of strings, default []]: card holder IDs. ex: ["5656565656565656", "4545454545454545"]
    - card_ids [list of strings, default []]: card  IDs. ex: ["5656565656565656", "4545454545454545"]
    - status [string, default None]: filter for status of retrieved objects. ex: "approved", "canceled", "denied", "confirmed" or "voided"
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - ids [list of strings, default [], default None]: purchase IDs
    - limit [integer, default 100]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - generator of IssuingPurchase objects with updated attributes
    """
    return rest.get_stream(
        resource=_resource,
        end_to_end_ids=end_to_end_ids,
        holder_ids=holder_ids,
        card_ids=card_ids,
        status=status,
        after=check_datetime(after),
        before=check_datetime(before),
        ids=ids,
        limit=limit,
        user=user,
    )


def page(end_to_end_ids=None, holder_ids=None, card_ids=None, status=None, after=None, before=None, ids=None,
         cursor=None, limit=None, user=None):
    """# Retrieve paged IssuingPurchase
    Receive a list of IssuingPurchase objects previously created in the Stark Infra API and the cursor to the next page.
    ## Parameters (optional):
    - end_to_end_ids [list of strings, default []]: central bank's unique transaction ID. ex: "E79457883202101262140HHX553UPqeq"
    - holder_ids [list of strings, default []]: card holder IDs. ex: ["5656565656565656", "4545454545454545"]
    - card_ids [list of strings, default []]: card  IDs. ex: ["5656565656565656", "4545454545454545"]
    - status [string, default None]: filter for status of retrieved objects. ex: "approved", "canceled", "denied", "confirmed" or "voided"
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - ids [list of strings, default [], default None]: purchase IDs
    - limit [integer, default 100]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - cursor [string, default None]: cursor returned on the previous page function call
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - list of IssuingPurchase objects with updated attributes
    - cursor to retrieve the next page of IssuingPurchase objects
    """
    return rest.get_page(
        resource=_resource,
        end_to_end_ids=end_to_end_ids,
        holder_ids=holder_ids,
        card_ids=card_ids,
        status=status,
        after=check_datetime(after),
        before=check_datetime(before),
        ids=ids,
        cursor=cursor,
        limit=limit,
        user=user,
    )
