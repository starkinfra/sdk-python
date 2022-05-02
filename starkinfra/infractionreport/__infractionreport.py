from ..utils import rest
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime, check_date


class InfractionReport(Resource):
    """# IssuingAuthorization object
    Infraction reports are used to report transactions that are suspected of
    fraud, to request a refund or to reverse a refund.
    When you initialize a InfractionReport, the entity will not be automatically
    created in the Stark Infra API. The 'create' function sends the objects
    to the Stark Infra API and returns the created object.
    ## Parameters (required):
    - reference_id [string]: end_to_end_id or return_id of the transaction being reported. ex: "E20018183202201201450u34sDGd19lz"
    - type [string]: type of infraction report. Options: "fraud", "reversal", "reversalChargeback"
    ## Parameters (optional):
    - description [string, Default None]: description for any details that can help with the infraction investigation.
    - credited_bank_code [string, Default None]: bank_code of the credited Pix participant in the reported transaction. ex: "20018183"
    ## Attributes (return-only):
    - agent [string, Default None]: Options: "reporter" if you created the InfractionReport, "reported" if you received the InfractionReport.
    - analysis [string, Default None]: analysis that led to the result.
    - bacen_id [string, Default None]: central bank's unique UUID that identifies the infraction report.
    - debited_bank_code [string, Default None]: bank_code of the debited Pix participant in the reported transaction. ex: "20018183"
    - id [string, default None]: unique id returned when the InfractionReport is created. ex: "5656565656565656"
    - reported_by [string, Default None]: agent that reported the InfractionReport. Options: "debited", "credited".
    - result [string, Default None]: result after the analysis of the InfractionReport by the receiving party. Options: "agreed", "disagreed"
    - status [string, default None]: current InfractionReport status. Options: "created", "failed", "delivered", "closed", "canceled".
    - created [datetime.datetime, default None]: creation datetime for the InfractionReport. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - updated [datetime.datetime, default None]: latest update datetime for the InfractionReport. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self,  reference_id, type, description=None, credited_bank_code=None, agent=None, analysis=None,
                 bacen_id=None, bank_code=None, debited_bank_code=None, id=None, reported_by=None, result=None, status=None,
                 created=None, updated=None):
        Resource.__init__(self, id=id)

        self.reference_id = reference_id
        self.type = type
        self.description = description
        self.credited_bank_code = credited_bank_code
        self.agent = agent
        self.analysis = analysis
        self.bacen_id = bacen_id
        self.bank_code = bank_code
        self.debited_bank_code = debited_bank_code
        self.reported_by = reported_by
        self.result = result
        self.status = status
        self.created = check_datetime(created)
        self.updated = check_datetime(updated)


_resource = {"class": InfractionReport, "name": "InfractionReport"}


def create(report, user=None):
    """# Create a InfractionReport object
    Create a InfractionReport in the Stark Infra API
    ## Parameters (optional):
    - report [InfractionReport object]: InfractionReport object to be created in the API.
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - InfractionReport object with updated attributes.
    """
    return rest.post_single(resource=_resource, entity=report, user=user)


def get(id, user=None):
    """# Retrieve a InfractionReport object
    Retrieve the InfractionReport object linked to your Workspace in the Stark Infra API using its id.
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656".
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - InfractionReport object that corresponds to the given id.
    """

    return rest.get_id(id=id, resource=_resource, user=user)


def query(limit=None, after=None, before=None, status=None, ids=None, type=None, user=None):
    """# Retrieve InfractionReports
    Receive a generator of InfractionReports objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default 100]: maximum number of objects to be retrieved. Max = 100. ex: 35
    - after [datetime.date or string, default None]: date filter for objects created after a specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None]: date filter for objects created before a specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. Options: "created", "failed", "delivered", "closed", "canceled".
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - type [list of strings, default None]: filter for the type of retrieved InfractionReports. Options: "fraud", "reversal", "reversalChargeback"
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - generator of InfractionReport objects with updated attributes
    """

    return rest.get_stream(
        resource=_resource,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        status=status,
        ids=ids,
        type=type,
        user=user,
    )


def page(cursor=None, limit=None, after=None, before=None, status=None, ids=None, type=None,
         user=None):
    """# Retrieve InfractionReports
    Receive a generator of InfractionReports objects previously created in the Stark Infra API
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call.
    - limit [integer, default 100]: maximum number of objects to be retrieved. Max = 100. ex: 35
    - after [datetime.date or string, default None]: date filter for objects created after a specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None]: date filter for objects created before a specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. Options: "created", "failed", "delivered", "closed", "canceled".
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - type [list of strings, default None]: filter for the type of retrieved InfractionReports. Options: "fraud", "reversal", "reversalChargeback"
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - cursor to retrieve the next page of InfractionReport objects
    - generator of InfractionReport objects with updated attributes
    """
    return rest.get_page(
        resource=_resource,
        cursor=cursor,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        status=status,
        ids=ids,
        type=type,
        user=user,
    )


def update(id, result, analysis=None, user=None):
    """# Update InfractionReport entity
    Respond to a received InfractionReport.
    ## Parameters (required):
    - id [string]: InfractionReport id. ex: '5656565656565656'
    - result [string]: result after the analysis of the InfractionReport. Options: "agreed", "disagreed"
    ## Parameters (optional):
    - analysis [string, default None]: analysis that led to the result.
    ## Return:
    - InfractionReport with updated attributes
    """
    payload = {
        "result": result,
        "analysis": analysis,
    }
    return rest.patch_id(resource=_resource, id=id, user=user, **payload)


def delete(id, user=None):
    """# Delete a InfractionReport entity
    Delete a InfractionReport entity previously created in the Stark Infra API
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - deleted InfractionReport object
    """
    return rest.delete_id(resource=_resource, id=id, user=user)
