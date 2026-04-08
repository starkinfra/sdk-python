import starkinfra
from unittest import TestCase, main
from tests.utils.user import exampleProject
from tests.utils.individualAccountRequest import generateExampleIndividualAccountRequestJson


starkinfra.user = exampleProject


class TestIndividualAccountRequestPost(TestCase):

    def test_success(self):
        requests = generateExampleIndividualAccountRequestJson(n=1)
        requests = starkinfra.individualaccountrequest.create(requests)
        for request in requests:
            self.assertIsNotNone(request.id)


class TestIndividualAccountRequestQuery(TestCase):

    def test_success(self):
        requests = list(starkinfra.individualaccountrequest.query(limit=1))
        for request in requests:
            print(request)
        print("Number of requests:", len(requests))


class TestIndividualAccountRequestPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            requests, cursor = starkinfra.individualaccountrequest.page(limit=2, cursor=cursor)
            for request in requests:
                print(request)
                self.assertFalse(request.id in ids)
                ids.append(request.id)
            if cursor is None:
                break
        self.assertEqual(len(ids), 4)


class TestIndividualAccountRequestInfoGet(TestCase):

    def test_success(self):
        requests = starkinfra.individualaccountrequest.query(limit=3)
        for request in requests:
            request_id = request.id
            request_new = starkinfra.individualaccountrequest.get(request_id)
            self.assertEqual(request_new.id, request_id)


class TestIndividualAccountRequestUpdate(TestCase):

    def test_success(self):
        requests = starkinfra.individualaccountrequest.query(limit=1)
        for request in requests:
            request = starkinfra.individualaccountrequest.update(id=request.id, name=request.name)
            self.assertIsNotNone(request.id)


if __name__ == '__main__':
    main()
