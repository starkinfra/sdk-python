from copy import deepcopy
from datetime import datetime, date, timedelta
from starkinfra import CreditHolmes
from tests.utils.date import randomDateBetween
from tests.utils.taxIdGenerator import TaxIdGenerator


def _generateCreditHolmes():
    return CreditHolmes(
        tax_id="012.345.678-90",
        competence=datetime(2022, 10, 1),
    )


def generateExampleCreditHolmesJson(n=1):
    credit_holmes = []
    today = date.today()
    for _ in range(n):
        holmes = deepcopy(_generateCreditHolmes())
        holmes.tax_id = TaxIdGenerator.taxId()
        holmes.competence = randomDateBetween(today - timedelta(days=today.day), today - timedelta(days=365))
        credit_holmes.append(holmes)
    return credit_holmes
