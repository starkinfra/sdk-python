from copy import deepcopy
import starkinfra
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


def generateExampleCardsWithoutHolderJson(n=1, type="physical", product_id=None):
    # The sandbox product ids differ per Project, so the first available product is used by default.
    product_id = product_id or next(starkinfra.issuingproduct.query(limit=1)).id
    return [IssuingCard(product_id=product_id, type=type, tags=["sdk-test"]) for _ in range(n)]


def findExistingHolderForProduct(product):
    # A holder can only be linked to a product of its own type: business holders have a CNPJ (14 digits) and
    # individual holders a CPF (11 digits). Existing holders are used so no personal data is created by the test.
    digits = {"business": 14, "individual": 11}[product.holder_type]
    for holder in starkinfra.issuingholder.query(status="active", limit=100):
        if len("".join(char for char in holder.tax_id if char.isdigit())) == digits:
            return holder
    return None
