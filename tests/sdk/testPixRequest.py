import starkinfra
from unittest import TestCase, main
from datetime import timedelta, date
from tests.utils.user import exampleProject
from starkcore.error import InvalidSignatureError
from tests.utils.pixRequest import generateExamplePixRequestJson


starkinfra.user = exampleProject


class TestPixRequestPost(TestCase):
    def test_success(self):
        pix_requests = generateExamplePixRequestJson(n=5)
        pix_requests = starkinfra.pixrequest.create(pix_requests)
        self.assertEqual(len(pix_requests), 5)
        for pix_request in pix_requests:
            print(pix_request.id)


class TestPixRequestQuery(TestCase):

    def test_success(self):
        pix_requests = list(starkinfra.pixrequest.query(limit=10))
        assert len(pix_requests) == 10

    def test_success_with_params(self):
        pix_requests = starkinfra.pixrequest.query(
            limit=10,
            after=date.today() - timedelta(days=100),
            before=date.today(),
            status="failed",
            tags=["iron", "bank"],
            ids=["1", "2", "3"],
            external_ids=["1", "2", "3"],
            end_to_end_ids=["1", "2", "3"],
        )
        self.assertEqual(len(list(pix_requests)), 0)


class TestPixRequestPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            pix_requests, cursor = starkinfra.pixrequest.page(limit=2, cursor=cursor)
            for pix_request in pix_requests:
                print(pix_request)
                self.assertFalse(pix_request.id in ids)
                ids.append(pix_request.id)
            if cursor is None:
                break
        self.assertTrue(len(ids) == 4)


class TestPixRequestInfoGet(TestCase):

    def test_success(self):
        pix_requests = starkinfra.pixrequest.query()
        pix_request_id = next(pix_requests).id
        pix_request = starkinfra.pixrequest.get(id=pix_request_id)
        self.assertIsNotNone(pix_request.id)
        self.assertEqual(pix_request.id, pix_request_id)
    
    def test_success_ids(self):
        pix_requests = starkinfra.pixrequest.query(limit=5)
        pix_requests_ids_expected = [t.id for t in pix_requests]
        pix_requests_ids_result = [t.id for t in starkinfra.pixrequest.query(ids=pix_requests_ids_expected)]
        pix_requests_ids_expected.sort()
        pix_requests_ids_result.sort()
        self.assertTrue(pix_requests_ids_result)
        self.assertEqual(pix_requests_ids_expected, pix_requests_ids_result)


class TesteEventProcess(TestCase):
    content = '{"receiverBranchCode": "0001", "cashierBankCode": "", "senderTaxId": "20.018.183/0001-80", "senderName": "Stark Bank S.A. - Instituicao de Pagamento", "id": "4508348862955520", "senderAccountType": "payment", "fee": 0, "receiverName": "Cora", "cashierType": "", "externalId": "", "method": "manual", "status": "processing", "updated": "2022-02-16T17:23:53.980250+00:00", "description": "", "tags": [], "receiverKeyId": "", "cashAmount": 0, "senderBankCode": "20018183", "senderBranchCode": "0001", "bankCode": "34052649", "senderAccountNumber": "5647143184367616", "receiverAccountNumber": "5692908409716736", "initiatorTaxId": "", "receiverTaxId": "34.052.649/0001-78", "created": "2022-02-16T17:23:53.980238+00:00", "flow": "in", "endToEndId": "E20018183202202161723Y4cqxlfLFcm", "amount": 1, "receiverAccountType": "checking", "reconciliationId": "", "receiverBankCode": "34052649"}'
    valid_signature = "MEUCIQC7FVhXdripx/aXg5yNLxmNoZlehpyvX3QYDXJ8o02X2QIgVwKfJKuIS5RDq50NC/+55h/7VccDkV1vm8Q/7jNu0VM="
    invalid_signature = "MEUCIQDOpo1j+V40DNZK2URL2786UQK/8mDXon9ayEd8U0/l7AIgYXtIZJBTs8zCRR3vmted6Ehz/qfw1GRut/eYyvf1yOk="
    malformed_signature = "something is definitely wrong"

    def test_success(self):
        request = starkinfra.pixrequest.parse(
            content=self.content,
            signature=self.valid_signature
        )
        print(request)

    def test_invalid_signature(self):
        with self.assertRaises(InvalidSignatureError):
            starkinfra.pixrequest.parse(
                content=self.content,
                signature=self.invalid_signature,
            )

    def test_malformed_signature(self):
        with self.assertRaises(InvalidSignatureError):
            starkinfra.pixrequest.parse(
                content=self.content,
                signature=self.malformed_signature,
            )


class TestPixRequestResponse(TestCase):

    def test_approved(self):
        response = starkinfra.pixrequest.response(
            status="approved",
        )
        print(response)

    def test_denied(self):
        response = starkinfra.pixrequest.response(
            status="denied",
            reason="taxIdMismatch",
        )
        print(response)


if __name__ == '__main__':
    main()
