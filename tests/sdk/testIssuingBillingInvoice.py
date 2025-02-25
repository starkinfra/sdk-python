import starkinfra
from unittest import TestCase, main
from datetime import date, timedelta
from tests.utils.user import exampleProject

starkinfra.user = exampleProject


class TestIssuingBillingInvoiceGet(TestCase):

    def test_success(self):
        billing_invoices = starkinfra.issuinginvoice.query(limit=1)
        billing_invoice = starkinfra.issuinginvoice.get(id=next(billing_invoices).id)
        self.assertEqual(billing_invoice.id, str(billing_invoice.id))


class TestIssuingBillingInvoiceQuery(TestCase):

    def test_success(self):
        billing_invoices = starkinfra.issuingbillinginvoice.query(
            after=date.today() - timedelta(days=100),
            before=date.today()
        )
        for billing_invoice in billing_invoices:
            self.assertEqual(billing_invoice.id, str(billing_invoice.id))


class TestIssuingBillingInvoicePage(TestCase):

    def test_success(self):
        billing_invoices = starkinfra.issuingbillinginvoice.page(
            after=date.today() - timedelta(days=100),
            before=date.today(),
            limit = 10,
            cursor = None
        )
        for billing_invoice in billing_invoices:
            self.assertEqual(billing_invoice.id, str(billing_invoice.id))


if __name__ == '__main__':
    main()
