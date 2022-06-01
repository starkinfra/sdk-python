import starkinfra
from unittest import TestCase, main
from datetime import date, timedelta
from starkinfra import IssuingWithdrawal
from tests.utils.user import exampleProject
from tests.utils.withdrawal import generateExampleWithdrawalJson

starkinfra.user = exampleProject


class TestIssuingWithdrawalQuery(TestCase):

    def test_success(self):
        withdrawals = starkinfra.issuingwithdrawal.query(
            limit=10,
            after=date.today() - timedelta(days=100),
            before=date.today(),
        )
        for withdrawal in withdrawals:
            self.assertEqual(withdrawal.id, str(withdrawal.id))


class TestIssuingWithdrawalGet(TestCase):

    def test_success(self):
        withdrawals = starkinfra.issuingwithdrawal.query(limit=1)
        withdrawal = starkinfra.issuingwithdrawal.get(id=next(withdrawals).id)
        self.assertEqual(withdrawal.id, str(withdrawal.id))


class TestIssuingWithdrawalPost(TestCase):

    def test_success(self):
        example_withdrawal = generateExampleWithdrawalJson()
        withdrawal = starkinfra.issuingwithdrawal.create(
            withdrawal=IssuingWithdrawal(
                amount=example_withdrawal.amount,
                external_id=example_withdrawal.external_id,
                description=example_withdrawal.description,
            )
        )
        self.assertEqual(withdrawal.id, str(withdrawal.id))


if __name__ == '__main__':
    main()
