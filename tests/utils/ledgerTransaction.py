import starkinfra
from copy import deepcopy
from random import randint
from starkinfra.ledger import Rule
from starkinfra import LedgerTransaction


_local_cache = {}
example_ledger_transaction = LedgerTransaction(
    amount=10,
    ledger_id="123",
    source="123",
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


def generateExampleLedgerTransactionJson(n=1):
    ledger_transactions = []
    for _ in range(n):
        example_ledger_transaction.amount = randint(1000, 9999)
        example_ledger_transaction.source = "account/" + str(randint(1, 999999)).zfill(6)
        example_ledger_transaction.external_id = str(randint(1, 999999)).zfill(6)
        ledger_transactions.append(deepcopy(example_ledger_transaction))
    return ledger_transactions


def getLedgerWithTransactions(min_transaction_count=10):
    ledger_with_transactions = _local_cache.get("ledger_with_transactions")
    if ledger_with_transactions:
        return ledger_with_transactions

    for ledger in starkinfra.ledger.query(limit=20):
        _transactions, cursor = starkinfra.ledgertransaction.page(ledger_id=ledger.id, limit=min_transaction_count - 1)
        if cursor:
            _local_cache["ledger_with_transactions"] = ledger
            break

    return _local_cache["ledger_with_transactions"]
