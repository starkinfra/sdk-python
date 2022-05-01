from uuid import uuid4
from copy import deepcopy
from ..utils.user import bank_code
from starkinfra import PixRequest, endtoendid
from random import randint, choice
from .names.names import get_full_name
from .taxIdGenerator import TaxIdGenerator


example_pix_request = PixRequest(
    amount=10,
    external_id=str(uuid4()),
    sender_account_number="00000-0",
    sender_branch_code="0000",
    sender_account_type="checking",
    sender_name="Joao",
    sender_tax_id="01234567890",
    receiver_bank_code="00000000",
    receiver_account_number="00000-1",
    receiver_branch_code="0001",
    receiver_account_type="checking",
    receiver_name="maria",
    receiver_tax_id="01234567890",
    end_to_end_id=endtoendid.create(bank_code),
)


def generateExamplePixRequestJson(n=1):
    pix_requests = []
    for _ in range(n):
        amount = randint(100000, 1000000)
        pix_request = deepcopy(example_pix_request)
        pix_request.amount = amount
        pix_request.external_id = str(uuid4())
        pix_request.sender_name = get_full_name()
        pix_request.sender_tax_id = TaxIdGenerator.taxId()
        pix_request.sender_branch_code = str(randint(1, 999))
        pix_request.sender_account_number = "{}-{}".format(randint(10000, 100000000), randint(0, 9))
        pix_request.sender_account_type = choice(["checking", "savings", "salary", "payment"])
        pix_request.receiver_name = get_full_name()
        pix_request.receiver_tax_id = TaxIdGenerator.taxId()
        pix_request.receiver_bank_code = choice(["18236120", "60701190", "00000000"])
        pix_request.receiver_account_number = "{}-{}".format(randint(10000, 100000000), randint(0, 9))
        pix_request.receiver_branch_code = str(randint(1, 999))
        pix_request.receiver_account_type = choice(["checking", "savings", "salary", "payment"])
        pix_request.end_to_end_id = endtoendid.create(bank_code)
        pix_request.description = choice([None, "Test description"])
        pix_request.initiator_tax_id = TaxIdGenerator.taxId()
        pix_request.cash_amount = randint(1000, 10000)
        pix_request.cashier_bank_code = choice(["18236120", "60701190", "00000000"])
        pix_request.cashier_type = choice(["merchant", "other", "participant"])
        pix_request.tags = [choice(["little", "girl", "no", "one"]), choice(["little", "girl", "no", "one"])]
        pix_requests.append(pix_request)
    return pix_requests
