#coding: utf-8
from copy import deepcopy
from random import choice
from ..utils.endToEndId import get_end_to_end_id
from starkinfra import PixInfraction, pixinfraction, pixreversal, pixrequest

example_pix_infraction = PixInfraction(
    description="Client payed for an item and never received it.",
    reference_id=get_end_to_end_id()[0],
    tags=["SDK tests", "python SDK"],
    type="fraud",
)


def generateExamplePixInfractionsJson(n=1, infractionType="fraud"):
    infractions = []
    requests = list(pixrequest.query(limit=n, status="success"))
    referenceIds = [request.end_to_end_id for request in requests]

    if infractionType == "reversalChargeback":
        reversals = list(pixreversal.query(limit=n, status="success"))
        referenceIds = [reversal.return_id for reversal in reversals]

    for id in referenceIds:
        infraction = deepcopy(example_pix_infraction)
        infraction.reference_id = id
        infraction.type = infractionType
        infractions.append(infraction)
    return infractions


def getPixInfractionToPatch():
    incfractions = []
    cursor = None
    while len(incfractions) < 1:
        reports, cursor = pixinfraction.page(status="created", limit=5, cursor=cursor)
        for report in reports:
            if report.flow == "out":
                incfractions.append(report)
        if cursor is None:
            break
    return choice(incfractions)
