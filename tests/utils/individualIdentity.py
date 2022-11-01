# coding=utf-8
from copy import deepcopy
from .names.names import get_full_name
from .taxIdGenerator import TaxIdGenerator
from starkinfra import IndividualIdentity


def _generateIndividualIdentity():
    return IndividualIdentity(
        name="Jamie Lannister",
        tax_id="012.345.678-90",
        tags=["test", "testing"],
    )


def generateExampleIndividualIdentityJson(n=1):
    identities_identity = []
    for _ in range(n):
        individual = deepcopy(_generateIndividualIdentity())

        individual.name = get_full_name()
        individual.tax_id = TaxIdGenerator.cpf()

        identities_identity.append(individual)
    return identities_identity

