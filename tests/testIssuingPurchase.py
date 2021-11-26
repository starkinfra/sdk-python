import starkinfra
from unittest import TestCase, main
from tests.utils.user import exampleProject

starkinfra.user = exampleProject


class TestIssuingPurchaseQuery(TestCase):

    def test_success(self):
        purchases = starkinfra.issuingpurchase.query(user=exampleProject)
        for purchase in purchases:
            self.assertIsInstance(purchase.id, str)


class TestIssuingPurchaseGet(TestCase):

    def test_success(self):
        purchases = starkinfra.issuingpurchase.query(user=exampleProject, limit=1)
        purchase = starkinfra.issuingpurchase.get(user=exampleProject, id=next(purchases).id)
        self.assertIsInstance(purchase.id, str)


if __name__ == '__main__':
    main()
