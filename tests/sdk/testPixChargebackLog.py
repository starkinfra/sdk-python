import starkinfra
from unittest import TestCase, main
from datetime import timedelta, date
from tests.utils.user import exampleProject


starkinfra.user = exampleProject


class TestPixChargebackLogQuery(TestCase):

    def test_success(self):
        logs = list(starkinfra.pixchargeback.log.query(limit=2))
        logs = list(starkinfra.pixchargeback.log.query(
            limit=2,
            chargeback_ids={log.chargeback.id for log in logs},
            types={log.type for log in logs}
        ))
        self.assertEqual(2, len(logs))
        print("Number of logs:", len(logs))

    def test_success_with_params(self):
        reversal_requests = starkinfra.pixchargeback.log.query(
            limit=10,
            after=date.today() - timedelta(days=100),
            before=date.today(),
            types="failed",
            chargeback_ids=["1"],
            ids=["1", "2", "3"],

        )
        self.assertEqual(len(list(reversal_requests)), 0)


class TestPixChargebackLogPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            logs, cursor = starkinfra.pixchargeback.log.page(limit=2, cursor=cursor)
            for log in logs:
                print(log)
                self.assertFalse(log.id in ids)
                ids.append(log.id)
            if cursor is None:
                break
        self.assertTrue(len(ids) == 4)

    def test_success_with_params(self):
        reversal_requests = starkinfra.pixchargeback.log.page(
            limit=2,
        )
        self.assertEqual(len(list(reversal_requests)), 2)


class TestPixChargebackLogInfoGet(TestCase):
    def test_success(self):
        logs = starkinfra.pixchargeback.log.query()
        log_id = next(logs).id
        log = starkinfra.pixchargeback.log.get(id=log_id)
        self.assertEqual(log_id, log.id)


if __name__ == '__main__':
    main()
