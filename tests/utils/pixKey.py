#coding: utf-8
from copy import deepcopy
from random import randint
from starkinfra import PixKey
from .names.names import get_full_name
from ..utils.date import randomPastDate
from .taxIdGenerator import TaxIdGenerator


example_pix_key = PixKey(
    account_created="2022-03-01T00:00:00.20+00:00",
    account_number="0000",
    account_type="savings",
    branch_code="0000",
    name="Jamie Lannister",
    tax_id="012.345.678-90"
)


def generateExamplePixKeyJson():
    pix_key = deepcopy(example_pix_key)
    pix_key.name = get_full_name()
    pix_key.account_number = str(randint(10000000, 99999999))
    pix_key.branch_code = str(randint(1000, 9999))
    pix_key.id = f"+55{randint(100, 999)}{randint(10000000, 99999999)}"
    pix_key.tax_id = TaxIdGenerator.taxId()
    pix_key.account_created = randomPastDate(days=360)
    return pix_key
