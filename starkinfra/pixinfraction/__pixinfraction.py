from ..utils import rest
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime, check_date


class PixInfraction(Resource):
    """# PixInfraction object
    PixInfractions are used to report transactions that are suspected of
    fraud, to request a refund or to reverse a refund.
    When you initialize a PixInfraction, the entity will not be automatically
    created in the Stark Infra API. The 'create' function sends the objects
    to the Stark Infra API and returns the created object.
    ## Parameters (required):
    - reference_id [string]: end_to_end_id or return_id of the transaction being reported. ex: "E20018183202201201450u34sDGd19lz"
    - type [string]: type of infraction report. Options: "reversal", "reversalChargeback"
    - method [string]:  method of Pix Infraction. Options: "scam", "unauthorized", "coercion", "invasion", "other", "unknown"
    ## Parameters (optional):
    - description [string, default None]: description for any details that can help with the infraction investigation.
    - operator_email [string]: contact email of the operator responsible for the PixInfraction.
    - operator_phone [string]: contact phone number of the operator responsible for the PixInfraction.
    - tags [list of strings, default []]: list of strings for tagging. ex: ["travel", "food"]
    - fraud_type [string, default None]: type of Pix Fraud. Options: "identity", "mule", "scam", "unknown", "other"
    ## Attributes (return-only):
    - id [string]: unique id returned when the PixInfraction is created. ex: "5656565656565656"
    - fraud_id [string]: id of the Pix Fraud. ex: "5741774970552320"
    - bacen_id [string, default None]: unique transaction id returned from Central Bank. ex: "ccf9bd9c-e99d-999e-bab9-b999ca999f99"
    - credited_bank_code [string]: bank_code of the credited Pix participant in the reported transaction. ex: "20018183"
    - debited_bank_code [string]: bank_code of the debited Pix participant in the reported transaction. ex: "20018183"
    - flow [string]: direction of the PixInfraction flow. Options: "out" if you created the PixInfraction, "in" if you received the PixInfraction.
    - analysis [string]: analysis that led to the result.
    - reported_by [string]: agent that reported the PixInfraction. Options: "debited", "credited"
    - result [string]: result after the analysis of the PixInfraction by the receiving party. Options: "agreed", "disagreed"
    - status [string]: current PixInfraction status. Options: "created", "failed", "delivered", "closed", "canceled"
    - created [datetime.datetime]: creation datetime for the PixInfraction. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - updated [datetime.datetime]: latest update datetime for the PixInfraction. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self,  reference_id, type, method, operator_email=None, operator_phone=None, description=None,
                 tags=None, fraud_type=None, id=None, fraud_id=None, bacen_id=None, credited_bank_code=None,
                 debited_bank_code=None, flow=None, analysis=None, reported_by=None, result=None, status=None,
                 created=None, updated=None):
        Resource.__init__(self, id=id)

        self.reference_id = reference_id
        self.type = type
        self.method = method
        self.description = description
        self.tags = tags
        self.fraud_type = fraud_type
        self.operator_email = operator_email
        self.operator_phone = operator_phone
        self.fraud_id = fraud_id
        self.bacen_id = bacen_id
        self.credited_bank_code = credited_bank_code
        self.debited_bank_code = debited_bank_code
        self.flow = flow
        self.analysis = analysis
        self.reported_by = reported_by
        self.result = result
        self.status = status
        self.created = check_datetime(created)
        self.updated = check_datetime(updated)


_resource = {"class": PixInfraction, "name": "PixInfraction"}


def create(infractions, user=None):
    """# Create PixInfraction objects
    Create PixInfractions in the Stark Infra API
    ## Parameters (required):
    - infractions [list of PixInfractions]: list of PixInfraction objects to be created in the API.
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of PixInfraction objects with updated attributes
    """
    return rest.post_multi(resource=_resource, entities=infractions, user=user)


def get(id, user=None):
    """# Retrieve a PixInfraction object
    Retrieve the PixInfraction object linked to your Workspace in the Stark Infra API using its id.
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - PixInfraction object that corresponds to the given id.
    """
    return rest.get_id(id=id, resource=_resource, user=user)


def query(limit=None, after=None, before=None, status=None, ids=None, bacen_id=None, type=None, flow=None, tags=None, user=None):
    """# Retrieve PixInfractions
    Receive a generator of PixInfraction objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None]: date filter for objects created after a specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None]: date filter for objects created before a specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. Options: ["created", "failed", "delivered", "closed", "canceled"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - bacen_id [string, default None]: unique transaction id returned from Central Bank. ex: "ccf9bd9c-e99d-999e-bab9-b999ca999f99"
    - type [list of strings, default None]: filter for the type of retrieved PixInfractions. Options: "fraud", "reversal", "reversalChargeback"
    - flow [string, default None]: direction of the PixInfraction flow. Options: "out" if you created the PixInfraction, "in" if you received the PixInfraction.
    - tags [list of strings, default None]: list of strings for tagging. ex: ["travel", "food"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - generator of PixInfraction objects with updated attributes
    """
    return rest.get_stream(
        resource=_resource,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        status=status,
        ids=ids,
        bacen_id=bacen_id,
        type=type,
        flow=flow,
        tags=tags,
        user=user,
    )


def page(cursor=None, limit=None, after=None, before=None, status=None, ids=None, bacen_id=None, type=None, flow=None, tags=None,
         user=None):
    """# Retrieve paged PixInfractions
    Receive a list of up to 100 PixInfraction objects previously created in the Stark Infra API and the cursor to the next page.
    Use this function instead of query if you want to manually page your requests.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call.
    - limit [integer, default 100]: maximum number of objects to be retrieved. Max = 100. ex: 35
    - after [datetime.date or string, default None]: date filter for objects created after a specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None]: date filter for objects created before a specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. Options: ["created", "failed", "delivered", "closed", "canceled"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - bacen_id [string, default None]: unique transaction id returned from Central Bank. ex: "ccf9bd9c-e99d-999e-bab9-b999ca999f99"
    - type [list of strings, default None]: filter for the type of retrieved PixInfractions. Options: "fraud", "reversal", "reversalChargeback"
    - flow [string, default None]: direction of the PixInfraction flow. Options: "out" if you created the PixInfraction, "in" if you received the PixInfraction.
    - tags [list of strings, default None]: list of strings for tagging. ex: ["travel", "food"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of PixInfraction objects with updated attributes and cursor to retrieve the next page of PixInfraction objects
    """
    return rest.get_page(
        resource=_resource,
        cursor=cursor,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        status=status,
        ids=ids,
        bacen_id=bacen_id,
        type=type,
        flow=flow,
        tags=tags,
        user=user,
    )


def update(id, result, fraud_type=None, analysis=None, user=None):
    """# Update PixInfraction entity
    Update a PixInfraction by passing id.
    ## Parameters (required):
    - id [string]: PixInfraction id. ex: '5656565656565656'
    - result [string]: result after the analysis of the PixInfraction. Options: "agreed", "disagreed"
    ## Parameters (conditionally required):
    - fraud_type [string, default None]: type of Pix Fraud. Options: "identity", "mule", "scam", "unknown", "other"
    ## Parameters (optional):
    - analysis [string, default None]: analysis that led to the result.
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - PixInfraction with updated attributes
    """
    payload = {
        "result": result,
        "fraud_type": fraud_type,
        "analysis": analysis,
    }
    return rest.patch_id(resource=_resource, id=id, user=user, payload=payload)


def cancel(id, user=None):
    """# Cancel a PixInfraction entity
    Cancel a PixInfraction entity previously created in the Stark Infra API
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - canceled PixInfraction object
    """
    return rest.delete_id(resource=_resource, id=id, user=user)
