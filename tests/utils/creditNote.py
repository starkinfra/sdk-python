# coding=utf-8
from uuid import uuid4
from copy import deepcopy
from random import randint, choice
from datetime import timedelta, datetime
from .user import template_id
from .names.names import get_full_name
from .taxIdGenerator import TaxIdGenerator
from .date import randomDatetimeBetween, randomFutureDatetime
from starkinfra import CreditNote
from starkinfra.creditsigner import CreditSigner
from starkinfra.creditnote import Invoice, Transfer, Description


def _generateCreditNote():
    return CreditNote(
        template_id=template_id,
        name="Jamie Lannister",
        tax_id="012.345.678-90",
        nominal_amount=100000,
        scheduled="2022-04-28",
        invoices=[
            Invoice(
                due="2023-06-25",
                amount=120000,
            )
        ],
        tags=["test", "testing"],
        payment=_generate_payment(),
        signers=[
            CreditSigner(
                name="Jamie Lannister",
                contact="jamie.lannister@gmail.com",
                method="link"
            )
        ],
        external_id="1234",
        street_line_1="Rua ABC",
        street_line_2="Ap 123",
        district="Jardim Paulista",
        city="São Paulo",
        state_code="SP",
        zip_code="01234-567",
    )


def _generate_payment(payment_type="transfer"):
    return {
        "transfer": _generateTransfer(),
    }[payment_type]


def _generateTransfer():
    return Transfer(
        bank_code="00000000",
        branch_code="1234",
        account_number="129340-1",
        name="Jamie Lannister",
        tax_id="012.345.678-90",
    )


def generateExampleCreditNoteJson(n=1, nominal_amount=None):
    credit_notes = []
    for _ in range(n):
        note = deepcopy(_generateCreditNote())

        note.name = get_full_name()
        note.tax_id = TaxIdGenerator.taxId()

        note_nominal_amount = randint(100000, 1000000)
        if nominal_amount is not None:
            note_nominal_amount = int(nominal_amount)

        note.nominal_amount = note_nominal_amount
        note.scheduled = randomFutureDatetime(days=600)

        note.invoices = generateExampleInvoiceJson(n=randint(3, 4), note_nominal_amount=note.nominal_amount // 2,
                                                   note_scheduled=note.scheduled)
        note.signers = generateExampleSignersJson(n=randint(1, 3))

        note.payment = Transfer(
            bank_code=choice(["18236120", "60701190"]),
            branch_code="{:04}".format(randint(1, 10 ** 4)),
            account_number="{:07}".format(randint(1, 10 ** 7)),
            name=get_full_name(),
            tax_id=TaxIdGenerator.taxId(),
        )
        note.payment_type = "transfer"

        note.external_id = str(uuid4())

        credit_notes.append(note)
    return credit_notes


def generateExampleInvoiceJson(n=1, note_nominal_amount=0, note_scheduled=datetime.now()):
    invoices = []

    for _ in range(n):
        invoices.append(Invoice(
            due=randomDatetimeBetween(note_scheduled + timedelta(days=500), note_scheduled + timedelta(days=1000)),
            amount=randint(note_nominal_amount, note_nominal_amount + 100000),
            descriptions=[Description(key="taxes", value="RS1000")],
        ))

    return invoices


def generateExampleSignersJson(n=1):
    signers = []

    for _ in range(n):
        name = get_full_name()
        signers.append(CreditSigner(
            name=get_full_name(),
            contact="{name}.{lastName}.{uuid}@invaliddomain.com".format(
                name=name.split(" ")[0].lower(),
                lastName=name.split(" ")[1].lower(),
                uuid=str(uuid4())
            ),
            method="link"
        ))

    return signers
