from random import randint, choice
from starkinfra import PixInternalTransactionReport, endtoendid, returnid
from .user import bank_code
from .date import randomPastDatetime
from .taxIdGenerator import TaxIdGenerator


def generateExamplePixInternalTransactionReportJson(n=1):
    reports = []
    for _ in range(n):
        reference_type = choice(["request", "reversal"])
        report = PixInternalTransactionReport(
            amount=randint(100, 1000000),
            created=randomPastDatetime(days=30),
            end_to_end_id=endtoendid.create(bank_code),
            method="manual",
            reference_type=reference_type,
            sender_account_number=str(randint(10000, 99999999)),
            sender_branch_code=str(randint(1, 999)),
            sender_account_type=choice(["checking", "savings", "salary", "payment"]),
            sender_bank_code=str(bank_code),
            sender_tax_id=TaxIdGenerator.taxId(),
            receiver_account_number=str(randint(10000, 99999999)),
            receiver_branch_code=str(randint(1, 999)),
            receiver_account_type=choice(["checking", "savings", "salary", "payment"]),
            receiver_bank_code=choice(["18236120", "60701190", "20018183"]),
            receiver_tax_id=TaxIdGenerator.taxId(),
            return_id=returnid.create(bank_code) if reference_type == "reversal" else None,
        )
        reports.append(report)
    return reports
