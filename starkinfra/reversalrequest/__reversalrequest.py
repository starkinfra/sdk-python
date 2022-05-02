from ..utils import rest
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_date


class ReversalRequest(Resource):
    """# ReversalRequest object
    A reversal request can be created when fraud is detected on a transaction or a system malfunction
    results in an erroneous transaction.
    It notifies another participant of your request to reverse the payment they have received.
    When you initialize a ReversalRequest, the entity will not be automatically
    created in the Stark Infra API. The 'create' function sends the objects
    to the Stark Infra API and returns the created object.
    ## Parameters (required):
    - amount [integer]: amount in cents to be reversed. ex: 11234 (= R$ 112.34)
    - reference_id [string]: end_to_end_id or return_id of the transaction to be reversed. ex: "E20018183202201201450u34sDGd19lz"
    - reason [string]: reason why the reversal was requested. Options: "fraud", "flaw", "reversalChargeback"
    ## Parameters (optional):
    - description [string, default None]: description for the ReversalRequest.
    ## Attributes (return-only):
    - analysis [string, Default None]: analysis that led to the result.
    - bacen_id [string, Default None]: central bank's unique UUID that identifies the ReversalRequest.
    - sender_bank_code [string, Default None]: bank_code of the Pix participant that created the ReversalRequest. ex: "20018183"
    - receiver_bank_code [string, Default None]: bank_code of the Pix participant that received the ReversalRequest. ex: "20018183"
    - rejection_reason [string, Default None]: reason for the rejection of the reversal request. Options: "noBalance", "accountClosed", "unableToReverse"
    - reversal_reference_id [string, Default None]: return id of the reversal transaction. ex: "D20018183202202030109X3OoBHG74wo".
    - id [string, default None]: unique id returned when the ReversalRequest is created. ex: "5656565656565656"
    - result [string, Default None]: result after the analysis of the ReversalRequest by the receiving party. Options: "rejected", "accepted", "partiallyAccepted"
    - status [string, default None]: current ReversalRequest status. Options: "created", "failed", "delivered", "closed", "canceled".
    - created [datetime.datetime, default None]: creation datetime for the ReversalRequest. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - updated [datetime.datetime, default None]: latest update datetime for the ReversalRequest. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self,  amount, reference_id, reason, description=None, analysis=None, bacen_id=None,
                 sender_bank_code=None, receiver_bank_code=None, rejection_reason=None, reversal_reference_id=None, id=None,
                 result=None, status=None, created=None, updated=None):
        Resource.__init__(self, id=id)

        self.amount = amount
        self.reference_id = reference_id
        self.reason = reason
        self.description = description
        self.analysis = analysis
        self.bacen_id = bacen_id
        self.sender_bank_code = sender_bank_code
        self.receiver_bank_code = receiver_bank_code
        self.rejection_reason = rejection_reason
        self.reversal_reference_id = reversal_reference_id
        self.result = result
        self.status = status
        self.created = created
        self.updated = updated


_resource = {"class": ReversalRequest, "name": "ReversalRequest"}


def create(request, user=None):
    """# Create a ReversalRequest object
    Create a ReversalRequest in the Stark Infra API
    ## Parameters (optional):
    - request [ReversalRequest object]: ReversalRequest object to be created in the API.
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - ReversalRequest object with updated attributes.
    """
    return rest.post_single(resource=_resource, entity=request, user=user)


def get(id, user=None):
    """# Retrieve a ReversalRequest object
    Retrieve the ReversalRequest object linked to your Workspace in the Stark Infra API using its id.
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656".
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - ReversalRequest object that corresponds to the given id.
    """

    return rest.get_id(id=id, resource=_resource, user=user)


def query(limit=None, after=None, before=None, status=None, ids=None, user=None):
    """# Retrieve ReversalRequests
    Receive a generator of ReversalRequests objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default 100]: maximum number of objects to be retrieved. Max = 100. ex: 35
    - after [datetime.date or string, default None]: date filter for objects created after a specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None]: date filter for objects created before a specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. Options: "created", "failed", "delivered", "closed", "canceled".
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - generator of ReversalRequest objects with updated attributes
    """

    return rest.get_stream(
        resource=_resource,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        status=status,
        ids=ids,
        user=user,
    )


def page(cursor=None, limit=None, after=None, before=None, status=None, ids=None, user=None):
    """# Retrieve ReversalRequests
    Receive a generator of ReversalRequests objects previously created in the Stark Infra API
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call.
    - limit [integer, default 100]: maximum number of objects to be retrieved. Max = 100. ex: 35
    - after [datetime.date or string, default None]: date filter for objects created after a specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None]: date filter for objects created before a specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. Options: "created", "failed", "delivered", "closed", "canceled".
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - type [list of strings, default None]: filter for the type of retrieved ReversalRequests. Options: "fraud", "reversal", "reversalChargeback"
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - cursor to retrieve the next page of ReversalRequest objects
    - generator of ReversalRequest objects with updated attributes
    """
    return rest.get_page(
        resource=_resource,
        cursor=cursor,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        status=status,
        ids=ids,
        user=user,
    )


def update(id, result, rejection_reason=None, reversal_reference_id=None, analysis=None, user=None):
    """# Update ReversalRequest entity
    Respond to a received ReversalRequest.
    ## Parameters (required):
    - id [string]: ReversalRequest id. ex: '5656565656565656'
    - result [string]: result after the analysis of the ReversalRequest. Options: "rejected", "accepted", "partiallyAccepted".
    ## Parameters (conditionally required):
    - rejection_reason [string, default None]: if the ReversalRequest is rejected a reason is required. Options: "noBalance", "accountClosed", "unableToReverse",
    - reversal_reference_id [string, default None]: return_id of the reversal transaction. ex: "D20018183202201201450u34sDGd19lz"
    ## Parameters (optional):
    - analysis [string, default None]: description of the analysis that led to the result.
    ## Return:
    - ReversalRequest with updated attributes
    """
    payload = {
        "result": result,
        "rejection_reason": rejection_reason,
        "reversal_reference_id": reversal_reference_id,
        "analysis": analysis
    }
    return rest.patch_id(resource=_resource, id=id, user=user, **payload)


def delete(id, user=None):
    """# Delete a ReversalRequest entity
    Delete a ReversalRequest entity previously created in the Stark Infra API
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - deleted ReversalRequest object
    """
    return rest.delete_id(resource=_resource, id=id, user=user)
