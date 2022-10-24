#coding: utf-8
from copy import deepcopy
from datetime import datetime
from random import randint, choice
from starkinfra import PixClaim, pixclaim
from .names.names import get_full_name
from .taxIdGenerator import TaxIdGenerator
from .pixKey import generateExamplePixKeyJson


example_pix_claim = PixClaim(
    tags=["SDK tests", "python SDK"],
    account_created=datetime.utcnow(),
    account_number=str(randint(100000, 9999999)),
    account_type=choice(["checking", "savings", "salary", "payment"]),
    branch_code=str(randint(1000, 9999)),
    name=get_full_name(),
    tax_id=TaxIdGenerator.taxId(),
    key_id="+55{area_code}{phone_number}".format(
        area_code=randint(10, 99),
        phone_number=randint(100000000, 999999999)
    ),
)


def generateExamplePixClaimJson(key=None, claimType="portability"):
    claim = deepcopy(example_pix_claim)
    if not key:
        keyType = choice(["phone", "email", "cpf", "cnpj"])
        key = generateExamplePixKeyJson(keyType=keyType)
        claim.key_id = key.id
        return claim

    claim.key_id = key.id
    if claimType == "portability":
        claim.tax_id = key.tax_id
    return claim


def keyTypeFromType(type):
    if type == "ownership":
        return choice(["phone", "email"])
    return choice(["phone", "email", "cpf", "cnpj"])


def getPixClaimToPatch():
    pix_claims = []
    cursor = None
    while len(pix_claims) < 1:
        claims, cursor = pixclaim.page(status="delivered", limit=5, cursor=cursor)
        for claim in claims:
            if claim.agent == "claimer":
                pix_claims.append(claim)
        if cursor is None:
            break
    return choice(pix_claims)
