import starkinfra
import starkbank
from unittest import TestCase, main
from tests.utils.user import exampleProject
from tests.utils.issuingInvoice import generateExampleInvoicesJson

starkbank.user = exampleProject


class TestIssuingInvoiceQuery(TestCase):

    def test_success(self):
        invoices = starkinfra.issuinginvoice.query(user=exampleProject)
        for invoice in invoices:
            self.assertIsInstance(invoice.id, str)


class TestIssuingInvoiceGet(TestCase):

    def test_success(self):
        invoices = starkinfra.issuinginvoice.query(user=exampleProject, limit=1)
        invoice = starkinfra.issuinginvoice.get(user=exampleProject, id=next(invoices).id)
        self.assertIsInstance(invoice.id, str)


class TestIssuingInvoicePost(TestCase):

    def test_success(self):
        example_invoice = generateExampleInvoicesJson()
        invoice = starkinfra.issuinginvoice.create(amount=example_invoice.amount)
        self.assertIsInstance(invoice.id, str)


if __name__ == '__main__':
    main()
