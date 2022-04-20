import starkinfra
from unittest import TestCase, main
from tests.utils.user import exampleProject
from tests.utils.withdrawal import generateExampleWithdrawalJson

starkinfra.user = exampleProject


class TestIssuingWithdrawalQuery(TestCase):

    def test_success(self):
        withdrawals = starkinfra.issuingwithdrawal.query(limit=10)
        for withdrawal in withdrawals:
            self.assertIsInstance(withdrawal.id, (str, unicode))


class TestIssuingWithdrawalGet(TestCase):

    def test_success(self):
        withdrawals = starkinfra.issuingwithdrawal.query(limit=1)
        withdrawal = starkinfra.issuingwithdrawal.get(id=next(withdrawals).id)
        self.assertIsInstance(withdrawal.id, (str, unicode))


class TestIssuingWithdrawalPost(TestCase):

    def test_success(self):
        example_withdrawal = generateExampleWithdrawalJson()
        withdrawal = starkinfra.issuingwithdrawal.create(
            amount=example_withdrawal.amount,
            external_id=example_withdrawal.external_id,
            description=example_withdrawal.description,
        )
        self.assertIsInstance(withdrawal.id, (str, unicode))


if __name__ == '__main__':
    main()
