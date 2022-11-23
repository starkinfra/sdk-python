import starkinfra
from unittest import TestCase, main
from datetime import date, timedelta
from tests.utils.user import exampleProject
from tests.utils.issuingEmbossingRequest import generateExampleEmbossingRequestsJson

starkinfra.user = exampleProject


class TestIssuingEmbossingRequestQuery(TestCase):

    def test_success(self):
        requests = starkinfra.issuingembossingrequest.query(
            after=date.today() - timedelta(days=100),
            before=date.today(),
        )
        for request in requests:
            self.assertEqual(request.id, str(request.id))


class TestIssuingEmbossingRequestPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            requests, cursor = starkinfra.issuingembossingrequest.page(
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


class TestIssuingEmbossingRequestGet(TestCase):

    def test_success(self):
        requests = starkinfra.issuingembossingrequest.query(limit=1)
        request = starkinfra.issuingembossingrequest.get(id=next(requests).id)
        self.assertEqual(request.id, str(request.id))


class TestIssuingEmbossingRequestPost(TestCase):

    def test_success(self):
        example_requests = generateExampleEmbossingRequestsJson(n=5)
        requests = starkinfra.issuingembossingrequest.create(example_requests)
        for request in requests:
            self.assertEqual(request.id, str(request.id))


if __name__ == '__main__':
    main()
