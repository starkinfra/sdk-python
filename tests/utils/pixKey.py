#coding: utf-8
from copy import deepcopy
from random import randint, choice
from starkinfra import PixKey
from .names.names import get_full_name
from ..utils.date import randomPastDate
from .taxIdGenerator import TaxIdGenerator


example_pix_key = PixKey(
    tags=["SDK tests", "python SDK"],
    account_created=randomPastDate(days=360),
    account_number=str(randint(10000000, 99999999)),
    account_type="savings",
    branch_code=str(randint(1000, 9999)),
    name=get_full_name(),
    tax_id=TaxIdGenerator.taxId()
)


def generateExamplePixKeyJson(keyType=None):
    if not keyType:
        choice(["phone", "email", "cpf", "cnpj", "evp"])
    key = deepcopy(example_pix_key)

    if keyType == "phone":
        key.id = "+55{area_code}{phone_number}".format(
            area_code=randint(10, 99),
            phone_number=randint(100000000, 999999999)
        )

    if keyType == "email":
        key.id = "emailTesteApi{random}@hotmail.com".format(
            random=randint(0, 99999999999)
        )

    if keyType == "cpf":
        key.id = TaxIdGenerator.cpf()
        key.tax_id = key.id
    if keyType == "cnpj":
        key.id = TaxIdGenerator.cnpj()
        key.tax_id = key.id

    return key
