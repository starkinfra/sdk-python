import starkinfra
from unittest import TestCase, main
from datetime import timedelta, date
from tests.utils.user import exampleProject


starkinfra.user = exampleProject


class TestPixKeyLogQuery(TestCase):

    def test_success(self):
        logs = list(starkinfra.pixkey.log.query(limit=10))
        logs = list(starkinfra.pixkey.log.query(
            limit=10,
            key_ids={log.key.id for log in logs},
            types={log.type for log in logs}
        ))
        self.assertEqual(10, len(logs))
        print("Number of logs:", len(logs))

    def test_success_with_params(self):
        pix_keys = starkinfra.pixkey.log.query(
            limit=10,
            after=date.today() - timedelta(days=100),
            before=date.today(),
            types="failed",
            key_ids=["1"],
            ids=["1", "2", "3"],

        )
        self.assertEqual(len(list(pix_keys)), 0)


class TestPixKeyLogPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            logs, cursor = starkinfra.pixkey.log.page(limit=2, cursor=cursor)
            for log in logs:
                print(log)
                self.assertFalse(log.id in ids)
                ids.append(log.id)
            if cursor is None:
                break
        self.assertTrue(len(ids) == 4)


class TestPixKeyLogInfoGet(TestCase):
    def test_success(self):
        logs = starkinfra.pixkey.log.query()
        log_id = next(logs).id
        log = starkinfra.pixkey.log.get(id=log_id)
        self.assertEqual(log_id, log.id)


if __name__ == '__main__':
    main()
