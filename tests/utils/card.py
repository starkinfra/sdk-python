from copy import deepcopy
from starkinfra import IssuingCard
from .rule import generateExampleRuleJson


example_card = IssuingCard(
    holder_name="",
    holder_tax_id="",
    holder_external_id="",
)


def generateExampleCardsJson(holder, n=1, type=None, product_id=None):
    cards = []
    for _ in range(n):
        if product_id:
            example_card.product_id = product_id
        example_card.holder_name = holder.name
        example_card.holder_tax_id = holder.tax_id
        example_card.holder_external_id = holder.external_id
        if type:
            example_card.type = type
        example_card.rules = generateExampleRuleJson()
        cards.append(deepcopy(example_card))
    return cards
