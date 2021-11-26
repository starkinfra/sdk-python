import starkinfra
from unittest import TestCase, main
from tests.utils.user import exampleProject


starkinfra.user = exampleProject


class TestIssuingBalanceQuery(TestCase):

    def test_success(self):
        balance = starkinfra.issuingbalance.get()
        self.assertIsInstance(balance.amount, int)


if __name__ == '__main__':
    main()
