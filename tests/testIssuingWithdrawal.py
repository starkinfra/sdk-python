import starkinfra
from unittest import TestCase, main
from tests.utils.user import exampleProject
from tests.utils.withdrawal import generateExampleWithdrawalJson

starkinfra.user = exampleProject


class TestIssuingWithdrawalQuery(TestCase):

    def test_success(self):
        withdrawals = starkinfra.issuingwithdrawal.query(user=exampleProject)
        for withdrawal in withdrawals:
            print(withdrawal)
            self.assertIsInstance(withdrawal.id, str)


class TestIssuingWithdrawalGet(TestCase):

    def test_success(self):
        withdrawals = starkinfra.issuingwithdrawal.query(user=exampleProject, limit=1)
        withdrawal = starkinfra.issuingwithdrawal.get(user=exampleProject, id=next(withdrawals).id)
        self.assertIsInstance(withdrawal.id, str)


class TestIssuingWithdrawalPost(TestCase):

    def test_success(self):
        withdrawal = starkinfra.issuingwithdrawal.create(generateExampleWithdrawalJson())
        self.assertIsInstance(withdrawal.id, str)


if __name__ == '__main__':
    main()
