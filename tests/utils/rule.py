# coding: utf-8
from copy import deepcopy
from random import choice, randint
from starkinfra import IssuingRule


example_rule = IssuingRule(
    name="Example Rule",
    interval="day",
    amount=100000,
    currency_code="USD"
)


def generateExampleRuleJson(n=1):
    rules = []
    for _ in range(n):
        example_rule.interval = choice(["day", "week", "month", "instant"])
        example_rule.amount = randint(1000, 100000)
        example_rule.currency_code = choice(["BRL", "USD"])
        rules.append(deepcopy(example_rule))
    return rules
