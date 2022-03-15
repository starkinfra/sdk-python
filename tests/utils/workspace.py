import starkinfra
from uuid import uuid4
from .taxIdGenerator import TaxIdGenerator


def generateExampleWorkspace():
    id = uuid4()
    return starkinfra.Workspace(
        username="starkv2-{id}".format(id=id),
        name="Stark V2: {id}".format(id=id),
        allowed_tax_ids=[TaxIdGenerator.cpf(), TaxIdGenerator.cnpj()],
    )
