from copy import deepcopy
from random import randint
from starkinfra import IssuingRestock, issuingstock


example_restock = IssuingRestock(
    count=1000,
    stock_id="6526579068895232"
)


def generateExampleRestocksJson(n=1):
    restocks = []
    for _ in range(n):
        example_restock.count = randint(100, 1000)
        example_restock.stockId = next(issuingstock.query(limit=1)).id
        restocks.append(deepcopy(example_restock))
    return restocks
