#coding: utf-8
from random import choice
from copy import deepcopy
from ..utils.user import bank_code
from starkinfra import ReversalRequest, pixrequest, reversalrequest


example_reversal_request = ReversalRequest(
    amount=None,
    reference_id=None,
    reason="flaw",
)


def generateExampleReversalRequestJson():
    pix_requests = pixrequest.query(limit=20)
    requests = []
    for request in pix_requests:
        requests.append(request)
    pix_request = choice(requests)
    reversal_request = deepcopy(example_reversal_request)
    reversal_request.amount = pix_request.amount
    reversal_request.reference_id = pix_request.end_to_end_id
    return reversal_request


def getReversalRequestToPatch():
    reversal_requests = []
    cursor = None
    while len(reversal_requests) < 3:
        requests, cursor = reversalrequest.page(status="delivered", limit=5, cursor=cursor)
        for request in requests:
            if request.sender_bank_code != bank_code:
                reversal_requests.append(request)
        if cursor is None:
            break
    return choice(reversal_requests)
