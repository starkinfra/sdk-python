import starkinfra
import starkbank
from unittest import TestCase, main
from tests.utils.user import exampleProject


starkbank.user = exampleProject


class TestIssuingBalanceQuery(TestCase):

    def test_success(self):
        balance = starkinfra.issuingbalance.get(user=exampleProject)
        self.assertIsInstance(balance.amount, int)


if __name__ == '__main__':
    main()
