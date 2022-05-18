import starkinfra
from random import randint, choice
from unittest import TestCase, main
from datetime import timedelta, date
from tests.utils.user import exampleProject
from tests.utils.names.names import get_full_name
from tests.utils.taxIdGenerator import TaxIdGenerator
from tests.utils.pixKey import generateExamplePixKeyJson


starkinfra.user = exampleProject


class TestPixKeyPostAndDelete(TestCase):
    def test_success(self):
        pix_keys = []
        for _ in range(2):
            pix_key = generateExamplePixKeyJson()
            pix_key = starkinfra.pixkey.create(pix_key)
            pix_keys.append(pix_key)
        self.assertEqual(len(pix_keys), 2)


class TestPixKeyQuery(TestCase):

    def test_success(self):
        pix_keys = list(starkinfra.pixkey.query(limit=10))
        assert len(pix_keys) == 10

    def test_success_with_params(self):
        pix_keys = starkinfra.pixkey.query(
            limit=10,
            after=date.today() - timedelta(days=100),
            before=date.today(),
            status="failed",
            tags=["iron", "bank"],
            ids=["+5511988887777"],
            type="cpf",
        )
        self.assertEqual(len(list(pix_keys)), 0)


class TestPixKeyPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            pix_keys, cursor = starkinfra.pixkey.page(limit=2, cursor=cursor)
            for pix_key in pix_keys:
                print(pix_key)
                self.assertFalse(pix_key.id in ids)
                ids.append(pix_key.id)
            if cursor is None:
                break
        self.assertTrue(len(ids) == 4)


class TestPixKeyInfoGet(TestCase):

    def test_success(self):
        pix_keys = starkinfra.pixkey.query()
        pix_key_id = next(pix_keys).id
        pix_key = starkinfra.pixkey.get(id=pix_key_id, payer_id=TaxIdGenerator.taxId())
        self.assertIsNotNone(pix_key.id)
        self.assertEqual(pix_key.id, pix_key_id)
        print(pix_key)
    
    def test_success_ids(self):
        pix_keys = starkinfra.pixkey.query(limit=5)
        pix_keys_ids_expected = [t.id for t in pix_keys]
        pix_keys_ids_result = [t.id for t in starkinfra.pixkey.query(ids=pix_keys_ids_expected)]
        pix_keys_ids_expected.sort()
        pix_keys_ids_result.sort()
        self.assertTrue(pix_keys_ids_result)
        self.assertEqual(pix_keys_ids_expected, pix_keys_ids_result)


class TestPixKeyInfoDelete(TestCase):

    def test_success(self):
        pix_key = next(starkinfra.pixkey.query(status="registered"))
        deleted_pix_key = starkinfra.pixkey.cancel(pix_key.id)
        self.assertIsNotNone(deleted_pix_key.id)
        self.assertEqual(deleted_pix_key.id, pix_key.id)


class TestPixKeyInfoPatch(TestCase):

    def test_success_cancel(self):
        pix_keys = starkinfra.pixkey.query(status="registered", type="phone", limit=1)
        for pix_key in pix_keys:
            print(pix_key)
            self.assertIsNotNone(pix_key.id)
            self.assertEqual(pix_key.status, "registered")
            name = get_full_name()
            updated_pix_key = starkinfra.pixkey.update(
                id=pix_key.id,
                reason="userRequested",
                account_created="2022-01-01",
                account_number=str(randint(10000, 99999)),
                account_type=choice(["checking", "savings", "salary", "payment"]),
                branch_code=str(randint(1000, 9999)),
                name=name,
            )
            self.assertEqual(updated_pix_key.name, name)


if __name__ == '__main__':
    main()
