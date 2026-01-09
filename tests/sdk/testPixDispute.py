import starkinfra
from unittest import TestCase, main
from datetime import timedelta, date
from tests.utils.user import exampleProject
from starkcore.error import InvalidSignatureError


starkinfra.user = exampleProject


class TestPixDisputeCreate(TestCase):

    def test_success(self):
        pix_disputes = starkinfra.pixdispute.create([
            starkinfra.PixDispute(
                reference_id="E20018183202512191914WcfANNEIYnt",
                method="scam",
                operator_phone="+5511999999999",
                operator_email="operator@example.com"
            )
        ])


class TestPixDisputeQuery(TestCase):

    def test_success(self):
        pix_disputes = list(starkinfra.pixdispute.query(limit=10))
        assert len(pix_disputes) == 10

    def test_success_with_params(self):
        pix_disputes = starkinfra.pixdispute.query(
            limit=10,
            after=date.today() - timedelta(days=100),
            before=date.today(),
            status="failed",
            tags=["iron", "bank"],
            ids=["1", "2", "3"],
        )
        self.assertEqual(len(list(pix_disputes)), 0)


class TestPixDisputePage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            pix_disputes, cursor = starkinfra.pixdispute.page(limit=2, cursor=cursor)
            for pix_dispute in pix_disputes:
                self.assertFalse(pix_dispute.id in ids)
                ids.append(pix_dispute.id)
            if cursor is None:
                break
        self.assertTrue(len(ids) == 4)


class testPixDisputeQueryAndDelete(TestCase):
    
    def test_success(self):
        pix_disputes = list(starkinfra.pixdispute.query(status=["created", "delivered"], limit=1))
        if not pix_disputes:
            self.skipTest("No disputes found")
        for pix_dispute in pix_disputes:
            deleted_pix_dispute = starkinfra.pixdispute.cancel(id=pix_dispute.id)
            self.assertEqual(deleted_pix_dispute.id, pix_dispute.id)

class TestPixDisputeInfoGet(TestCase):

    def test_success(self):
        pix_disputes = starkinfra.pixdispute.query()
        pix_dispute_id = next(pix_disputes).id
        pix_dispute = starkinfra.pixdispute.get(id=pix_dispute_id)
        self.assertIsNotNone(pix_dispute.id)
        self.assertEqual(pix_dispute.id, pix_dispute_id)
    
    def test_success_ids(self):
        pix_disputes = starkinfra.pixdispute.query(limit=5)
        pix_disputes_ids_expected = [t.id for t in pix_disputes]
        pix_disputes_ids_result = [t.id for t in starkinfra.pixdispute.query(ids=pix_disputes_ids_expected)]
        pix_disputes_ids_expected.sort()
        pix_disputes_ids_result.sort()
        self.assertTrue(pix_disputes_ids_result)
        self.assertEqual(pix_disputes_ids_expected, pix_disputes_ids_result)


class TestPixDisputeEventParse(TestCase):
    content = '{"event": {"created": "2025-12-19T19:20:08.687079+00:00", "id": "4543235613523968", "log": {"created": "2025-12-19T19:20:08.107566+00:00", "dispute": {"bacenId": "42e3c802-22c0-4862-b352-cedc912c07a1", "created": "2025-12-19T19:16:04.867430+00:00", "description": "", "flow": "in", "id": "4652621482688512", "maxHopCount": 5, "maxHopInterval": 86400, "maxTransactionCount": 500, "method": "scam", "minTransactionAmount": 20000, "operatorEmail": "fraud@company.com", "operatorPhone": "+5511989898989", "referenceId": "E20018183202512191914WcfANNEIYnt", "status": "analysed", "tags": [], "transactions": [{"amount": 20000, "endToEndId": "E20018183202512191914WcfANNEIYnt", "nominalAmount": 20000, "receiverAccountCreated": "", "receiverBankCode": "39908427", "receiverId": "1", "receiverTaxIdCreated": "", "receiverType": "business", "senderAccountCreated": "", "senderBankCode": "20018183", "senderId": "2", "senderTaxIdCreated": "", "senderType": "business", "settled": "2025-12-19T19:14:25.760000+00:00"}], "updated": "2025-12-19T19:20:08.107585+00:00"}, "errors": [], "id": "6007878011846656", "type": "analysed"}, "subscription": "pix-dispute", "workspaceId": "5560467233701888"}}'
    valid_signature = "MEYCIQCPgzyktxttTM9ooQaXq37NvFjL2cF/nQMfl1rvUcsLAQIhAKLbphPa5311mHvXlz6Rtkk+LPhctxgGYOnxAdhdldls"
    invalid_signature = "MEUCIQDOpo1j+V40DNZK2URL2786UQK/8mDXon9ayEd8U0/l7AIgYXtIZJBTs8zCRR3vmted6Ehz/qfw1GRut/eYyvf1yOk="

    def test_success(self):
        event = starkinfra.event.parse(
            content=self.content,
            signature=self.valid_signature
        )

    def test_invalid_signature(self):
        with self.assertRaises(InvalidSignatureError):
            starkinfra.event.parse(
                content=self.content,
                signature=self.invalid_signature,
            )


if __name__ == '__main__':
    main()
