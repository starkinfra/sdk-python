from copy import deepcopy
from random import randint
from starkinfra import IssuingStockRule, issuingstock


example_stock_rule = IssuingStockRule(
    minimum_balance=10000,
    stock_id="6526579068895232",
    tags=["test"],
    emails=["john.doe@enterprise.com"],
    phones=["+55 (11) 1234-5678"],
)


def generateExampleStockRulesJson(n=1):
    rules = []
    for _ in range(n):
        example_stock_rule.minimum_balance = randint(1000, 100000)
        example_stock_rule.stock_id = next(issuingstock.query(limit=1)).id
        rules.append(deepcopy(example_stock_rule))
    return rules
