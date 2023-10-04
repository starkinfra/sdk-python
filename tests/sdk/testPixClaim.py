import starkinfra
from unittest import TestCase, main
from datetime import timedelta, date
from tests.utils.user import exampleProject
from tests.utils.pixClaim import generateExamplePixClaimJson, getPixClaimToPatch


starkinfra.user = exampleProject


class TestPixClaimPost(TestCase):
    def test_success(self):
        pix_claims = []
        for _ in range(2):
            pix_claim = generateExamplePixClaimJson()
            pix_claim = starkinfra.pixclaim.create(pix_claim)
            print(pix_claim)
            pix_claims.append(pix_claim)
        self.assertEqual(len(pix_claims), 2)


class TestPixClaimQuery(TestCase):

    def test_success(self):
        pix_claims = list(starkinfra.pixclaim.query(limit=4))
        assert len(pix_claims) == 4

    def test_success_with_params(self):
        pix_claims = starkinfra.pixclaim.query(
            limit=10,
            after=date.today() - timedelta(days=100),
            before=date.today(),
            status="failed",
            ids=["1", "2", "3"],
            type="ownership",
            flow="out",
            key_type="cpf",
            key_id="123.456.789-09",
            bacen_id="ccf9bd9c-e99d-999e-bab9-b999ca999f99"
        )
        self.assertEqual(len(list(pix_claims)), 0)


class TestPixClaimPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            pix_claims, cursor = starkinfra.pixclaim.page(limit=2, cursor=cursor, flow="out")
            for pix_claim in pix_claims:
                print(pix_claim)
                self.assertFalse(pix_claim.id in ids)
                ids.append(pix_claim.id)
            if cursor is None:
                break
        self.assertTrue(len(ids) == 4)


class TestPixClaimInfoGet(TestCase):

    def test_success(self):
        pix_claims = starkinfra.pixclaim.query()
        pix_claim_id = next(pix_claims).id
        pix_claim = starkinfra.pixclaim.get(id=pix_claim_id)
        self.assertIsNotNone(pix_claim.id)
        self.assertEqual(pix_claim.id, pix_claim_id)
        print(pix_claim)
    
    def test_success_ids(self):
        pix_claims = starkinfra.pixclaim.query(limit=1)
        pix_claims_ids_expected = [t.id for t in pix_claims]
        pix_claims_ids_result = [t.id for t in starkinfra.pixclaim.query(ids=pix_claims_ids_expected)]
        pix_claims_ids_expected.sort()
        pix_claims_ids_result.sort()
        self.assertTrue(pix_claims_ids_result)
        self.assertEqual(pix_claims_ids_expected, pix_claims_ids_result)
        
        
class TestPixClaimInfoPatch(TestCase):

    def test_success_cancel(self):
        pix_claim = getPixClaimToPatch()
        self.assertIsNotNone(pix_claim.id)
        self.assertEqual(pix_claim.status, "delivered")
        updated_pix_claim = starkinfra.pixclaim.update(
            id=pix_claim.id,
            reason="userRequested",
            status="canceled"
        )
        self.assertIsNotNone(updated_pix_claim.id)


if __name__ == '__main__':
    main()
