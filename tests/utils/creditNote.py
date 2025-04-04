# coding=utf-8
from uuid import uuid4
from datetime import datetime
from random import randint, choice
from datetime import timedelta, datetime, date
from .user import template_id
from .names.names import get_full_name
from .taxIdGenerator import TaxIdGenerator
from .date import futureDateTime, randomDateBetween, randomDatetimeBetween, randomFutureDate, randomFutureDatetime
from starkinfra import CreditNote
from starkinfra.creditsigner import CreditSigner
from starkinfra.creditnote import Invoice, Transfer, Description


def _generateCreditNote():
    scheduled = futureDateTime(days=1)
    nominal_amount = randint(100000, 1000000)
    invoice_nominal_amount = nominal_amount // 2

    return CreditNote(
        template_id=template_id,
        name=get_full_name(),
        tax_id=TaxIdGenerator.taxId(),
        nominal_amount=nominal_amount,
        scheduled=datetime.strftime(scheduled, "%Y-%m-%d"),
        expiration=timedelta(days=1),
        invoices=generateExampleInvoiceStringDateJson(n=randint(3, 4), note_nominal_amount=invoice_nominal_amount,
                                                     note_scheduled=scheduled),
        tags=["test", "testing"],
        payment=Transfer(
            bank_code=choice(["18236120", "60701190"]),
            branch_code="{:04}".format(randint(1, 10 ** 4)),
            account_number="{:07}".format(randint(1, 10 ** 7)),
            name=get_full_name(),
            tax_id=TaxIdGenerator.taxId(),
        ),
        payment_type="transfer",
        signers=generateExampleSignersJson(n=randint(1, 3)),
        external_id=str(uuid4()),
        street_line_1="Rua ABC",
        street_line_2="Ap 123",
        district="Jardim Paulista",
        city="São Paulo",
        state_code="SP",
        zip_code="01234-567",
    )


def generateExampleCreditNoteJson(n=1, nominal_amount=None):
    credit_notes = []
    for _ in range(n):
        note = _generateCreditNote()

        note_nominal_amount = randint(100000, 1000000)
        if nominal_amount is not None:
            note_nominal_amount = int(nominal_amount)

        note.nominal_amount = note_nominal_amount
        note.scheduled = randomFutureDate(days=600)

        note.invoices = generateExampleInvoiceJson(n=randint(3, 4), note_nominal_amount=note.nominal_amount // 2,
                                                   note_scheduled=note.scheduled)
        credit_notes.append(note)
    return credit_notes

def generateExampleCreditNoteIsoDatetimeJson(n=1, nominal_amount=None):
    credit_notes = []
    for _ in range(n):
        note = _generateCreditNote()

        note_nominal_amount = randint(100000, 1000000)
        if nominal_amount is not None:
            note_nominal_amount = int(nominal_amount)

        note.nominal_amount = note_nominal_amount

        note.scheduled = randomFutureDatetime(days=600)
        note.invoices = generateExampleInvoiceDatetimeJson(n=randint(3, 4), note_nominal_amount=note.nominal_amount // 2,
                                                   note_scheduled=note.scheduled)

        credit_notes.append(note)
    return credit_notes

def generateExampleCreditNoteStringDatesJson(n=1, nominal_amount=None):
    """
    Generate a list of credit notes with string dates.
    Note: This function does not overwrite `schedule` and `Invoice.due` 
    dates in the CreditNote object.
    """
    credit_notes = []
    for _ in range(n):
        note = _generateCreditNote()

        credit_notes.append(note)
    return credit_notes


def generateExampleInvoiceJson(n=1, note_nominal_amount=0, note_scheduled=date.today()):
    invoices = []

    for _ in range(n):
        invoices.append(Invoice(
            due=randomDateBetween(note_scheduled + timedelta(days=500), note_scheduled + timedelta(days=1000)),
            amount=randint(note_nominal_amount, note_nominal_amount + 100000),
            descriptions=[Description(key="taxes", value="RS1000")],
        ))

    return invoices


def generateExampleInvoiceStringDateJson(n=1, note_nominal_amount=0, note_scheduled=datetime.now()):
    invoices = []

    for _ in range(n):
        date = randomDatetimeBetween(note_scheduled + timedelta(days=500), note_scheduled + timedelta(days=1000))
        invoices.append(Invoice(
            due=datetime.strftime(date, "%Y-%m-%d"),
            amount=randint(note_nominal_amount, note_nominal_amount + 100000),
            descriptions=[Description(key="taxes", value="RS1000")],
        ))

    return invoices


def generateExampleInvoiceDatetimeJson(n=1, note_nominal_amount=0, note_scheduled=datetime.now()):
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
