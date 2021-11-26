from starkbank.utils.resource import Resource
from starkbank.utils.checks import check_datetime
from starkbank.utils import rest


class IssuingPurchase(Resource):

    def __init__(self, id, holder_name, card_id, card_ending, amount, tax, issuer_amount, issuer_currency_code,
                 issuer_currency_symbol, merchant_amount, merchant_currency_code, merchant_currency_symbol,
                 merchant_category_code, merchant_country_code, acquirer_id, merchant_id, merchant_name, wallet_id,
                 method_code, score, issuing_transaction_ids, end_to_end_id, status, tags, created, updated):
        super().__init__(id)
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
    """# Retrieve a specific Invoice
    Receive a single Invoice object previously created in the Stark Bank API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkbank.user was set before function call
    ## Return:
    - Invoice object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def query(end_to_end_ids=None, holder_ids=None, card_ids=None, status=None, after=None, before=None, ids=None,
          limit=None, expand=None, user=None):
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
        expand=expand,
        user=user,
    )


def page(end_to_end_ids=None, holder_ids=None, card_ids=None, status=None, after=None, before=None, ids=None,
         cursor=None, limit=None, expand=None, user=None):
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
        expand=expand,
        user=user,
    )
