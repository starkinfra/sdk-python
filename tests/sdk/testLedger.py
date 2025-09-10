import starkinfra
from starkinfra.ledger import Rule
from unittest import TestCase, main
from datetime import date, timedelta
from tests.utils.user import exampleProject
from tests.utils.ledger import generateExampleLedgerJson


starkinfra.user = exampleProject


class TestLedgerPost(TestCase):

    def test_success(self):
        ledgers = generateExampleLedgerJson(n=3)
        ledgers = starkinfra.ledger.create(ledgers=ledgers)
        for ledger in ledgers:
            check_ledger = starkinfra.ledger.get(ledger.id)
            self.assertEqual(ledger.id, check_ledger.id)


class TestLedgerQuery(TestCase):

    def test_success(self):
        ledgers = list(starkinfra.ledger.query(limit=10))
        self.assertEqual(len(ledgers), 10)

    def test_success_with_params(self):
        ledgers = starkinfra.ledger.query(
            limit=10,
            after=date.today() - timedelta(days=100),
            before=date.today(),
            tags=["iron", "bank"],
            ids=["1", "2", "3"],
            external_ids=["1", "2", "3"],
        )
        self.assertEqual(len(list(ledgers)), 0)


class TestLedgerPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            ledgers, cursor = starkinfra.ledger.page(limit=2, cursor=cursor)
            for ledger in ledgers:
                self.assertFalse(ledger.id in ids)
                ids.append(ledger.id)
            if cursor is None:
                break
        self.assertTrue(len(ids) == 4)


class TestLedgerInfoGet(TestCase):

    def test_success(self):
        ledgers = starkinfra.ledger.query()
        ledger_id = next(ledgers).id
        ledger = starkinfra.ledger.get(id=ledger_id)
        self.assertEqual(ledger.id, ledger_id)
    
    def test_success_ids(self):
        ledgers = starkinfra.ledger.query(limit=5)
        ledger_ids_expected = [ledger.id for ledger in ledgers]
        ledger_ids_result = [ledger.id for ledger in starkinfra.ledger.query(ids=ledger_ids_expected)]
        ledger_ids_expected.sort()
        ledger_ids_result.sort()
        self.assertListEqual(ledger_ids_expected, ledger_ids_result)


class TestLedgerInfoPatch(TestCase):

    def test_success_update_rules(self):
        ledger = next(starkinfra.ledger.query(limit=1))
        self.assertIsNotNone(ledger.id)
        updated_ledger = starkinfra.ledger.update(
            id=ledger.id,
            rules=[
                Rule(
                    key="minimumBalance",
                    value=0,
                ),
            ],
        )
        self.assertIsNotNone(updated_ledger.id)


if __name__ == '__main__':
    main()
