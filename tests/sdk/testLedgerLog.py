import starkinfra
from unittest import TestCase, main
from tests.utils.user import exampleProject


starkinfra.user = exampleProject


class TestLedgerLogQuery(TestCase):

    def test_success(self):
        logs = list(starkinfra.ledger.log.query(limit=10))
        logs = list(starkinfra.ledger.log.query(            
            limit=10,
        ))
        self.assertEqual(10, len(logs))


class TestLedgerLogPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            logs, cursor = starkinfra.ledger.log.page(limit=2, cursor=cursor)
            for log in logs:
                self.assertFalse(log.id in ids)
                ids.append(log.id)
            if cursor is None:
                break
        self.assertTrue(len(ids) == 4)


class TestLedgerLogInfoGet(TestCase):

    def test_success(self):
        logs = starkinfra.ledger.log.query()
        log_id = next(logs).id
        log = starkinfra.ledger.log.get(id=log_id)
        self.assertEqual(log_id, log.id)

    def test_success_ids(self):
        logs = starkinfra.ledger.log.query(limit=5)
        log_ids_expected = [log.id for log in logs]
        log_ids_result = [log.id for log in starkinfra.ledger.log.query(ids=log_ids_expected)]
        log_ids_expected.sort()
        log_ids_result.sort()
        self.assertListEqual(log_ids_expected, log_ids_result)


if __name__ == '__main__':
    main()
