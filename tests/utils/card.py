# coding: utf-8
from copy import deepcopy
from starkinfra import IssuingCard


example_card = IssuingCard(
    holder_name="",
    holder_tax_id="",
    holder_external_id="",
)


def generateExampleCardsJson(holder, n=1):
    cards = []
    for _ in range(n):
        example_card.holder_name = holder.name
        example_card.holder_tax_id = holder.tax_id
        example_card.holder_external_id = holder.external_id
        cards.append(deepcopy(example_card))
    return cards
