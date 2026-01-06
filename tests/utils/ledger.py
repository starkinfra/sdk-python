from copy import deepcopy
from random import randint
from starkinfra import Ledger
from starkinfra.ledger import Rule


example_ledger = Ledger(
    external_id="123",
    tags=[
        "savings account",
        "spending counter",
    ],
    metadata={
        "account_id": "123",
    },
    rules=[
        Rule(
            key="minimumBalance",
            value=0,
        ),
    ],
)


def generateExampleLedgerJson(n=1):
    ledgers = []
    for _ in range(n):
        example_ledger.external_id = str(randint(1, 999999))
        ledgers.append(deepcopy(example_ledger))
    return ledgers
