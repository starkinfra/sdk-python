from json import dumps
from starkinfra.utils import rest
from starkcore.utils.api import api_json
from ..utils.parse import parse_and_verify
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime, check_date


class IssuingToken(Resource):
    """# IssuingToken object
    The IssuingToken object displays the information of the tokens created in your Workspace.
    ## Attributes (return-only):
    - card_id [string]: card ID which the token is bounded to. ex: "5656565656565656"
    - wallet_id [string]: wallet provider which the token is bounded to. ex: "google"
    - wallet_name [string]: wallet name. ex: "GOOGLE"
    - merchant_id [string]: merchant unique id. ex: "5656565656565656"
    ## Attributes (IssuingToken only):
    - id [string]: unique id returned when IssuingToken is created. ex: "5656565656565656"
    - external_id [string]: a unique string among all your IssuingTokens, used to avoid resource duplication. ex: "DSHRMC00002626944b0e3b539d4d459281bdba90c2588791"
    - tags [list of strings]: list of strings for reference when searching for IssuingToken. ex: ["employees", "monthly"]
    - status [string]: current IssuingToken status. ex: "active", "blocked", "canceled", "frozen" or "pending"
    - updated [datetime.datetime]: latest update datetime for the IssuingToken. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - created [datetime.datetime]: creation datetime for the IssuingToken. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    ## Attributes (authorization request only):
    - activation_code [string]: activation code recived through the bank app or sms. ex: "481632" 
    - method_code [string]: provisioning method. Options: "app", "token", "manual", "server" or "browser"
    - device_type [string]: device type used for tokenization. ex: "Phone"
    - device_name [string]: device name used for tokenization. ex: "My phone" 
    - device_serial_number [string]: device serial number used for tokenization. ex: "2F6D63"
    - device_os_name [string]: device operational system name used for tokenization. ex: "Android"
    - device_os_version [string]: device operational system version used for tokenization. ex: "4.4.4"
    - device_imei [string]: device imei used for tokenization. ex: "352099001761481"
    - wallet_instance_id [string]: unique id refered to the wallet app in the current device. ex: "71583be4777eb89aaf0345eebeb82594f096615ed17862d0"
    """

    def __init__(self, card_id=None, wallet_id=None, wallet_name=None, merchant_id=None, id=None,
                external_id=None, tags=None, status=None, updated=None, created=None, activation_code=None,
                method_code=None, device_type=None, device_name=None, device_serial_number=None, device_os_name=None,
                device_os_version=None, device_imei=None, wallet_instance_id=None):
        Resource.__init__(self, id=id)

        self.card_id = card_id
        self.wallet_id = wallet_id
        self.wallet_name = wallet_name
        self.merchant_id = merchant_id
        self.external_id = external_id
        self.tags = tags
        self.status = status
        self.updated = updated
        self.created = created
        self.activation_code = activation_code
        self.method_code = method_code
        self.device_type = device_type
        self.device_name = device_name
        self.device_serial_number = device_serial_number
        self.device_os_name = device_os_name
        self.device_os_version = device_os_version
        self.device_imei = device_imei
        self.wallet_instance_id = wallet_instance_id


_resource = {"class": IssuingToken, "name": "IssuingToken"}


