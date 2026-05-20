from ..utils import rest
from ..utils.parse import parse_and_verify
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime, check_datetime_or_date, check_date


class PixPullSubscription(Resource):
    """# PixPullSubscription object
    PixPullSubscriptions are recurring Pix debit authorizations. A subscription defines
    the frequency, amount, and required payer authorizations for a series of Pix debits
    to be pulled from the sender by the receiver. Each cycle of an active subscription
    is triggered by a PixPullRequest (its subscriptionId references the subscription's id).
    When you initialize a PixPullSubscription, the entity will not be automatically
    created in the Stark Infra API. The 'create' function sends the objects
    to the Stark Infra API and returns the list of created objects.
    ## Parameters (required):
    - bacen_id [string]: Central Bank's unique recurrency id. Identifies the subscription in the Pix infrastructure.
    - external_id [string]: safe string that must be unique among all your Pix Pull Subscriptions. Used for idempotency.
    - installment_start [datetime.datetime or string]: start datetime of settlements allowed for this subscription. ISO 8601. ex: "2026-03-10T19:32:35.418698+00:00"
    - interval [string]: cycle definition. Options: "week", "month", "quarter", "semester", "year"
    - receiver_name [string]: receiver's full name. ex: "Edward Stark"
    - receiver_tax_id [string]: receiver's tax ID (CPF or CNPJ) with or without formatting. ex: "01234567890" or "20.018.183/0001-80"
    - receiver_bank_code [string]: receiver's bank institution code.
    - reference_code [string]: commercial-relation identifier. May be a contract number, order id, or client code.
    - sender_account_number [string]: sender's bank account number. Use '-' before the verifier digit. ex: "876543-2"
    - sender_bank_code [string]: sender's bank institution code in Brazil. ex: "20018183"
    - sender_branch_code [string]: sender's bank account branch code. Use '-' in case there is a verifier digit. ex: "1357-9"
    - sender_city_code [string]: IBGE code of the payer's city.
    - sender_tax_id [string]: sender's tax ID (CPF or CNPJ). Same format rules as receiver_tax_id.
    ## Parameters (conditionally required):
    - amount [integer, default None]: amount in cents charged every cycle. Required if the subscription has a fixed value; omit for variable-amount subscriptions. At least one of `amount` or `amount_min_limit` MUST be provided. ex: 11234 (= R$ 112.34)
    - amount_min_limit [integer, default None]: floor value for the maximum amount the sender can set when approving. Used for variable-amount subscriptions. At least one of `amount` or `amount_min_limit` MUST be provided.
    ## Parameters (optional):
    - type [string, default None]: subscription journey type. Options: "push", "qrcode", "qrcodeAndPayment", "paymentAndOrQrcode"
    - description [string, default None]: additional information delivered to the sender.
    - due [datetime.datetime, datetime.date or string, default None]: due date for the sender's answer (approval or denial).
    - installment_end [datetime.datetime, datetime.date or string, default None]: end datetime of settlements allowed for this subscription.
    - pull_retry_limit [integer, default None]: max number of retries the receiver may issue for a single failed pull cycle.
    - sender_final_name [string, default None]: final sender name when the sender differs from the originating institution.
    - sender_final_tax_id [string, default None]: final sender tax ID. Same format rules as sender_tax_id.
    - tags [list of strings, default None]: list of strings for reference when searching for PixPullSubscriptions. ex: ["employees", "monthly"]
    ## Attributes (return-only):
    - id [string]: unique id returned when the PixPullSubscription is created. ex: "5656565656565656"
    - status [string]: current lifecycle state. Options: "active", "approved", "canceled", "created", "denied", "expired", "failed", "pending"
    - flow [string]: direction of money flow. Options: "in", "out"
    - created [datetime.datetime]: creation datetime for the PixPullSubscription. ex: datetime.datetime(2026, 3, 10, 10, 30, 0, 0)
    - updated [datetime.datetime]: latest update datetime for the PixPullSubscription. ex: datetime.datetime(2026, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, bacen_id, external_id, installment_start, interval, receiver_name, receiver_tax_id,
                 receiver_bank_code, reference_code, sender_account_number, sender_bank_code,
                 sender_branch_code, sender_city_code, sender_tax_id,
                 type=None, amount=None, amount_min_limit=None, description=None, due=None,
                 installment_end=None, pull_retry_limit=None, sender_final_name=None,
                 sender_final_tax_id=None, tags=None,
                 id=None, status=None, flow=None, created=None, updated=None):
        Resource.__init__(self, id=id)

        self.bacen_id = bacen_id
        self.external_id = external_id
        self.installment_start = check_datetime(installment_start)
        self.interval = interval
        self.receiver_name = receiver_name
        self.receiver_tax_id = receiver_tax_id
        self.receiver_bank_code = receiver_bank_code
        self.reference_code = reference_code
        self.sender_account_number = sender_account_number
        self.sender_bank_code = sender_bank_code
        self.sender_branch_code = sender_branch_code
        self.sender_city_code = sender_city_code
        self.sender_tax_id = sender_tax_id
        self.type = type
        self.amount = amount
        self.amount_min_limit = amount_min_limit
        self.description = description
        if due == "":
            due = None
        self.due = check_datetime_or_date(due)
        if installment_end == "":
            installment_end = None
        self.installment_end = check_datetime_or_date(installment_end)
        self.pull_retry_limit = pull_retry_limit
        self.sender_final_name = sender_final_name
        self.sender_final_tax_id = sender_final_tax_id
        self.tags = tags
        self.status = status
        self.flow = flow
        self.created = check_datetime(created)
        self.updated = check_datetime(updated)


_resource = {"class": PixPullSubscription, "name": "PixPullSubscription"}


def create(subscriptions, user=None):
    """# Create PixPullSubscriptions
    Send a list of PixPullSubscription objects for creation at the Stark Infra API
    ## Parameters (required):
    - subscriptions [list of PixPullSubscription objects]: list of PixPullSubscription objects to be created in the API
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of PixPullSubscription objects with updated attributes
    """
    return rest.post_multi(resource=_resource, entities=subscriptions, user=user)


def get(id, user=None):
    """# Retrieve a specific PixPullSubscription
    Receive a single PixPullSubscription object previously created in the Stark Infra API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - PixPullSubscription object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def query(limit=None, after=None, before=None, status=None, tags=None, ids=None, flows=None, user=None):
    """# Retrieve PixPullSubscriptions
    Receive a generator of PixPullSubscription objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None]: date filter for objects created after a specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None]: date filter for objects created before a specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. ex: ["created", "active", "canceled", "failed"]
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - flows [list of strings, default None]: direction of money flow to filter retrieved objects. Options: "in", "out".
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - generator of PixPullSubscription objects with updated attributes
    """
    return rest.get_stream(
        resource=_resource,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        status=status,
        tags=tags,
        ids=ids,
        flows=flows,
        user=user,
    )


