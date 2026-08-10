# coding=utf-8
from copy import deepcopy
from random import randint, choice
from starkinfra import BusinessAccountRequest
from starkinfra.businessaccountrequest import Address, Owner
from .names.names import get_full_name
from .taxIdGenerator import TaxIdGenerator


def _generateExampleAddress():
    return Address(
        street="Av. Faria Lima",
        number="2000",
        neighborhood="Itaim Bibi",
        city="Sao Paulo",
        state="SP",
        zip_code="04538-132",
        complement="Sala 42",
    )


def _generateExampleOwners(n=2):
    return [
        Owner(
            tax_id=TaxIdGenerator.cpf(),
            name=get_full_name(),
            role=choice(["partner", "representative"]),
        )
        for _ in range(n)
    ]


def _generateBusinessAccountRequest():
    return BusinessAccountRequest(
        address=_generateExampleAddress(),
        revenue=100000000,
        name="Stark Bank S.A.",
        tax_id=TaxIdGenerator.cnpj(),
        owners=_generateExampleOwners(),
        tags=["test", "testing"],
    )


def generateExampleBusinessAccountRequestJson(n=1):
    requests = []
    for _ in range(n):
        request = deepcopy(_generateBusinessAccountRequest())

        request.name = "{name} S.A.".format(name=get_full_name())
        request.tax_id = TaxIdGenerator.cnpj()
        request.revenue = randint(10000000, 1000000000)
        request.address = _generateExampleAddress()
        request.owners = _generateExampleOwners(n=randint(1, 3))

        requests.append(request)
    return requests
