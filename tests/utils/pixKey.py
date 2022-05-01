#coding: utf-8
from copy import deepcopy
from random import randint
from starkinfra import PixKey
from .names.names import get_full_name
from ..utils.date import randomPastDate
from .taxIdGenerator import TaxIdGenerator


example_pix_key = PixKey(
    account_created="2022-03-01",
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
    pix_key.id = "+55{area_code}{phone_number}".format(
        area_code=randint(10, 99),
        phone_number=randint(100000000, 999999999)
    )
    pix_key.tax_id = TaxIdGenerator.taxId()
    pix_key.account_created = randomPastDate(days=360)
    return pix_key
