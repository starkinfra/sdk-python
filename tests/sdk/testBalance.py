import starkinfra
from unittest import TestCase, main
from tests.utils.user import exampleProject


starkinfra.user = exampleProject


class TestPixBalanceGet(TestCase):

    def test_success(self):
        pix_balance = starkinfra.pixbalance.get(user=exampleProject)
        print(pix_balance)
        self.assertIsInstance(pix_balance.amount, int)


if __name__ == '__main__':
    main()
