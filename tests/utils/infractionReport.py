#coding: utf-8
from copy import deepcopy
from random import choice
from ..utils.endToEndId import get_end_to_end_id
from starkinfra import InfractionReport, infractionreport


example_infraction_report = InfractionReport(
    reference_id=get_end_to_end_id()[0],
    type="fraud",
)


def generateExampleInfractionReportJson():
    infraction_report = deepcopy(example_infraction_report)
    return infraction_report


def getInfractionReportToPatch():
    infraction_reports = []
    cursor = None
    while len(infraction_reports) < 1:
        reports, cursor = infractionreport.page(status="created", limit=5, cursor=cursor)
        for report in reports:
            if report.agent == "reported":
                infraction_reports.append(report)
        if cursor is None:
            break
    return choice(infraction_reports)
