from uuid import uuid4
from copy import deepcopy
from datetime import datetime, timezone
from random import randint
from starkinfra import PixPullSubscription
from .names.names import get_full_name
from .taxIdGenerator import TaxIdGenerator
from ..utils.user import bank_code


def _generate_bacen_id():
    now = datetime.now(timezone.utc)
    date_part = now.strftime("%Y%m%d%H%M")
    random_part = str(randint(1000000, 9999999))
    return "RR" + bank_code + date_part + random_part


example_pix_pull_subscription = PixPullSubscription(
    bacen_id=_generate_bacen_id(),
    external_id=str(uuid4()),
    installment_start=datetime.now(timezone.utc),
    interval="month",
    receiver_name="Stark Bank",
    receiver_tax_id="39.908.427/0001-28",
    receiver_bank_code=bank_code,
    reference_code="36135971",
    sender_account_number="876543-2",
    sender_bank_code=bank_code,
    sender_branch_code="1357-9",
    sender_city_code="3550308",
    sender_tax_id="39908427000128",
    sender_final_name="STARK SCD S.A.",
    sender_final_tax_id="39908427000128",
    type="push",
    amount=52064,
    amount_min_limit=1000,
    description="A Lannister always pays his debts",
    pull_retry_limit=3,
    tags=["test", "pix-pull"],
)


def generateExamplePixPullSubscriptionJson(n=1):
    subscriptions = []
    for _ in range(n):
        subscription = deepcopy(example_pix_pull_subscription)
        subscription.bacen_id = _generate_bacen_id()
        subscription.external_id = str(uuid4())
        subscription.installment_start = datetime.now(timezone.utc)
        subscription.interval = "month"
        subscription.receiver_name = get_full_name()
        subscription.receiver_tax_id = TaxIdGenerator.taxId()
        subscription.sender_account_number = "{}-{}".format(randint(10000, 100000000), randint(0, 9))
        subscription.sender_branch_code = "{}-{}".format(randint(1, 9999), randint(0, 9))
        subscription.sender_city_code = "3550308"
        subscription.sender_tax_id = TaxIdGenerator.taxId()
        subscription.type = "push"
        subscription.amount = randint(1000, 1000000)
        subscription.amount_min_limit = randint(100, 999)
        subscription.description = "Test PixPullSubscription"
        subscription.reference_code = str(randint(10000000, 99999999))
        subscription.tags = ["test", "pix-pull"]
        subscriptions.append(subscription)
    return subscriptions
