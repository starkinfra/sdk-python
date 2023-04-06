from ..utils import rest
from ..utils.parse import parse_and_verify
from starkcore.utils.api import from_api_json
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime, check_date
from ..creditnote.log.__log import _resource as _creditnote_log_resource
from ..pixkey.log.__log import _resource as _pixkey_log_resource
from ..pixclaim.log.__log import _resource as _pixclaim_log_resource
from ..pixrequest.log.__log import _resource as _pixrequest_log_resource
from ..pixreversal.log.__log import _resource as _pixreversal_log_resource
from ..pixchargeback.log.__log import _resource as _pixchargeback_log_resource
from ..pixinfraction.log.__log import _resource as _pixinfraction_log_resource
from ..issuingcard.log.__log import _resource as _issuingcard_log_resource
from ..issuinginvoice.log.__log import _resource as _issuinginvoice_log_resource
from ..issuingpurchase.log.__log import _resource as _issuingpurchase_log_resource


_resource_by_subscription = {
    "pix-key": _pixkey_log_resource,
    "pix-claim": _pixclaim_log_resource,
    "pix-chargeback": _pixchargeback_log_resource,
    "pix-infraction": _pixinfraction_log_resource,
    "pix-request.in": _pixrequest_log_resource,
    "pix-request.out": _pixrequest_log_resource,
    "pix-reversal.in": _pixreversal_log_resource,
    "pix-reversal.out": _pixreversal_log_resource,
    "issuing-card": _issuingcard_log_resource,
    "issuing-invoice": _issuinginvoice_log_resource,
    "issuing-purchase": _issuingpurchase_log_resource,
    "credit-note": _creditnote_log_resource,
}


class Event(Resource):
    """# Webhook Event object
    An Event is the notification received from the subscription to the Webhook.
    Events cannot be created, but may be retrieved from the Stark Infra API to
    list all generated updates on entities.
    ## Attributes (return-only):
    - id [string]: unique id returned when the Event is created. ex: "5656565656565656"
    - log [Log]: a Log object from one of the subscribed services (PixRequestLog, PixReversalLog)
    - created [datetime.datetime]: creation datetime for the notification Event. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - is_delivered [bool]: true if the Event has been successfully delivered to the user url. ex: False
    - subscription [string]: service that triggered this Event. Options: "pix-request.in", "pix-request.out", "pix-reversal.in", "pix-reversal.out", "pix-key", "pix-claim", "pix-infraction", "pix-chargeback", "issuing-card", "issuing-invoice", "issuing-purchase", "credit-note"
    - workspace_id [string]: ID of the Workspace that generated this Event. Mostly used when multiple Workspaces have Webhooks registered to the same endpoint. ex: "4545454545454545"
    """

    def __init__(self, log, created, is_delivered, subscription, workspace_id, id):
        Resource.__init__(self, id=id)

        self.log = log
        self.created = check_datetime(created)
        self.is_delivered = is_delivered
        self.subscription = subscription
        self.workspace_id = workspace_id
        if subscription in _resource_by_subscription:
            self.log = from_api_json(resource=_resource_by_subscription[subscription], json=log)


_resource = {"class": Event, "name": "Event"}


def get(id, user=None):
    """# Retrieve a specific notification Event
    Receive a single notification Event object previously created in the Stark Infra API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - Event object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def query(limit=None, after=None, before=None, is_delivered=None, user=None):
    """# Retrieve notification Events
    Receive a generator of notification Event objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None]: date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None]: date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - is_delivered [bool, default None]: bool to filter successfully delivered events. ex: True or False
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - generator of Event objects with updated attributes
    """
    return rest.get_stream(
        resource=_resource,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        is_delivered=is_delivered,
        user=user,
    )


def page(cursor=None, limit=None, after=None, before=None, is_delivered=None, user=None):
    """# Retrieve paged Events
    Receive a list of up to 100 Event objects previously created in the Stark Infra API and the cursor to the next page.
    Use this function instead of query if you want to manually page your requests.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - limit [integer, default 100]: maximum number of objects to be retrieved. It must be an integer between 1 and 100. ex: 50
    - after [datetime.date or string, default None]: date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None]: date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - is_delivered [bool, default None]: bool to filter successfully delivered events. ex: True or False
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of Event objects with updated attributes
    - cursor to retrieve the next page of Event objects
    """
    return rest.get_page(
        resource=_resource,
        cursor=cursor,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        is_delivered=is_delivered,
        user=user,
    )


def delete(id, user=None):
    """# Delete a Webhook Event entity
    Delete a notification Event entity previously created in the Stark Infra API by its ID
    ## Parameters (required):
    - id [string]: Event unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - deleted Event object
    """
    return rest.delete_id(resource=_resource, id=id, user=user)


def update(id, is_delivered, user=None):
    """# Update notification Event entity
    Update notification Event by passing id.
    If is_delivered is True, the event will no longer be returned on queries with is_delivered=False.
    ## Parameters (required):
    - id [list of strings]: Event unique ids. ex: "5656565656565656"
    - is_delivered [bool]: If True and event hasn't been delivered already, event will be set as delivered. ex: True
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - target Event with updated attributes
    """
    payload = {
        "is_delivered": is_delivered
    }
    return rest.patch_id(resource=_resource, id=id, user=user, payload=payload)


def parse(content, signature, user=None):
    """# Create a single notification Event from a content string
    Create a single Event object received from Event listening at subscribed user endpoint.
    If the provided digital signature does not check out with the StarkInfra public key, a
    starkinfra.error.InvalidSignatureError will be raised.
    ## Parameters (required):
    - content [string]: response content from request received at user endpoint (not parsed)
    - signature [string]: base-64 digital signature received at response header "Digital-Signature"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - Parsed Event object
    """

    return parse_and_verify(
        content=content,
        signature=signature,
        user=user,
        resource=_resource,
        key="event",
    )
