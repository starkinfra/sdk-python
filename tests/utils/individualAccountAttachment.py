# coding=utf-8
from starkinfra import IndividualAccountAttachment
from .individualDocument import readImage, RgImages


def generateExampleIndividualAccountAttachmentJson(account_request_id, n=1):
    attachments = []
    for _ in range(n):
        attachments.append(IndividualAccountAttachment(
            content=readImage(RgImages["front"]),
            content_type="image/png",
            type="identity-front",
            account_request_id=account_request_id,
            tags=["test", "testing"],
        ))
    return attachments
