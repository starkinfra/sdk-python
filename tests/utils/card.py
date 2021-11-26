# coding: utf-8
from copy import deepcopy
from random import randint
from starkinfra import IssuingCard
from .names.names import get_full_name
from .taxIdGenerator import TaxIdGenerator


example_card = {
    "holderName": "",
    "holderTaxId": "",
    "holderExternalId": ""
}


def generateExampleCardsJson(holder, n=1):
    cards = []
    for _ in range(n):
        example_card["holderName"] = holder.name
        example_card["holderTaxId"] = holder.tax_id
        example_card["holderExternalId"] = holder.external_id
        cards.append(example_card)
    return cards
