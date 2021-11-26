import starkinfra
from unittest import TestCase, main
from tests.utils.user import exampleProject
from tests.utils.issuingInvoice import generateExampleInvoicesJson

starkinfra.user = exampleProject


class TestIssuingInvoiceQuery(TestCase):

    def test_success(self):
        invoices = starkinfra.issuinginvoice.query()
        for invoice in invoices:
            self.assertIsInstance(invoice.id, str)


class TestIssuingInvoiceGet(TestCase):

    def test_success(self):
        invoices = starkinfra.issuinginvoice.query(limit=1)
        invoice = starkinfra.issuinginvoice.get(id=next(invoices).id)
        self.assertIsInstance(invoice.id, str)


class TestIssuingInvoicePost(TestCase):

    def test_success(self):
        example_invoice = generateExampleInvoicesJson()
        invoice = starkinfra.issuinginvoice.create(amount=example_invoice.amount)
        self.assertIsInstance(invoice.id, str)


if __name__ == '__main__':
    main()
