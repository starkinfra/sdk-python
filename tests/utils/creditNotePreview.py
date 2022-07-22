from random import randint, choice, uniform, random
from .taxIdGenerator import TaxIdGenerator
from .date import randomFutureDatetime, futureDate
from starkinfra.creditpreview import CreditNotePreview
from starkinfra.creditnote import Invoice


def _choiceBetween(option):
    if random() < 0.5:
        return None
    return option


def _generateInvoice(days=None, amount=100):
    return Invoice(
        amount=amount,
        due=randomFutureDatetime(days=days or randint(1, 90))
    )


def _generateInvoicePreview(n=1, amount=randint(1, 100000)):
    return [_generateInvoice(days=(i + 1) * 30, amount=int(amount / n)) for i in range(n)]


def generateSacPreview():
    return CreditNotePreview(
        tax_id=TaxIdGenerator.taxId(),
        type="sac",
        nominal_amount=randint(1, 100000),
        rebate_amount=_choiceBetween(randint(1, 1000)),
        nominal_interest=uniform(0, 4.99),
        scheduled=futureDate(days=randint(11, 20)),
        initial_due=futureDate(days=randint(30, 40)),
        initial_amount=randint(1, 9999),
        interval=_choiceBetween(choice(["month", "year"]))
    )


def generatePricePreview():
    return CreditNotePreview(
        tax_id=TaxIdGenerator.taxId(),
        type="price",
        nominal_amount=randint(1, 100000),
        rebate_amount=_choiceBetween(randint(1, 1000)),
        nominal_interest=uniform(0, 4.99),
        scheduled=futureDate(days=randint(11, 20)),
        initial_due=futureDate(days=randint(30, 40)),
        initial_amount=randint(1, 9999),
        interval=_choiceBetween(choice(["month", "year"]))
    )


def generateAmericanPreview():
    return CreditNotePreview(
        tax_id=TaxIdGenerator.taxId(),
        type="american",
        nominal_amount=randint(1, 100000),
        rebate_amount=_choiceBetween(randint(1, 1000)),
        nominal_interest=uniform(0, 4.99),
        scheduled=futureDate(days=randint(11, 20)),
        initial_due=futureDate(days=randint(30, 40)),
        count=randint(1, 12),
        interval=_choiceBetween(choice(["month", "year"]))
    )


def generateBulletPreview():
    return CreditNotePreview(
        tax_id=TaxIdGenerator.taxId(),
        type="bullet",
        nominal_amount=randint(1, 100000),
        rebate_amount=_choiceBetween(randint(1, 1000)),
        nominal_interest=uniform(0, 4.99),
        scheduled=futureDate(days=randint(11, 20)),
        initial_due=futureDate(days=randint(30, 40)),
    )


def generateCustomPreview():
    amount = randint(1, 100000)
    return CreditNotePreview(
        tax_id=TaxIdGenerator.taxId(),
        type="custom",
        nominal_amount=amount,
        scheduled=futureDate(days=randint(1, 90)),
        rebate_amount=_choiceBetween(randint(1, 1000)),
        invoices=_generateInvoicePreview(n=randint(1, 12), amount=amount),
    )


def generateRandomPreview():
    return choice([
        generateSacPreview(),
        generatePricePreview(),
        generateAmericanPreview(),
        generateBulletPreview(),
        generateCustomPreview()
    ])


_generatorsByType = {
    'sac': generateSacPreview,
    'price': generatePricePreview,
    'american': generateAmericanPreview,
    'bullet': generateBulletPreview,
    'custom': generateCustomPreview,
}


def getCreditNotePreviewExample(type="sac"):
    return _generatorsByType[type]()


def getCreditNotePreviewExamples(n=10, type="sac"):
    return [_generatorsByType[type]() for _ in range(n)]