def get(id, user=None):
    """# Retrieve a specific IssuingToken
    Receive a single IssuingToken object previously created in the Stark Infra API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - IssuingToken object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def query(limit=None, after=None, before=None, status=None, card_ids=None, tags=None, ids=None, user=None, external_ids=None):
    """# Retrieve IssuingTokens
    Receive a generator of IssuingToken objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Max = 100. ex: 35
    - after [datetime.date or string, default None]: date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None]: date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - status [string, default None]: current IssuingToken status. ex: "active", "blocked", "canceled", "frozen" or "pending"
    - card_ids [list of strings, default None]: list of card_ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - tags [list of strings, default None]: list of strings for tagging. ex: ["travel", "food"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    - external_ids [list of strings, default None]: external IDs. ex: ["DSHRMC00002626944b0e3b539d4d459281bdba90c2588791", "DSHRMC00002626941c531164a0b14c66ad9602ee716f1e85"]
    ## Return:
    - generator of IssuingToken objects with updated attributes
    """
    return rest.get_stream(
        resource=_resource,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        status=status,
        card_ids=card_ids,
        tags=tags,
        ids=ids,
        user=user,
        external_ids=external_ids,
    )


def page(cursor=None, limit=None, after=None, before=None, status=None, card_ids=None, tags=None, ids=None, user=None, external_ids=None):
    """# Retrieve paged IssuingTokens
    Receive a list of IssuingToken objects previously created in the Stark Infra API and the cursor to the next page.
    Use this function instead of query if you want to manually page your requests.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - limit [integer, default 100]: maximum number of objects to be retrieved. Max = 100. ex: 35
    - after [datetime.date or string, default None]: date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None]: date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - status [string, default None]: current IssuingToken status. ex: "active", "blocked", "canceled", "frozen" or "pending"
    - card_ids [list of strings, default None]: list of card_ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - tags [list of strings, default None]: list of strings for tagging. ex: ["travel", "food"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    - external_ids [list of strings, default None]: external IDs. ex: ["5656565656565656", "4545454545454545"]
    ## Return:
    - list of IssuingToken objects with updated attributes
    - cursor to retrieve the next page of IssuingToken objects
    """
    return rest.get_page(
        resource=_resource,
        cursor=cursor,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        status=status,
        card_ids=card_ids,
        tags=tags,
        ids=ids,
        user=user,
        external_ids=external_ids,
    )


def update(id, status=None, tags=None, user=None):
    """# Update IssuingToken entity
    Update an IssuingToken by passing id.
    ## Parameters (required):
    - id [string]: IssuingToken id. ex: "5656565656565656"
    ## Parameters (optional):
    - status [string, default None]: You may block the IssuingToken by passing "blocked" or activate by passing "active" in the status. ex: "active", "blocked"
    - tags [list of strings, default None]: list of strings for tagging. ex: ["travel", "food"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - target IssuingToken with updated attributes
    """
    payload = {
        "status": status,
        "tags": tags
    }
    return rest.patch_id(resource=_resource, id=id, payload=payload, user=user)    


def cancel(id, user=None):
    """# Cancel an IssuingToken entity
    Cancel an entity previously created in the Stark Infra API by its ID
    ## Parameters (required):
    - id [string]: IssuingToken unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - canceled IssuingToken object
    """
    return rest.delete_id(resource=_resource, id=id, user=user)


def parse(content, signature, user=None):
    """# Create a single verified IssuingToken request from a content string
    Use this method to parse and verify the authenticity of the request received at the informed endpoint.
    Token requests are posted to your registered endpoint whenever IssuingTokens are received.
    If the provided digital signature does not check out with the StarkInfra public key, a stark.exception.InvalidSignatureException will be raised.
    ## Parameters (required):
    - content [string]: response content from request received at user endpoint (not parsed)
    - signature [string]: base-64 digital signature received at response header "Digital-Signature"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - Parsed IssuingToken object
    """
    return parse_and_verify(
        content=content,
        signature=signature,
        user=user,
        resource=_resource,
        key="",
    )


def response_authorization(status, reason=None, activation_methods=None, design_id=None, tags=None):
    """# Helps you respond IssuingToken authorization requests
    When a new tokenization is triggered by your user, a POST request will be made to your registered URL to get your decision to complete the tokenization.
    The POST request must be answered in the following format, within 2 seconds, and with an HTTP status code 200.
    ## Parameters (required):
    - status [string]: sub-issuer response to the authorization. ex: "approved" or "denied"
    ## Parameters (conditionally required):
    - reason [string, default ""]: denial reason. Options: "other", "bruteForce", "subIssuerError", "lostCard", "invalidCard", "invalidHolder", "expiredCard", "canceledCard", "blockedCard", "invalidExpiration", "invalidSecurityCode", "missingTokenAuthorizationUrl", "maxCardTriesExceeded", "maxWalletInstanceTriesExceeded"
    - activation_methods [list of dictionaries, default None]: list of dictionaries with "type":string and "value":string pairs
    - design_id [string, default None]: design unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - tags [list of strings, default None]: tags to filter retrieved object. ex: ["tony", "stark"]
    ## Return:
    - Dumped JSON string that must be returned to us on the IssuingToken request
    """
    params = {"authorization": {
        "status": status,
        "reason": reason or "",
        "activationMethods": activation_methods,
        "designId": design_id,
        "tags": tags,
    }}
    return dumps(api_json(params))


def response_activation(status, reason=None, tags=None):
    """# Helps you respond IssuingToken activation requests
    When a new token activation is triggered by your user, a POST request will be made to your registered URL for you to confirm the activation code you informed to them. You may identify this request through the present activation_code in the payload.
    The POST request must be answered in the following format, within 2 seconds, and with an HTTP status code 200.
    ## Parameters (required):
    - status [string]: sub-issuer response to the activation. ex: "approved" or "denied"
    ## Parameters (optional):
    - reason [string, default ""]: denial reason. Options: "other", "bruteForce", "subIssuerError", "lostCard", "invalidCard", "invalidHolder", "expiredCard", "canceledCard", "blockedCard", "invalidExpiration", "invalidSecurityCode", "missingTokenAuthorizationUrl", "maxCardTriesExceeded", "maxWalletInstanceTriesExceeded"
    - tags [list of strings, default None]: tags to filter retrieved object. ex: ["tony", "stark"]
    ## Return:
    - Dumped JSON string that must be returned to us on the IssuingToken request
    """
    params = {"authorization": {
        "status": status,
        "reason": reason or "",
        "tags": tags,
    }}
    return dumps(api_json(params))
