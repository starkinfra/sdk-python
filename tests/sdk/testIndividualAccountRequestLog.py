import starkinfra
from datetime import date, timedelta
from unittest import TestCase, main
from tests.utils.user import exampleProject
from starkinfra import IndividualAccountRequest


starkinfra.user = exampleProject


class TestIndividualAccountRequestLogQuery(TestCase):

    def test_success(self):
        logs = list(starkinfra.individualaccountrequest.log.query(limit=10))
        for log in logs:
            self.assertIsNotNone(log.id)

    def test_success_with_params(self):
        logs = starkinfra.individualaccountrequest.log.query(
            limit=10,
            after=date.today() - timedelta(days=100),
            before=date.today(),
            types=["created", "processing"],
            account_request_ids=["1", "2", "3"],
        )
        self.assertEqual(len(list(logs)), 0)


class TestIndividualAccountRequestLogPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            logs, cursor = starkinfra.individualaccountrequest.log.page(limit=2, cursor=cursor)
            for log in logs:
                self.assertNotIn(log.id, ids)
                ids.append(log.id)
            if cursor is None:
                break


class TestIndividualAccountRequestLogGet(TestCase):

    def test_success(self):
        first = next(starkinfra.individualaccountrequest.log.query(limit=1), None)
        if first is None:
            self.skipTest("no IndividualAccountRequest log in this workspace")
        log = starkinfra.individualaccountrequest.log.get(id=first.id)
        self.assertEqual(log.id, first.id)
        self.assertIsInstance(log.request, IndividualAccountRequest)
        self.assertIn(
            log.type,
            ["created", "processing", "approved", "denied", "verificationFailed", "updated"],
        )


if __name__ == '__main__':
    main()
