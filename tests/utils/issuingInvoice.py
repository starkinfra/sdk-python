from random import randint
from starkinfra import IssuingInvoice


example_invoice = IssuingInvoice(
    amount=1000,
)


def generateExampleInvoicesJson():
    example_invoice.amount = randint(1, 1000)
    return example_invoice
