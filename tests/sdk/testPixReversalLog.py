import starkinfra
from unittest import TestCase, main
from tests.utils.user import exampleProject


starkinfra.user = exampleProject


class TestPixReversalLogQuery(TestCase):

    def test_success(self):
        logs = list(starkinfra.pixreversal.log.query(limit=10))
        logs = list(starkinfra.pixreversal.log.query(
            limit=10,
            reversal_ids={log.reversal.id for log in logs},
            types={log.type for log in logs}
        ))
        self.assertEqual(10, len(logs))
        print("Number of logs:", len(logs))


class TestPixReversalLogPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            logs, cursor = starkinfra.pixreversal.log.page(limit=2, cursor=cursor)
            for log in logs:
                print(log)
                self.assertFalse(log.id in ids)
                ids.append(log.id)
            if cursor is None:
                break
        self.assertTrue(len(ids) == 4)


class TestPixReversalLogInfoGet(TestCase):
    def test_success(self):
        logs = starkinfra.pixreversal.log.query()
        log_id = next(logs).id
        log = starkinfra.pixreversal.log.get(id=log_id)
        self.assertEqual(log_id, log.id)


if __name__ == '__main__':
    main()
