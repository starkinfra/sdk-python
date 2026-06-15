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
                self.assertFalse(log.id in ids)
                ids.append(log.id)
            if cursor is None:
                break
        self.assertTrue(len(ids) == 4)


class TestIndividualAccountRequestLogGet(TestCase):

    def test_success(self):
        logs = starkinfra.individualaccountrequest.log.query(limit=1)
        log_id = next(logs).id
        log = starkinfra.individualaccountrequest.log.get(id=log_id)
        self.assertEqual(log.id, log_id)
        self.assertIsInstance(log.request, IndividualAccountRequest)
        self.assertIn(
            log.type,
            ["approved", "created", "denied", "processing", "updated"],
        )


if __name__ == '__main__':
    main()
