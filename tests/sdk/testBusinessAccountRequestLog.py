import starkinfra
from datetime import datetime, date, timedelta
from unittest import TestCase, main
from tests.utils.user import exampleProject
from starkinfra import BusinessAccountRequest


starkinfra.user = exampleProject


class TestBusinessAccountRequestLogQuery(TestCase):

    def test_success(self):
        logs = list(starkinfra.businessaccountrequest.log.query(limit=10))
        for log in logs:
            self.assertIsNotNone(log.id)
            self.assertIsInstance(log.request, BusinessAccountRequest)

    def test_success_with_params(self):
        logs = starkinfra.businessaccountrequest.log.query(
            limit=10,
            after=date.today() - timedelta(days=100),
            before=date.today(),
            types=["created"],
            account_request_ids=["1", "2", "3"],
        )
        self.assertEqual(len(list(logs)), 0)


class TestBusinessAccountRequestLogPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            logs, cursor = starkinfra.businessaccountrequest.log.page(limit=2, cursor=cursor)
            for log in logs:
                self.assertNotIn(log.id, ids)
                ids.append(log.id)
            if cursor is None:
                break


class TestBusinessAccountRequestLogGet(TestCase):

    def test_success(self):
        log = next(starkinfra.businessaccountrequest.log.query(limit=1), None)
        if log is None:
            self.skipTest("no BusinessAccountRequest log in this workspace")
        fetched = starkinfra.businessaccountrequest.log.get(log.id)
        self.assertEqual(fetched.id, log.id)
        self.assertIsInstance(fetched.created, datetime)

    def test_success_type_enum(self):
        logs = list(starkinfra.businessaccountrequest.log.query(limit=5))
        if not logs:
            self.skipTest("no BusinessAccountRequest log in this workspace")
        for log in logs:
            self.assertIn(
                log.type,
                ["created", "processing", "approved", "denied", "verificationFailed", "updated"],
            )


if __name__ == '__main__':
    main()
