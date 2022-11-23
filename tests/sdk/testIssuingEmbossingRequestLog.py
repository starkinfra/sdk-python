import starkinfra
from datetime import date, timedelta
from unittest import TestCase, main
from tests.utils.user import exampleProject

starkinfra.user = exampleProject


class TestIssuingEmbossingRequestLogQuery(TestCase):

    def test_success(self):
        logs = starkinfra.issuingembossingrequest.log.query(limit=10)
        for log in logs:
            self.assertEqual(log.id, str(log.id))


class TestIssuingEmbossingRequestPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            requests, cursor = starkinfra.issuingembossingrequest.log.page(
                limit=2,
                after=date.today() - timedelta(days=100),
                before=date.today(),
                cursor=cursor
            )
            for request in requests:
                self.assertFalse(request.id in ids)
                ids.append(request.id)
            if cursor is None:
                break


class TestIssuingEmbossingRequestLogGet(TestCase):

    def test_success(self):
        logs = starkinfra.issuingembossingrequest.log.query(limit=1)
        log = starkinfra.issuingembossingrequest.log.get(id=next(logs).id)
        self.assertEqual(log.id, str(log.id))


if __name__ == '__main__':
    main()
