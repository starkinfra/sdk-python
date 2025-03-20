from ..utils import rest
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime, check_date


class IssuingBillingTransaction(Resource):
    """# IssuingBillingTransaction object
    Check out our API Documentation at https://starkinfra.com/docs/api#issuing-billing-transaction
    """

    def __init__(self, id=None, amount=None, invoice_id=None, installment=None, installment_count=None,
                 balance=None, holder_name=None, source=None, external_id=None, description=None, card_ending=None,
                 tax=None, rate=None, merchant_amount=None, merchant_currency_code=None, created=None):
        Resource.__init__(self, id=id)

        self.amount = amount
        self.invoice_id = invoice_id
        self.installment = installment
        self.installment_count = installment_count
        self.balance = balance
        self.holder_name = holder_name
        self.source = source
        self.external_id = external_id
        self.description = description
        self.card_ending = card_ending
        self.tax = tax
        self.rate = rate
        self.merchant_amount = merchant_amount
        self.merchant_currency_code = merchant_currency_code
        self.created = check_datetime(created)


_resource = {"class": IssuingBillingTransaction, "name": "IssuingBillingTransaction"}


def query(limit=None, after=None, before=None, invoice_id=None, tags=None, user=None):
    """# IssuingBillingTransaction object
    Check out our API Documentation at https://starkinfra.com/docs/api#issuing-billing-transaction
    """
    return rest.get_stream(
        resource=_resource,
        after=check_datetime(after),
        before=check_datetime(before),
        invoice_id=invoice_id,
        tags=tags,
        limit=limit,
        user=user,
    )

def page(cursor=None, limit=None, after=None, before=None, invoice_id=None, tags=None, user=None):
    """# IssuingBillingTransaction object
    Check out our API Documentation at https://starkinfra.com/docs/api#issuing-billing-transaction
    """
    return rest.get_page(
        resource=_resource,
        cursor=cursor,
        after=check_datetime(after),
        before=check_datetime(before),
        tags=tags,
        invoice_id=invoice_id,
        limit=limit,
        user=user,
    )
