# coding=utf-8
from copy import deepcopy
from .names.names import get_full_name
from .taxIdGenerator import TaxIdGenerator
from starkinfra import IndividualAccountRequest


def _generateIndividualAccountRequest():
    return IndividualAccountRequest(
        name="Jamie Lannister",
        tax_id="012.345.678-90",
        address="Rua das Flores, 123",
        income=1000000,
        tags=["test", "testing"],
    )


def generateExampleIndividualAccountRequestJson(n=1):
    requests = []
    for _ in range(n):
        request = deepcopy(_generateIndividualAccountRequest())

        request.name = get_full_name()
        request.tax_id = TaxIdGenerator.cpf()

        requests.append(request)
    return requests
