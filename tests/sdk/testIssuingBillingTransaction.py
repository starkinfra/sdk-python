import starkinfra
from unittest import TestCase, main
from datetime import date, timedelta
from tests.utils.user import exampleProject


starkinfra.user = exampleProject


class TestIssuingBillingTransactionQuery(TestCase):

    def test_success(self):
        billing_transactions = starkinfra.issuingbillingtransaction.query(
            after=date.today() - timedelta(days=100),
            before=date.today()
        )
        for billing_transaction in billing_transactions:
            self.assertEqual(billing_transaction.id, str(billing_transaction.id))

class TestIssuingBillingTransactionPage(TestCase):

    def test_success(self):
        billing_transactions = starkinfra.issuingbillingtransaction.page(
            after=date.today() - timedelta(days=100),
            before=date.today(),
            limit = 10,
            cursor = None
        )
        for billing_transaction in billing_transactions:
            self.assertEqual(billing_transaction.id, str(billing_transaction.id))

if __name__ == '__main__':
    main()
