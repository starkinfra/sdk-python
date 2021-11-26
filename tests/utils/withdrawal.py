# coding: utf-8
from copy import deepcopy
from random import randint
from starkinfra import IssuingWithdrawal


example_withdrawal = IssuingWithdrawal(
    amount=10,
    external_id="123",
    description="Issuing Withdrawal test"
)


def generateExampleWithdrawalJson():
    example_withdrawal.external_id = str(randint(1, 999999))
    example_withdrawal.amount = randint(100, 1000)
    return example_withdrawal
