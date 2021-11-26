import starkinfra
import starkbank
from unittest import TestCase, main
from tests.utils.user import exampleProject


starkbank.user = exampleProject


class TestIssuingTransactionQuery(TestCase):

    def test_success(self):
        transactions = starkinfra.issuingtransaction.query(user=exampleProject)
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
        transactions = starkinfra.issuingtransaction.query(user=exampleProject, limit=1)
        transaction = starkinfra.issuingtransaction.get(user=exampleProject, id=next(transactions).id)
        print(transaction)
        self.assertIsInstance(transaction.amount, int)


if __name__ == '__main__':
    main()
