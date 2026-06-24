from copy import deepcopy
from uuid import uuid4
from random import choice, randint
from starkinfra import PixKeyHolmes
from tests.utils.taxIdGenerator import TaxIdGenerator


example_pix_key_holmes = PixKeyHolmes(
    key_id="valid@sandbox.com",
    tags=["test"],
)


def _random_key_id():
    return choice([
        "{}@sandbox.com".format(uuid4().hex[:12]),
        "+55{}".format(randint(10000000000, 99999999999)),
        TaxIdGenerator.taxId(),
    ])


def generateExamplePixKeyHolmesJson(n=1):
    holmes_list = []
    for _ in range(n):
        holmes = deepcopy(example_pix_key_holmes)
        holmes.key_id = _random_key_id()
        holmes.tags = ["test"]
        holmes_list.append(holmes)
    return holmes_list
