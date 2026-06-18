# coding=utf-8
from copy import deepcopy
from random import randint
from starkinfra import IndividualAccountRequest
from starkinfra.individualaccountrequest import Address
from .names.names import get_full_name
from .taxIdGenerator import TaxIdGenerator


def _generateExampleAddress():
    return Address(
        street="Rua do Estilo Barroco",
        number="648",
        neighborhood="Santo Amaro",
        city="Sao Paulo",
        state="SP",
        zip_code="05724005",
    )


def _generateIndividualAccountRequest():
    return IndividualAccountRequest(
        name="Jamie Lannister",
        tax_id="012.345.678-90",
        address=_generateExampleAddress(),
        income=1000000,
        birth_date="2012-03-06",
        tags=["test", "testing"],
    )


def generateExampleIndividualAccountRequestJson(n=1):
    requests = []
    for _ in range(n):
        request = deepcopy(_generateIndividualAccountRequest())

        request.name = get_full_name()
        request.tax_id = TaxIdGenerator.cpf()
        request.income = randint(100000, 10000000)
        request.address = _generateExampleAddress()

        requests.append(request)
    return requests
