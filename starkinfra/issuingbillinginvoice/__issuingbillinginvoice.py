from ..utils import rest
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime, check_date


class IssuingBillingInvoice(Resource):
    """# IssuingBillingInvoice object
    Check out our API Documentation at https://starkinfra.com/docs/api#issuing-billing-invoice
    """

    def __init__(self, id=None, name=None, tax_id=None, fine=None, interest=None, status=None, amount=None,
                 nominal_amount=None, brcode=None, link=None, due=None, start=None, end=None, created=None,
                 updated=None):
        Resource.__init__(self, id=id)

        self.tax_id = tax_id
        self.name = name
        self.fine = fine
        self.interest = interest
        self.status = status
        self.amount = amount
        self.nominal_amount = nominal_amount
        self.brcode = brcode
        self.link = link
        self.due = check_datetime(due)
        self.start = check_datetime(start)
        self.end = check_datetime(end)
        self.created = check_datetime(created)
        self.updated = check_datetime(updated)


_resource = {"class": IssuingBillingInvoice, "name": "IssuingBillingInvoice"}


def get(id, user=None):
    """# IssuingBillingInvoice object
    Check out our API Documentation at https://starkinfra.com/docs/api#issuing-billing-invoice
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def query(limit=None, after=None, before=None, status=None, id=None, tags=None, user=None):
    """# IssuingBillingInvoice object
    Check out our API Documentation at https://starkinfra.com/docs/api#issuing-billing-invoice
    """
    return rest.get_stream(
        resource=_resource,
        status=status,
        after=check_datetime(after),
        before=check_datetime(before),
        id=id,
        tags=tags,
        limit=limit,
        user=user,
    )


def page(cursor=None, limit=None, after=None, before=None, status=None, tags=None, user=None):
    """# IssuingBillingInvoice object
    Check out our API Documentation at https://starkinfra.com/docs/api#issuing-billing-invoice
    """
    return rest.get_page(
        resource=_resource,
        cursor=cursor,
        status=status,
        after=check_datetime(after),
        before=check_datetime(before),
        tags=tags,
        limit=limit,
        user=user,
    )