def page(cursor=None, limit=None, after=None, before=None, status=None, tags=None, ids=None, flows=None, user=None):
    """# Retrieve paged PixPullSubscriptions
    Receive a list of up to 100 PixPullSubscription objects previously created in the Stark Infra API and the cursor to the next page.
    Use this function instead of query if you want to manually page your requests.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - limit [integer, default 100]: maximum number of objects to be retrieved. Max = 100. ex: 35
    - after [datetime.date or string, default None]: date filter for objects created after a specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None]: date filter for objects created before a specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. ex: ["created", "active", "canceled", "failed"]
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - flows [list of strings, default None]: direction of money flow to filter retrieved objects. Options: "in", "out".
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of PixPullSubscription objects with updated attributes
    - cursor to retrieve the next page of PixPullSubscription objects
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
        flows=flows,
        user=user,
    )


def update(id, status, sender_city_code=None, reason=None, amount=None, amount_min_limit=None,
           due=None, pull_retry_limit=None, tags=None, user=None):
    """# Update PixPullSubscription entity
    Update a PixPullSubscription's mutable parameters by passing its id.
    When patching `status` to "confirmed", `sender_city_code` MUST be present in the patch.
    ## Parameters (required):
    - id [string]: PixPullSubscription unique id. ex: "5656565656565656"
    - status [string]: new status to set. ex: "confirmed". When set to "confirmed", `sender_city_code` is required.
    ## Parameters (conditionally required):
    - sender_city_code [string, default None]: IBGE code of the payer's city. Required when `status` is being set to "confirmed".
    ## Parameters (optional):
    - reason [string, default None]: reason for the patch. Options: "accountClosed", "accountBlocked", "invalidBranchCode", "notRecognizedBySender", "userRejected", "notOffered"
    - amount [integer, default None]: new amount in cents.
    - amount_min_limit [integer, default None]: new amount minimum limit.
    - due [datetime.datetime or string, default None]: new due date for the sender's answer.
    - pull_retry_limit [integer, default None]: new max number of retries.
    - tags [list of strings, default None]: new list of tags.
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - PixPullSubscription with updated attributes
    """
    payload = {
        "status": status,
        "sender_city_code": sender_city_code,
        "reason": reason,
        "amount": amount,
        "amount_min_limit": amount_min_limit,
        "due": due,
        "pull_retry_limit": pull_retry_limit,
        "tags": tags,
    }
    return rest.patch_id(resource=_resource, id=id, user=user, payload=payload)


def cancel(id, reason, user=None):
    """# Cancel a PixPullSubscription entity
    Cancel a PixPullSubscription entity previously created in the Stark Infra API.
    `reason` is sent as a query parameter on the DELETE request.
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    - reason [string]: reason why the PixPullSubscription is being cancelled. Options: "accountClosed", "receiverOrganizationClosed", "subscriptionRequestFailed", "fraud", "receiverUserRequested", "paymentNotFound"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - canceled PixPullSubscription object
    """
    return rest.delete_id(resource=_resource, id=id, reason=reason, user=user)


def parse(content, signature, user=None):
    """# Create a single verified PixPullSubscription object from a content string
    Create a single PixPullSubscription object from a content string received from a handler listening at the subscription url.
    If the provided digital signature does not check out with the StarkInfra public key, a
    starkinfra.error.InvalidSignatureError will be raised.
    ## Parameters (required):
    - content [string]: response content from request received at user endpoint (not parsed)
    - signature [string]: base-64 digital signature received at response header "Digital-Signature"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - Parsed PixPullSubscription object
    """
    return parse_and_verify(
        content=content,
        signature=signature,
        user=user,
        resource=_resource,
    )
