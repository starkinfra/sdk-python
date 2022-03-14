import starkinfra
from unittest import TestCase, main
from tests.utils.user import exampleProject


starkinfra.user = exampleProject


class TestPixRequestLogQuery(TestCase):

    def test_success(self):
        logs = list(starkinfra.pixrequest.log.query(limit=10))
        logs = list(starkinfra.pixrequest.log.query(limit=10, request_ids={log.request.id for log in logs}, types={log.type for log in logs}))
        self.assertEqual(10, len(logs))
        print("Number of logs:", len(logs))


class TestPixRequestLogPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            logs, cursor = starkinfra.pixrequest.log.page(limit=2, cursor=cursor)
            for log in logs:
                print(log)
                self.assertFalse(log.id in ids)
                ids.append(log.id)
            if cursor is None:
                break
        self.assertTrue(len(ids) == 4)


class TestPixRequestLogInfoGet(TestCase):
    def test_success(self):
        logs = starkinfra.pixrequest.log.query()
        log_id = next(logs).id
        logs = starkinfra.pixrequest.log.get(id=log_id)


if __name__ == '__main__':
    main()
