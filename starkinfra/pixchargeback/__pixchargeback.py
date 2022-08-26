from ..utils import rest
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_date


class PixChargeback(Resource):
    """# PixChargeback object
    A Pix chargeback can be created when fraud is detected on a transaction or a system malfunction
    results in an erroneous transaction.
    It notifies another participant of your request to reverse the payment they have received.
    When you initialize a PixChargeback, the entity will not be automatically
    created in the Stark Infra API. The 'create' function sends the objects
    to the Stark Infra API and returns the created object.
    ## Parameters (required):
    - amount [integer]: amount in cents to be reversed. ex: 11234 (= R$ 112.34)
    - reference_id [string]: end_to_end_id or return_id of the transaction to be reversed. ex: "E20018183202201201450u34sDGd19lz"
    - reason [string]: reason why the reversal was requested. Options: "fraud", "flaw", "reversalChargeback"
    ## Parameters (optional):
    - description [string, default None]: description for the PixChargeback.
    - tags [list of strings, default []]: list of strings for tagging. ex: ["travel", "food"]
    ## Attributes (return-only):
    - id [string]: unique id returned when the PixChargeback is created. ex: "5656565656565656"
    - analysis [string]: analysis that led to the result.
    - sender_bank_code [string]: bank_code of the Pix participant that created the PixChargeback. ex: "20018183"
    - receiver_bank_code [string]: bank_code of the Pix participant that received the PixChargeback. ex: "20018183"
    - rejection_reason [string]: reason for the rejection of the Pix chargeback. Options: "noBalance", "accountClosed", "unableToReverse"
    - reversal_reference_id [string]: return_id or end_to_end_id of the reversal transaction. ex: "D20018183202202030109X3OoBHG74wo"
    - result [string]: result after the analysis of the PixChargeback by the receiving party. Options: "rejected", "accepted", "partiallyAccepted"
    - flow [string]: direction of the Pix Chargeback. Options: "in" for received chargebacks, "out" for chargebacks you requested
    - status [string]: current PixChargeback status. Options: "created", "failed", "delivered", "closed", "canceled"
    - created [datetime.datetime]: creation datetime for the PixChargeback. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - updated [datetime.datetime]: latest update datetime for the PixChargeback. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self,  amount, reference_id, reason, description=None, tags=None, id=None, analysis=None,
                 sender_bank_code=None, receiver_bank_code=None, rejection_reason=None, reversal_reference_id=None,
                 result=None, flow=None, status=None, created=None, updated=None):
        Resource.__init__(self, id=id)

        self.amount = amount
        self.reference_id = reference_id
        self.reason = reason
        self.description = description
        self.tags = tags
        self.analysis = analysis
        self.sender_bank_code = sender_bank_code
        self.receiver_bank_code = receiver_bank_code
        self.rejection_reason = rejection_reason
        self.reversal_reference_id = reversal_reference_id
        self.result = result
        self.flow = flow
        self.status = status
        self.created = created
        self.updated = updated


_resource = {"class": PixChargeback, "name": "PixChargeback"}


def create(chargebacks, user=None):
    """# Create PixChargeback objects
    Create PixChargebacks in the Stark Infra API
    ## Parameters (optional):
    - chargebacks [list of PixChargeback]: list of PixChargeback objects to be created in the API.
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of PixChargeback objects with updated attributes
    """
    return rest.post_multi(resource=_resource, entities=chargebacks, user=user)


def get(id, user=None):
    """# Retrieve a PixChargeback object
    Retrieve the PixChargeback object linked to your Workspace in the Stark Infra API using its id.
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - PixChargeback object that corresponds to the given id.
    """

    return rest.get_id(id=id, resource=_resource, user=user)


def query(limit=None, after=None, before=None, status=None, ids=None, flow=None, tags=None, user=None):
    """# Retrieve PixChargebacks
    Receive a generator of PixChargeback objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None]: date filter for objects created after a specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None]: date filter for objects created before a specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. ex: ["created", "failed", "delivered", "closed", "canceled"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - flow [string, default None]: direction of the Pix Chargeback. Options: "in" for received chargebacks, "out" for chargebacks you requested
    - tags [list of strings, default None]: filter for tags of retrieved objects. ex: ["travel", "food"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - generator of PixChargeback objects with updated attributes
    """

    return rest.get_stream(
        resource=_resource,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        status=status,
        ids=ids,
        flow=flow,
        tags=tags,
        user=user,
    )


def page(cursor=None, limit=None, after=None, before=None, status=None, ids=None, flow=None, tags=None, user=None):
    """# Retrieve PixChargebacks
    Receive a generator of PixChargeback objects previously created in the Stark Infra API
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call.
    - limit [integer, default 100]: maximum number of objects to be retrieved. Max = 100. ex: 35
    - after [datetime.date or string, default None]: date filter for objects created after a specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None]: date filter for objects created before a specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. ex: ["created", "failed", "delivered", "closed", "canceled"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - flow [string, default None]: direction of the Pix Chargeback. Options: "in" for received chargebacks, "out" for chargebacks you requested
    - tags [list of strings, default None]: filter for tags of retrieved objects. ex: ["travel", "food"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - cursor to retrieve the next page of PixChargeback objects
    - generator of PixChargeback objects with updated attributes
    """
    return rest.get_page(
        resource=_resource,
        cursor=cursor,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        status=status,
        ids=ids,
        flow=flow,
        tags=tags,
        user=user,
    )


def update(id, result, rejection_reason=None, reversal_reference_id=None, analysis=None, user=None):
    """# Update PixChargeback entity
    Respond to a received PixChargeback.
    ## Parameters (required):
    - id [string]: PixChargeback id. ex: '5656565656565656'
    - result [string]: result after the analysis of the PixChargeback. Options: "rejected", "accepted", "partiallyAccepted"
    ## Parameters (conditionally required):
    - rejection_reason [string, default None]: if the PixChargeback is rejected a reason is required. Options: "noBalance", "accountClosed", "unableToReverse",
    - reversal_reference_id [string, default None]: return_id of the reversal transaction. ex: "D20018183202201201450u34sDGd19lz"
    ## Parameters (optional):
    - analysis [string, default None]: description of the analysis that led to the result.
    ## Return:
    - PixChargeback with updated attributes
    """
    payload = {
        "result": result,
        "rejection_reason": rejection_reason,
        "reversal_reference_id": reversal_reference_id,
        "analysis": analysis
    }
    return rest.patch_id(resource=_resource, id=id, user=user, payload=payload)


def cancel(id, user=None):
    """# Cancel a PixChargeback entity
    Cancel a PixChargeback entity previously created in the Stark Infra API
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - canceled PixChargeback object
    """
    return rest.delete_id(resource=_resource, id=id, user=user)
