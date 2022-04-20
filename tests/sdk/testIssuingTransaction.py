import starkinfra
from unittest import TestCase, main
from tests.utils.user import exampleProject


starkinfra.user = exampleProject


class TestIssuingTransactionQuery(TestCase):

    def test_success(self):
        transactions = starkinfra.issuingtransaction.query(limit=10)
        for transaction in transactions:
            self.assertIsInstance(transaction.amount, int)


class TestIssuingTransactionPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            transactions, cursor = starkinfra.issuingtransaction.page(limit=2, cursor=cursor)
            for transaction in transactions:
                self.assertFalse(transaction.id in ids)
                ids.append(transaction.id)
            if cursor is None:
                break
        self.assertTrue(len(ids) == 4)


class TestIssuingTransactionGet(TestCase):

    def test_success(self):
        transactions = starkinfra.issuingtransaction.query(limit=1)
        transaction = starkinfra.issuingtransaction.get(id=next(transactions).id)
        self.assertIsInstance(transaction.amount, int)


if __name__ == '__main__':
    main()
