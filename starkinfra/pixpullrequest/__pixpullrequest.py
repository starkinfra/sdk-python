from ..utils import rest
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime, check_date


class PixPullRequest(Resource):
    """# PixPullRequest object
    A Pix Pull Request is a command sent to the payer's bank to trigger the automatic
    debit linked to an active PixPullSubscription. It confirms the receiver's intent
    to collect the agreed amount within the current billing cycle and initiates the
    settlement process through the Pix infrastructure. Each pull request references a
    parent PixPullSubscription via `subscription_id`.
    When you initialize a PixPullRequest, the entity will not be automatically
    created in the Stark Infra API. The 'create' function sends the objects
    to the Stark Infra API and returns the list of created objects.
    ## Parameters (required):
    - amount [integer]: amount to be charged in cents. ex: 11234 (= R$ 112.34)
    - due [datetime.datetime or string]: due date for answering with an approval or denial. ISO 8601.
    - end_to_end_id [string]: Central Bank's unique transaction id. ex: "E00002649202201172211u34srod19le"
    - receiver_account_number [string]: receiver's bank account number. Use '-' before the verifier digit. ex: "876543-2"
    - receiver_account_type [string]: receiver's account type. Options: "checking", "savings", "salary", "payment"
    - receiver_bank_code [string]: receiver's bank code.
    - reconciliation_id [string]: id used for conciliation of the resulting Pix transaction. Up to 25 alphanumeric chars. ex: "123456"
    - subscription_id [string]: unique id of the parent PixPullSubscription.
    ## Parameters (optional):
    - attempt_type [string, default None]: defines the type of attempt. Options: "default", "instantRetry", "scheduledRetry".
    - description [string, default None]: additional information to be delivered to the sender.
    - receiver_branch_code [string, default None]: receiver's branch code.
    - tags [list of strings, default None]: list of strings for reference when searching for PixPullRequests. ex: ["employees", "monthly"]
    ## Attributes (return-only):
    - id [string]: unique id returned when the PixPullRequest is created. ex: "5656565656565656"
    - status [string]: current PixPullRequest status. Options: "created", "processing", "scheduled", "denied", "success", "canceled", "expired"
    - flow [string]: direction of money flow. Options: "in", "out"
    - receiver_name [string]: receiver's full name (filled in by the Pix infrastructure during settlement).
    - receiver_tax_id [string]: receiver's tax ID (CPF or CNPJ).
    - sender_bank_code [string]: sender's bank institution code in Brazil.
    - sender_final_name [string]: sender's final name when the sender differs from the originating institution.
    - sender_tax_id [string]: sender's tax ID (CPF or CNPJ).
    - subscription_bacen_id [string]: bacenId of the parent subscription, denormalized for convenience.
    - created [datetime.datetime]: creation datetime for the PixPullRequest.
    - updated [datetime.datetime]: latest update datetime for the PixPullRequest.
    """

    def __init__(self, amount, due, end_to_end_id, receiver_account_number, receiver_account_type,
                 receiver_bank_code, reconciliation_id, subscription_id,
                 attempt_type=None, description=None, receiver_branch_code=None, tags=None,
                 id=None, status=None, flow=None, receiver_name=None, receiver_tax_id=None,
                 sender_bank_code=None, sender_final_name=None, sender_tax_id=None,
                 subscription_bacen_id=None, created=None, updated=None):
        Resource.__init__(self, id=id)

        self.amount = amount
        self.due = check_datetime(due)
        self.end_to_end_id = end_to_end_id
        self.receiver_account_number = receiver_account_number
        self.receiver_account_type = receiver_account_type
        self.receiver_bank_code = receiver_bank_code
        self.reconciliation_id = reconciliation_id
        self.subscription_id = subscription_id
        self.attempt_type = attempt_type
        self.description = description
        self.receiver_branch_code = receiver_branch_code
        self.tags = tags
        self.status = status
        self.flow = flow
        self.receiver_name = receiver_name
        self.receiver_tax_id = receiver_tax_id
        self.sender_bank_code = sender_bank_code
        self.sender_final_name = sender_final_name
        self.sender_tax_id = sender_tax_id
        self.subscription_bacen_id = subscription_bacen_id
        self.created = check_datetime(created)
        self.updated = check_datetime(updated)


