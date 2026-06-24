# coding=utf-8
from copy import deepcopy
from starkinfra import BusinessIdentity


# A real CNPJ is required: the API looks the company up in the bureau and rejects
# it if no representatives are found, so a randomly generated tax ID would not work.
def _generateBusinessIdentity():
    return BusinessIdentity(
        tax_id="20.018.183/0001-80",
        tags=["test", "testing"],
    )


def generateExampleBusinessIdentityJson(n=1):
    identities = []
    for _ in range(n):
        identities.append(deepcopy(_generateBusinessIdentity()))
    return identities
