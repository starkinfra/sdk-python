import starkinfra
from unittest import TestCase, main
from tests.utils.user import exampleProject


starkinfra.user = exampleProject


class TestPixFraudLogQuery(TestCase):

    def test_success(self):
        logs = list(starkinfra.pixfraud.log.query(limit=10))
        logs = list(starkinfra.pixfraud.log.query(
            limit=10,
            fraud_ids={log.fraud.id for log in logs},
            types={log.type for log in logs}
        ))
        self.assertEqual(10, len(logs))

    def test_success_with_params(self):
        frauds = starkinfra.pixfraud.log.query(
            limit=2,
        )
        self.assertEqual(len(list(frauds)), 2)


class TestPixFraudLogPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            logs, cursor = starkinfra.pixfraud.log.page(limit=2, cursor=cursor)
            for log in logs:
                self.assertFalse(log.id in ids)
                ids.append(log.id)
            if cursor is None:
                break
        self.assertTrue(len(ids) == 4)

    def test_success_with_params(self):
        frauds = starkinfra.pixfraud.log.page(
            limit=2,
        )
        self.assertEqual(len(list(frauds)), 2)


class TestPixFraudLogInfoGet(TestCase):
    def test_success(self):
        logs = starkinfra.pixfraud.log.query(limit=10)
        log_id = next(logs).id
        log = starkinfra.pixfraud.log.get(id=log_id)
        self.assertEqual(log_id, log.id)


if __name__ == '__main__':
    main()
