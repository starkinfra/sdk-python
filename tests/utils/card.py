# coding: utf-8

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
