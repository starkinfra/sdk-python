# coding: utf-8
from copy import deepcopy
from random import randint
from starkinfra import IssuingHolder
from .names.names import get_full_name
from .taxIdGenerator import TaxIdGenerator


example_holder = IssuingHolder(
    name="Iron Bank S.A.",
    external_id="123",
    tax_id="012.345.678-90",
    tags=[
        "Traveler Employee"
    ],
    rules=[
        {
            "name": "General USD",
            "interval": "day",
            "amount": 100000,
            "currencyCode": "USD"
        }
    ]
)


def generateExampleHoldersJson(n=1):
    holders = []
    for _ in range(n):
        example_holder.name = get_full_name()
        example_holder.external_id = str(randint(1, 999999))
        example_holder.tax_id = TaxIdGenerator.taxId()
        holders.append(deepcopy(example_holder))
    return holders
