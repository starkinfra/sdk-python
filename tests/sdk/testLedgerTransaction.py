import starkinfra
from random import choices
from unittest import TestCase, main
from datetime import date, timedelta
from tests.utils.user import exampleProject
from tests.utils.ledgerTransaction import generateExampleLedgerTransactionJson, getLedgerWithTransactions


starkinfra.user = exampleProject


class TestLedgerTransactionPost(TestCase):
    
    def test_success(self):
        transactions = generateExampleLedgerTransactionJson(n=25)
        ledgers = choices(list(starkinfra.ledger.query(limit=3)), k=len(transactions))
        for transaction, ledger in zip(transactions, ledgers):
            transaction.ledger_id = ledger.id
        transactions = starkinfra.ledgertransaction.create(transactions=transactions)
        for transaction in transactions:
            check_transaction = starkinfra.ledgertransaction.get(transaction.id)
            self.assertEqual(transaction.id, check_transaction.id)


class TestLedgerTransactionQuery(TestCase):

    def test_success(self):
        ledger = getLedgerWithTransactions()
        transactions = list(starkinfra.ledgertransaction.query(
            ledger_id=ledger.id,
            limit=5,
        ))
        self.assertEqual(len(transactions), 5)

    def test_success_with_params(self):
        transactions = starkinfra.ledgertransaction.query(
            limit=10,
            after=date.today() - timedelta(days=100),
            before=date.today(),
            tags=["iron", "bank"],
            ids=["1", "2", "3"],
            external_ids=["1", "2", "3"],
        )
        self.assertEqual(len(list(transactions)), 0)


class TestLedgerTransactionPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        ledger = getLedgerWithTransactions()
        for _ in range(2):
            transactions, cursor = starkinfra.ledgertransaction.page(ledger_id=ledger.id, limit=2, cursor=cursor)
            for transaction in transactions:
                self.assertFalse(transaction.id in ids)
                ids.append(transaction.id)
            if cursor is None:
                break
        self.assertEqual(len(ids), 4)


class TestLedgerTransactionInfoGet(TestCase):

    def test_success(self):
        ledger = getLedgerWithTransactions()
        transactions = starkinfra.ledgertransaction.query(ledger_id=ledger.id)
        transaction_id = next(transactions).id
        transaction = starkinfra.ledgertransaction.get(id=transaction_id)
        self.assertEqual(transaction_id, transaction.id)
        self.assertEqual(ledger.id, transaction.ledger_id)
    
    def test_success_ids(self):
        ledger = getLedgerWithTransactions()
        transactions = starkinfra.ledgertransaction.query(ledger_id=ledger.id)
        transaction_ids_expected = [transaction.id for transaction in transactions]
        transaction_ids_result = [transaction.id for transaction in starkinfra.ledgertransaction.query(ids=transaction_ids_expected)]
        transaction_ids_expected.sort()
        transaction_ids_result.sort()
        self.assertListEqual(transaction_ids_expected, transaction_ids_result)


if __name__ == "__main__":
    main()
