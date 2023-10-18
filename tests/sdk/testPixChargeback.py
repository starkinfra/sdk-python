import starkinfra

from unittest import TestCase, main
from datetime import timedelta, date
from tests.utils.user import exampleProject, bank_code
from tests.utils.pixChargeback import generateExamplePixChargebackJson, getPixChargebackToPatch


starkinfra.user = exampleProject


class TestPixChargebackPostAndDelete(TestCase):
    def test_success(self):
        pix_chargebacks = generateExamplePixChargebackJson(n=2)
        pix_chargebacks = starkinfra.pixchargeback.create(pix_chargebacks)
        self.assertIsNotNone(pix_chargebacks)
        for chargeback in pix_chargebacks:
            deleted_reversal_request = starkinfra.pixchargeback.cancel(chargeback.id)
            self.assertEqual(deleted_reversal_request.status, "canceled")
            print(chargeback.id)


class TestPixChargebackQuery(TestCase):

    def test_success(self):
        reversal_requests = list(starkinfra.pixchargeback.query(limit=3))
        assert len(reversal_requests) == 3

    def test_success_with_params(self):
        reversal_requests = starkinfra.pixchargeback.query(
            limit=10,
            after=date.today() - timedelta(days=100),
            before=date.today(),
            status="failed",
            ids=["1", "2"],
            bacen_id="ccf9bd9c-e99d-999e-bab9-b999ca999f99"
        )
        self.assertEqual(len(list(reversal_requests)), 0)


class TestPixChargebackPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            reversal_requests, cursor = starkinfra.pixchargeback.page(limit=2, cursor=cursor)
            for reversal_request in reversal_requests:
                print(reversal_request)
                self.assertFalse(reversal_request.id in ids)
                ids.append(reversal_request.id)
            if cursor is None:
                break
        self.assertTrue(len(ids) == 4)


class TestPixChargebackInfoGet(TestCase):

    def test_success(self):
        reversal_requests = starkinfra.pixchargeback.query()
        reversal_request_id = next(reversal_requests).id
        reversal_request = starkinfra.pixchargeback.get(id=reversal_request_id)
        self.assertIsNotNone(reversal_request.id)
        self.assertEqual(reversal_request.id, reversal_request_id)
        print(reversal_request)
    
    def test_success_ids(self):
        reversal_requests = starkinfra.pixchargeback.query(limit=5)
        reversal_requests_ids_expected = [t.id for t in reversal_requests]
        reversal_requests_ids_result = [t.id for t in starkinfra.pixchargeback.query(ids=reversal_requests_ids_expected)]
        reversal_requests_ids_expected.sort()
        reversal_requests_ids_result.sort()
        self.assertTrue(reversal_requests_ids_result)
        self.assertEqual(reversal_requests_ids_expected, reversal_requests_ids_result)


class TestPixChargebackInfoPatch(TestCase):

    def test_success_cancel(self):
        reversal_request = getPixChargebackToPatch()
        self.assertIsNotNone(reversal_request.id)
        self.assertEqual(reversal_request.status, "delivered")
        print(reversal_request)
        updated_reversal_request = starkinfra.pixchargeback.update(
            id=reversal_request.id,
            result="accepted",
            reversal_reference_id=starkinfra.returnid.create(bank_code=bank_code),
        )
        self.assertEqual(updated_reversal_request.result, "agreed")


if __name__ == '__main__':
    main()
