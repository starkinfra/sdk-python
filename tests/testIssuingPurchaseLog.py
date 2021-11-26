import starkinfra
from unittest import TestCase, main
from tests.utils.user import exampleProject

starkinfra.user = exampleProject


class TestIssuingPurchaseLogQuery(TestCase):

    def test_success(self):
        logs = starkinfra.issuingpurchase.log.query()
        for log in logs:
            self.assertIsInstance(log.id, str)


class TestIssuingPurchaseLogGet(TestCase):

    def test_success(self):
        logs = starkinfra.issuingpurchase.log.query(limit=1)
        log = starkinfra.issuingpurchase.log.get(id=next(logs).id)
        self.assertIsInstance(log.id, str)


if __name__ == '__main__':
    main()
