from ..utils.api import from_api_json
from ..utils.checks import check_datetime
from ..utils.resource import Resource
from ..pixrequest.log.__log import _resource as _pixrequest_log_resource
from ..pixreversal.log.__log import _resource as _pixreversal_log_resource
from json import loads, dumps
from requests import get as get_request
from ellipticcurve import Ecdsa, Signature, PublicKey
from ..utils.request import fetch
from ..error import InvalidSignatureError
from ..utils import cache


_resource_by_subscription = {
    "pix-request.in": _pixrequest_log_resource,
    "pix-request.out": _pixrequest_log_resource,
    "pix-reversal.in": _pixreversal_log_resource,
    "pix-reversal.out": _pixreversal_log_resource
}


class Event(Resource):
    """# Webhook Event object
    An Event is the notification received from the subscription to the Webhook.
    Events cannot be created, but may be retrieved from the Stark Infra API to
    list all generated updates on entities.
    ## Attributes:
    - id [string]: unique id returned when the Event is created. ex: "5656565656565656"
    - log [Log]: a Log object from one of the subscribed services (PixRequestLog, PixReversalLog)
    - created [datetime.datetime]: creation datetime for the notification Event. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - is_delivered [bool]: true if the Event has been successfully delivered to the user url. ex: False
    - subscription [string]: service that triggered this Event. ex: "pix-request.in", "pix-request.out"
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


def parse(content, signature, user=None):
    """# Create single notification Event from a content string
    Create a single Event object received from Event listening at subscribed user endpoint.
    If the provided digital signature does not check out with the StarkInfra public key, a
    starkinfra.exception.InvalidSignatureException will be raised.
    ## Parameters (required):
    - content [string]: response content from request received at user endpoint (not parsed)
    - signature [string]: base-64 digital signature received at response header "Digital-Signature"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - Parsed Event object
    """

    event = from_api_json(_resource, loads(content)["event"])

    try:
        signature = Signature.fromBase64(signature)
    except:
        raise InvalidSignatureError("The provided signature is not valid")

    public_key = _get_public_key(user=user)
    if _is_valid(content=content, signature=signature, public_key=public_key):
        return event

    public_key = _get_public_key(user=user, refresh=True)
    if _is_valid(content=content, signature=signature, public_key=public_key):
        return event

    raise InvalidSignatureError("The provided signature and content do not match the Stark Infra public key")


def _is_valid(content, signature, public_key):
    if Ecdsa.verify(message=content, signature=signature, publicKey=public_key):
        return True

    normalized = dumps(loads(content), sort_keys=True)
    if Ecdsa.verify(message=normalized, signature=signature, publicKey=public_key):
        return True

    return False


def _get_public_key(user, refresh=False):
    public_key = cache.get("starkinfra-public-key")
    if public_key and not refresh:
        return public_key

    pem = fetch(method=get_request, path="/public-key", query={"limit": 1}, user=user).json()["publicKeys"][0]["content"]
    public_key = PublicKey.fromPem(pem)
    cache["starkinfra-public-key"] = public_key
    return public_key
