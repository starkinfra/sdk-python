#coding: utf-8
from copy import deepcopy
from random import randint, choice
from starkinfra import PixClaim, pixclaim
from .names.names import get_full_name
from .taxIdGenerator import TaxIdGenerator


example_pix_claim = PixClaim(
    account_created="2022-02-01T00:00:00.00",
    account_number="0000-1",
    account_type="savings",
    branch_code="0000-1",
    name="Jamie Lannister",
    tax_id="012.345.678-90",
    key_id=f"+55{randint(100, 999)}{randint(10000000, 99999999)}"
)


def generateExamplePixClaimJson():
    pix_claim = deepcopy(example_pix_claim)
    pix_claim.name = get_full_name()
    pix_claim.tax_id = TaxIdGenerator.taxId()
    return pix_claim


def getPicClaimToPatch():
    pix_claims = []
    cursor = None
    while len(pix_claims) < 1:
        claims, cursor = pixclaim.page(status="created", limit=5, cursor=cursor)
        for claim in claims:
            if claim.agent == "claimed":
                pix_claims.append(claim)
        if cursor is None:
            break
    return choice(pix_claims)
