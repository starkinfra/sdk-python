import random
import starkinfra
from starkinfra import DynamicBrcode


example_dynamic_brcode = DynamicBrcode(
    name="Jamie Lannister",
    city="Rio de Janeiro",
    external_id="01",
    type="instant"
)


def generate_example_dynamic_brcode_json(type = None):
    example_dynamic_brcode.type = random.choice(["instant", "due"])
    example_dynamic_brcode.external_id = str(random.randint(1, 1000000))
    return example_dynamic_brcode

def create_dynamic_brcode_by_type(type = None):
    example_dynamic_brcode.type = type
    if type is None:
        type = random.choice(["instant", "due", "subscription", "subscriptionAndInstant", "dueAndOrSubscription"])
    example_dynamic_brcode.external_id = str(random.randint(1, 1000000))
    dynamic_brcode = starkinfra.dynamicbrcode.create(
        brcodes=[example_dynamic_brcode]
    )
    return dynamic_brcode[0]