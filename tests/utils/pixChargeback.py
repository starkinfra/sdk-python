#coding: utf-8
from random import choice, randint
from copy import deepcopy
from ..utils.user import bank_code
from starkinfra import PixChargeback, pixrequest, pixchargeback, pixreversal


example_chargeback = PixChargeback(
    description="Client payed for an item and never received it.",
    tags=["SDK tests", "python SDK"],
    amount=randint(1, 5),
    reference_id=None,
    reason="flaw",
)


def generateExamplePixChargebacksJson(n=1, reason=None):
    if not reason:
        reason = choice(["flaw", "fraud", "reversalChargeback"])

    chargebacks = []
    cursor = None
    if reason == "reversalChargeback":
        while True:
            reversals, cursor = pixreversal.page(limit=100, status="success", cursor=cursor)
            referenceIds = [reversal.return_id for reversal in reversals]
            chargebacks = setChargebackInfo(
                transactions=reversals,
                reason=reason,
                chargebacks=chargebacks,
                referenceIds=referenceIds
            )
            if cursor is None:
                break
            if len(chargebacks) < n:
                continue
            break

    if reason != "reversalChargeback":
        while True:
            requests, cursor = pixrequest.page(limit=100, status="success", cursor=cursor)
            referenceIds = [request.end_to_end_id for request in requests]
            chargebacks = setChargebackInfo(
                transactions=requests,
                reason=reason,
                chargebacks=chargebacks,
                referenceIds=referenceIds
            )
            if cursor is None:
                break
            if len(chargebacks) < n:
                continue
            break

    if len(chargebacks) > n:
        chargebacks = chargebacks[:n]
    if not chargebacks:
        raise Exception("No inbound Pix transactions for a PicChargeback of reason {}".format(reason))
    return chargebacks


def setChargebackInfo(transactions, reason, chargebacks, referenceIds):
    elements = [list(element) for element in zip(referenceIds, transactions)]

    for referenceId, transaction in elements:
        if transaction.flow == "out":
            chargeback = deepcopy(example_chargeback)
            chargeback.amount = transaction.amount
            chargeback.reference_id = referenceId
            chargeback.reason = reason
            chargebacks.append(chargeback)
    return chargebacks


def getPixChargebackToPatch():
    allChargebacks = []
    cursor = None
    while len(allChargebacks) < 3:
        chargebacks, cursor = pixchargeback.page(status="delivered", limit=5, cursor=cursor)
        for chargeback in chargebacks:
            if chargeback.sender_bank_code != bank_code:
                allChargebacks.append(chargeback)
        if cursor is None:
            break
    return choice(allChargebacks)
