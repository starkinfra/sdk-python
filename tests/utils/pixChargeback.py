#coding: utf-8
from random import choice
from copy import deepcopy
from ..utils.user import bank_code
from starkinfra import PixChargeback, pixrequest, pixchargeback


example_pix_chargeback = PixChargeback(
    amount=None,
    reference_id=None,
    reason="flaw",
)


def generateExamplePixChargebackJson(n=1):
    pix_requests = pixrequest.query(limit=n)
    chargebacks = []
    for request in pix_requests:
        pix_chargeback = deepcopy(example_pix_chargeback)
        pix_chargeback.amount = request.amount
        pix_chargeback.reference_id = request.end_to_end_id
        chargebacks.append(pix_chargeback)
    return chargebacks


def getPixChargebackToPatch():
    reversal_requests = []
    cursor = None
    while len(reversal_requests) < 3:
        requests, cursor = pixchargeback.page(status="delivered", limit=5, cursor=cursor)
        for request in requests:
            if request.sender_bank_code != bank_code:
                reversal_requests.append(request)
        if cursor is None:
            break
    return choice(reversal_requests)
