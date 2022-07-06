import random
from starkinfra import DynamicBrcode


example_dynamic_brcode = DynamicBrcode(
    name="Jamie Lannister",
    city="Rio de Janeiro",
    external_id="01",
    type="instant"
)


def generateExampleDynamicBrcodeJson():
    example_dynamic_brcode.type = random.choice(["instant", "due"])
    example_dynamic_brcode.external_id = str(random.randint(1, 100000))
    return example_dynamic_brcode
