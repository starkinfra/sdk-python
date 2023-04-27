import starkinfra
from unittest import TestCase, main
from tests.utils.user import exampleProject

starkinfra.user = exampleProject


class TestIssuingEmbossingKitQuery(TestCase):

    def test_success(self):
        kits = starkinfra.issuingembossingkit.query()
        for kit in kits:
            self.assertEqual(kit.id, str(kit.id))


class TestIssuingEmbossingKitPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            kits, cursor = starkinfra.issuingembossingkit.page(
                limit=2,
                cursor=cursor
            )
            for kit in kits:
                self.assertFalse(kit.id in ids)
                ids.append(kit.id)
            if cursor is None:
                break


class TestIssuingEmbossingKitGet(TestCase):

    def test_success(self):
        kits = starkinfra.issuingembossingkit.query(limit=1)
        kit = starkinfra.issuingembossingkit.get(id=next(kits).id)
        self.assertEqual(kit.id, str(kit.id))


if __name__ == '__main__':
    main()
