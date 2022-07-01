import starkinfra
from json import dumps, loads
from unittest import TestCase, main
from datetime import timedelta, date
from starkcore.error import InvalidSignatureError
from tests.utils.user import exampleProject
from tests.utils.pixReversal import generateExamplePixReversalJson


starkinfra.user = exampleProject


class TestPixReversalPost(TestCase):

    def test_success(self):
        pix_reversals = generateExamplePixReversalJson(n=1)
        pix_reversals = starkinfra.pixreversal.create(pix_reversals)
        self.assertEqual(len(pix_reversals), 1)
        for pix_reversal in pix_reversals:
            print(pix_reversal.id)


class TestPixReversalQuery(TestCase):

    def test_success(self):
        pix_reversals = list(starkinfra.pixreversal.query(limit=10))
        assert len(pix_reversals) == 10

    def test_success_with_params(self):
        pix_reversals = starkinfra.pixreversal.query(
            limit=10,
            after=date.today() - timedelta(days=100),
            before=date.today(),
            status="failed",
            tags=["iron", "bank"],
            ids=["1", "2", "3"],  # HUSTON
            external_ids=["1", "2", "3"],  # HUSTON
            return_ids=["1", "2", "3"],
        )
        self.assertEqual(len(list(pix_reversals)), 0)


class TestPixReversalPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            pix_reversals, cursor = starkinfra.pixreversal.page(limit=2, cursor=cursor)
            for pix_reversal in pix_reversals:
                print(pix_reversal)
                self.assertFalse(pix_reversal.id in ids)
                ids.append(pix_reversal.id)
            if cursor is None:
                break
        self.assertTrue(len(ids) == 4)


class TestPixReversalInfoGet(TestCase):

    def test_success(self):
        pix_reversals = starkinfra.pixreversal.query()
        pix_reversal_id = next(pix_reversals).id
        pix_reversal = starkinfra.pixreversal.get(id=pix_reversal_id)
        self.assertIsNotNone(pix_reversal.id)
        self.assertEqual(pix_reversal.id, pix_reversal_id)

    def test_success_ids(self):
        pix_reversals = starkinfra.pixreversal.query(limit=5)
        pix_reversals_ids_expected = [t.id for t in pix_reversals]
        pix_reversals_ids_result = [t.id for t in starkinfra.pixreversal.query(ids=pix_reversals_ids_expected)]
        pix_reversals_ids_expected.sort()
        pix_reversals_ids_result.sort()
        self.assertTrue(pix_reversals_ids_result)
        self.assertEqual(pix_reversals_ids_expected, pix_reversals_ids_result)


class TesteEventProcess(TestCase):
    content = '{"amount": "10", "external_id": "82635892395", "end_to_end_id": "E20018183202201201450u34sDGd19lz", "reason": "bankError", "tags": ["teste","sdk"], "senderAccountType": "payment", "fee": 0, "receiverName": "Cora", "cashierType": "", "externalId": "", "method": "manual", "status": "processing", "updated": "2022-02-16T17:23:53.980250+00:00", "description": "", "tags": [], "receiverKeyId": "", "cashAmount": 0, "senderBankCode": "20018183", "senderBranchCode": "0001", "bankCode": "34052649", "senderAccountNumber": "5647143184367616", "receiverAccountNumber": "5692908409716736", "initiatorTaxId": "", "receiverTaxId": "34.052.649/0001-78", "created": "2022-02-16T17:23:53.980238+00:00", "flow": "in", "endToEndId": "E20018183202202161723Y4cqxlfLFcm", "amount": 1, "receiverAccountType": "checking", "reconciliationId": "", "receiverBankCode": "34052649"}'
    valid_signature = "MEUCIQC7FVhXdripx/aXg5yNLxmNoZlehpyvX3QYDXJ8o02X2QIgVwKfJKuIS5RDq50NC/+55h/7VccDkV1vm8Q/7jNu0VM="
    invalid_signature = "MEUCIQDOpo1j+V40DNZK2URL2786UQK/8mDXon9ayEd8U0/l7AIgYXtIZJBTs8zCRR3vmted6Ehz/qfw1GRut/eYyvf1yOk="
    malformed_signature = "something is definitely wrong"

    def test_success(self):
        reversal = starkinfra.pixreversal.parse(
            content=self.content,
            signature=self.valid_signature
        )
        print(reversal)

    def test_normalized_success(self):
        reversal = starkinfra.pixreversal.parse(
            content=dumps(loads(self.content), sort_keys=False, indent=4),
            signature=self.valid_signature
        )
        print(reversal)

    def test_invalid_signature(self):
        with self.assertRaises(InvalidSignatureError):
            starkinfra.pixreversal.parse(
                content=self.content,
                signature=self.invalid_signature,
            )

    def test_malformed_signature(self):
        with self.assertRaises(InvalidSignatureError):
            starkinfra.pixreversal.parse(
                content=self.content,
                signature=self.malformed_signature,
            )


class TestPixRequestResponse(TestCase):

    def test_approved(self):
        response = starkinfra.pixreversal.response(
            status="approved",
        )
        print(response)

    def test_denied(self):
        response = starkinfra.pixreversal.response(
            status="denied",
            reason="taxIdMismatch",
        )
        print(response)


if __name__ == '__main__':
    main()