_resource = {"class": PixPullRequest, "name": "PixPullRequest"}


def create(requests, user=None):
    """# Create PixPullRequests
    Send a list of PixPullRequest objects for creation at the Stark Infra API
    ## Parameters (required):
    - requests [list of PixPullRequest objects]: list of PixPullRequest objects to be created in the API
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of PixPullRequest objects with updated attributes
    """
    return rest.post_multi(resource=_resource, entities=requests, user=user)


def get(id, user=None):
    """# Retrieve a specific PixPullRequest
    Receive a single PixPullRequest object previously created in the Stark Infra API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - PixPullRequest object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def query(limit=None, after=None, before=None, status=None, tags=None, ids=None,
          subscription_ids=None, flows=None, user=None):
    """# Retrieve PixPullRequests
    Receive a generator of PixPullRequest objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None]: date filter for objects created after a specified date.
    - before [datetime.date or string, default None]: date filter for objects created before a specified date.
    - status [list of strings, default None]: filter for status of retrieved objects. ex: ["created", "processing", "scheduled", "denied", "success", "canceled", "expired"]
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["employees", "monthly"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - subscription_ids [list of strings, default None]: filter by parent PixPullSubscription ids. ex: ["5656565656565656", "4545454545454545"]
    - flows [list of strings, default None]: direction of money flow to filter retrieved objects. Options: "in", "out".
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - generator of PixPullRequest objects with updated attributes
    """
    return rest.get_stream(
        resource=_resource,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        status=status,
        tags=tags,
        ids=ids,
        subscription_ids=subscription_ids,
        flows=flows,
        user=user,
    )


def page(cursor=None, limit=None, after=None, before=None, status=None, tags=None,
         ids=None, subscription_ids=None, flows=None, user=None):
    """# Retrieve paged PixPullRequests
    Receive a list of up to 100 PixPullRequest objects previously created and a cursor for the next page.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page call.
    - limit [integer, default 100]: maximum number of objects to be retrieved. Max = 100. ex: 50
    - after [datetime.date or string, default None]: date filter for objects created after a specified date.
    - before [datetime.date or string, default None]: date filter for objects created before a specified date.
    - status [list of strings, default None]: filter for status of retrieved objects. ex: ["created", "processing", "scheduled", "denied", "success", "canceled", "expired"]
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["employees", "monthly"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - subscription_ids [list of strings, default None]: filter by parent PixPullSubscription ids. ex: ["5656565656565656", "4545454545454545"]
    - flows [list of strings, default None]: direction of money flow to filter retrieved objects. Options: "in", "out".
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of PixPullRequest objects with updated attributes
    - cursor to retrieve the next page
    """
    return rest.get_page(
        resource=_resource,
        cursor=cursor,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        status=status,
        tags=tags,
        ids=ids,
        subscription_ids=subscription_ids,
        flows=flows,
        user=user,
    )


def update(id, status=None, reason=None, user=None):
    """# Update PixPullRequest entity
    Update a PixPullRequest to change its status to "scheduled" or "denied".
    ## Parameters (required):
    - id [string]: PixPullRequest unique id. ex: "5656565656565656"
    ## Parameters (conditionally required):
    - reason [string, default None]: required when `status` is "denied". Options: "senderAccountClosed", "senderAccountBlocked", "amountNotAllowed".
    ## Parameters (optional):
    - status [string, default None]: new status. Options: "scheduled", "denied".
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - PixPullRequest with updated attributes
    """
    payload = {
        "status": status,
        "reason": reason,
    }
    return rest.patch_id(resource=_resource, id=id, user=user, payload=payload)


def cancel(id, reason=None, user=None):
    """# Cancel a PixPullRequest entity
    Cancel a PixPullRequest previously created in the Stark Infra API.
    `reason` is sent as a query parameter on the DELETE request.
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - reason [string, default None]: cancellation reason. Options: "accountClosed", "accountBlocked", "pixRequestFailed", "other", "senderUserRequested", "receiverUserRequested"
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - canceled PixPullRequest object
    """
    return rest.delete_id(resource=_resource, id=id, reason=reason, user=user)
