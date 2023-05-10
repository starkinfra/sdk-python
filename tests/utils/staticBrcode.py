from random import randint, choice
from starkinfra import StaticBrcode


example_static_brcode = StaticBrcode(
    name="Jamie Lannister",
    key_id="+5511988887777",
    cashier_bank_code="20018183",
    amount=0,
    reconciliation_id="123",
    city="São Paulo",
    description="A Static Brcode"
)


def generateExampleStaticBrcodeJson():
    example_static_brcode.amount = choice([randint(0, 10), None])
    example_static_brcode.reconciliation_id = str(randint(100, 999))
    example_static_brcode.key_id = "+55{area_code}{phone_number}".format(
        area_code=randint(10, 99),
        phone_number=randint(100000000, 999999999)
    )
    return example_static_brcode
