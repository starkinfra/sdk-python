import starkinfra
from unittest import TestCase, main
from tests.utils.user import exampleProject


starkinfra.user = exampleProject


class TestPixPullRequestLogQuery(TestCase):

    def test_success(self):
        logs = list(starkinfra.pixpullrequest.log.query(limit=10))
        self.assertLessEqual(len(logs), 10)


class TestPixPullRequestLogPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            logs, cursor = starkinfra.pixpullrequest.log.page(limit=2, cursor=cursor)
            for log in logs:
                self.assertFalse(log.id in ids)
                ids.append(log.id)
            if cursor is None:
                break
        self.assertTrue(len(ids) <= 4)


class TestPixPullRequestLogInfoGet(TestCase):

    def test_success(self):
        logs = starkinfra.pixpullrequest.log.query(limit=1)
        log = next(logs, None)
        if log is None:
            self.skipTest("no logs available to fetch")
        result = starkinfra.pixpullrequest.log.get(id=log.id)
        self.assertIsNotNone(result.id)
        self.assertEqual(log.id, result.id)


class TestPixPullRequestLogFilter(TestCase):

    def test_query_by_request_ids(self):
        requests = list(starkinfra.pixpullrequest.query(limit=1))
        if not requests:
            self.skipTest("no pull requests available to filter logs by")
        target_id = requests[0].id
        logs = list(starkinfra.pixpullrequest.log.query(
            limit=5,
            request_ids=[target_id],
        ))
        for log in logs:
            self.assertEqual(log.request.id, target_id)


if __name__ == '__main__':
    main()
