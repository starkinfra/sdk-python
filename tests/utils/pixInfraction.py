#coding: utf-8
from copy import deepcopy
from random import choice
from ..utils.endToEndId import get_end_to_end_id
from starkinfra import PixInfraction, pixinfraction


example_pix_infraction = PixInfraction(
    reference_id=get_end_to_end_id()[0],
    type="fraud",
)


def generateExamplePixInfractionsJson(n=1):
    pix_infractions = []
    end_to_end_ids = get_end_to_end_id(n=n)
    for id in end_to_end_ids:
        infraction = deepcopy(example_pix_infraction)
        infraction.reference_id = id
        pix_infractions.append(infraction)
    return pix_infractions


def getPixInfractionToPatch():
    infraction_reports = []
    cursor = None
    while len(infraction_reports) < 1:
        reports, cursor = pixinfraction.page(status="delivered", limit=5, cursor=cursor)
        for report in reports:
            if report.flow == "in":
                infraction_reports.append(report)
        if cursor is None:
            break
    return choice(infraction_reports)
