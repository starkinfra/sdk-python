import starkinfra
from ..utils.user import bank_code
from unittest import TestCase, main
from datetime import timedelta, date
from tests.utils.user import exampleProject
from tests.utils.reversalRequest import generateExampleReversalRequestJson, getReversalRequestToPatch


starkinfra.user = exampleProject


class TestReversalRequestPostAndDelete(TestCase):
    def test_success(self):
        reversal_request = generateExampleReversalRequestJson()
        reversal_request = starkinfra.reversalrequest.create(reversal_request)
        print(reversal_request)
        self.assertIsNotNone(reversal_request)
        deleted_reversal_request = starkinfra.reversalrequest.delete(reversal_request.id)
        self.assertEqual(deleted_reversal_request.status, "canceled")
        print(reversal_request.id)


class TestReversalRequestQuery(TestCase):

    def test_success(self):
        reversal_requests = list(starkinfra.reversalrequest.query(limit=3))
        assert len(reversal_requests) == 3

    def test_success_with_params(self):
        reversal_requests = starkinfra.reversalrequest.query(
            limit=10,
            after=date.today() - timedelta(days=100),
            before=date.today(),
            status="failed",
            ids=["1", "2"],
        )
        self.assertEqual(len(list(reversal_requests)), 0)


class TestReversalRequestPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            reversal_requests, cursor = starkinfra.reversalrequest.page(limit=2, cursor=cursor)
            for reversal_request in reversal_requests:
                print(reversal_request)
                self.assertFalse(reversal_request.id in ids)
                ids.append(reversal_request.id)
            if cursor is None:
                break
        self.assertTrue(len(ids) == 4)


class TestReversalRequestInfoGet(TestCase):

    def test_success(self):
        reversal_requests = starkinfra.reversalrequest.query()
        reversal_request_id = next(reversal_requests).id
        reversal_request = starkinfra.reversalrequest.get(id=reversal_request_id)
        self.assertIsNotNone(reversal_request.id)
        self.assertEqual(reversal_request.id, reversal_request_id)
        print(reversal_request)
    
    def test_success_ids(self):
        reversal_requests = starkinfra.reversalrequest.query(limit=5)
        reversal_requests_ids_expected = [t.id for t in reversal_requests]
        reversal_requests_ids_result = [t.id for t in starkinfra.reversalrequest.query(ids=reversal_requests_ids_expected)]
        reversal_requests_ids_expected.sort()
        reversal_requests_ids_result.sort()
        self.assertTrue(reversal_requests_ids_result)
        self.assertEqual(reversal_requests_ids_expected, reversal_requests_ids_result)


class TestReversalRequestInfoPatch(TestCase):

    def test_success_cancel(self):
        reversal_request = getReversalRequestToPatch()
        self.assertIsNotNone(reversal_request.id)
        self.assertEqual(reversal_request.status, "delivered")
        print(reversal_request)
        updated_reversal_request = starkinfra.reversalrequest.update(
            id=reversal_request.id,
            result="accepted",
            reversal_reference_id=starkinfra.returnid.create(bank_code=bank_code),
        )
        self.assertEqual(updated_reversal_request.result, "agreed")


if __name__ == '__main__':
    main()
