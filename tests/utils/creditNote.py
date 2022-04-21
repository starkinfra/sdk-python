from uuid import uuid4
from copy import deepcopy
from random import randint, choice
from datetime import timedelta, datetime
from starkinfra import CreditNote
from .names.names import get_full_name
from .taxIdGenerator import TaxIdGenerator
from .date import randomDatetimeBetween, randomFutureDatetime


example_note = CreditNote(
    template_id="5745297539989504",
    name="Jamie Lannister",
    tax_id="012.345.678-90",
    nominal_amount=100000,
    scheduled="2022-04-28",
    invoices=[
        {
            "due": "2023-06-25",
            "amount": 120000,
            "fine": 10,
            "interest": 2
        }
    ],
    tags=["test", "testing"],
    transfer={
        "bank_code": "00000000",
        "branch_code": "1234",
        "account_number": "129340-1",
        "name": "Jamie Lannister",
        "taxId": "012.345.678-90"
    },
    signers=[
        {
            "name": "Jamie Lannister",
            "contact": "jamie.lannister@gmail.com",
            "method": "link"
        }
    ],
)

example_invoice = {
    "due": "2023-06-25",
    "amount": 60000,
    "fine": 10,
    "interest": 2
}

example_signer = {
    "name": "Jamie Lannister",
    "contact": "jamie.lannister@gmail.com",
    "method": "link"
}


def generateExampleCreditNoteJson(n=1, nominal_amount=None):
    credit_notes = []
    for _ in range(n):
        note = deepcopy(example_note)

        note.name = get_full_name()
        note.tax_id = TaxIdGenerator.taxId()

        note_nominal_amount = randint(100000, 1000000)
        if nominal_amount is not None:
            note_nominal_amount = int(nominal_amount)

        note.nominal_amount = note_nominal_amount
        note.scheduled = randomFutureDatetime(days=600)

        note.invoices = generateExampleInvoiceJson(n=randint(3, 4), noteNominalAmount=note.nominal_amount // 2, noteScheduled=note.scheduled)

        note.transfer["bank_code"] = choice(["18236120", "60701190"])
        note.transfer["branch_code"] = "{:04}".format(randint(1, 10**4))
        note.transfer["account_number"] = "{:07}".format(randint(1, 10**7))
        note.transfer["name"] = get_full_name()
        note.transfer["tax_id"] = TaxIdGenerator.taxId()

        note.signers = generateExampleSignersJson(n=randint(1, 3))

        note.external_id = str(uuid4())

        credit_notes.append(note)
    return credit_notes


def generateExampleInvoiceJson(n=1, noteNominalAmount=0, noteScheduled=datetime.now()):
    invoices = []

    for _ in range(n):
        invoice = deepcopy(example_invoice)

        invoice["due"] = randomDatetimeBetween(noteScheduled + timedelta(days=500), noteScheduled + timedelta(days=1000))
        invoice["amount"] = randint(noteNominalAmount, noteNominalAmount+100000)
        invoice["fine"] = randint(0, 20)
        invoice["interest"] = randint(0, 20)

        invoices.append(invoice)
    return invoices


def generateExampleSignersJson(n=1):
    signers = []

    for _ in range(n):
        signer = deepcopy(example_signer)

        signer["name"] = get_full_name()
        signer["contact"] = "{name}.{lastName}.{uuid}@invaliddomain.com".format(
            name=signer["name"].split(" ")[0].lower(),
            lastName=signer["name"].split(" ")[1].lower(),
            uuid=str(uuid4())
        )

        signers.append(signer)

    return signers



