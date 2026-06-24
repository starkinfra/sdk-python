from uuid import uuid4
from copy import deepcopy
from datetime import datetime, timezone, timedelta
from random import choice, randint
from starkinfra import PixPullRequest, endtoendid
from ..utils.user import bank_code


example_pix_pull_request = PixPullRequest(
    amount=10000,
    due=datetime.now(timezone.utc) + timedelta(days=2),
    end_to_end_id=endtoendid.create(bank_code),
    receiver_account_number="876543-2",
    receiver_account_type="checking",
    receiver_bank_code=bank_code,
    reconciliation_id="recon-" + str(uuid4())[:8],
    subscription_id="5656565656565656",
    attempt_type="default",
)


def generateExamplePixPullRequestJson(subscription_id="5656565656565656", n=1):
    requests = []
    for _ in range(n):
        request = deepcopy(example_pix_pull_request)
        request.amount = randint(1000, 1000000)
        request.due = datetime.now(timezone.utc) + timedelta(days=randint(1, 30))
        request.end_to_end_id = endtoendid.create(bank_code)
        request.receiver_account_number = "{}-{}".format(randint(10000, 100000000), randint(0, 9))
        request.receiver_account_type = choice(["checking", "savings", "salary", "payment"])
        request.receiver_bank_code = bank_code
        request.reconciliation_id = "recon-" + str(uuid4())[:16]
        request.subscription_id = subscription_id
        request.attempt_type = "default"
        request.description = choice([None, "Test pull request"])
        request.receiver_branch_code = str(randint(1, 9999))
        request.tags = ["test", "pix-pull"]
        requests.append(request)
    return requests
