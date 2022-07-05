import starkinfra
from unittest import TestCase, main
from tests.utils.user import exampleProject


starkinfra.user = exampleProject


class TestIssuingProductQuery(TestCase):

    def test_success(self):
        products = starkinfra.issuingproduct.query()
        for product in products:
            self.assertEqual(product.id, str(product.id))


class TestIssuingProductPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            products, cursor = starkinfra.issuingproduct.page(limit=2, cursor=cursor)
            for product in products:
                self.assertFalse(product.id in ids)
                ids.append(product.id)
            if cursor is None:
                break


if __name__ == '__main__':
    main()
