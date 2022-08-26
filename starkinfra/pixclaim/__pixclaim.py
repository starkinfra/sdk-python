from ..utils import rest
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime, check_date


class PixClaim(Resource):
    """# PixClaim object
    PixClaims intend to transfer a PixKey from one account to another.
    When you initialize a PixClaim, the entity will not be automatically
    created in the Stark Infra API. The 'create' function sends the objects
    to the Stark Infra API and returns the created object.
    ## Parameters (required):
    - account_created [datetime.date, datetime.datetime or string]: opening Date or DateTime for the account claiming the PixKey. ex: "2022-01-01"
    - account_number [string]: number of the account claiming the PixKey. ex: "76543"
    - account_type [string]: type of the account claiming the PixKey. Options: "checking", "savings", "salary" or "payment"
    - branch_code [string]: branch code of the account claiming the PixKey. ex: "1234"
    - name [string]: holder's name of the account claiming the PixKey. ex: "Jamie Lannister"
    - tax_id [string]: holder's taxId of the account claiming the PixKey (CPF/CNPJ). ex: "012.345.678-90"
    - key_id [string]: id of the registered Pix Key to be claimed. Allowed keyTypes are CPF, CNPJ, phone number or email. ex: "+5511989898989"
    # Parameters (Options):
    - tags [list of strings, default []]: list of strings for tagging. ex: ["travel", "food"]
    ## Attributes (return-only):
    - id [string]: unique id returned when the PixClaim is created. ex: "5656565656565656"
    - status [string]: current PixClaim status. Options: "created", "failed", "delivered", "confirmed", "success", "canceled"
    - type [string]: type of Pix Claim. Options: "ownership", "portability"
    - key_type [string]: keyType of the claimed PixKey. Options: "CPF", "CNPJ", "phone" or "email"
    - flow [string]: direction of the Pix Claim. Options: "in" if you received the PixClaim or "out" if you created the PixClaim.
    - claimer_bank_code [string]: bank_code of the Pix participant that created the PixClaim. ex: "20018183"
    - claimed_bank_code [string]: bank_code of the account donating the PixKey. ex: "20018183"
    - created [datetime.datetime]: creation datetime for the PixClaim. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - updated [datetime.datetime]: update datetime for the PixClaim. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, account_created, account_number, account_type, branch_code, name, tax_id, key_id, tags=None, id=None,
                 status=None, type=None, key_type=None, flow=None, claimer_bank_code=None, claimed_bank_code=None, created=None,
                 updated=None):
        Resource.__init__(self, id=id)

        self.account_created = check_datetime(account_created)
        self.account_number = account_number
        self.account_type = account_type
        self.branch_code = branch_code
        self.name = name
        self.tax_id = tax_id
        self.key_id = key_id
        self.tags = tags
        self.status = status
        self.type = type
        self.key_type = key_type
        self.flow = flow
        self.claimer_bank_code = claimer_bank_code
        self.claimed_bank_code = claimed_bank_code
        self.created = check_datetime(created)
        self.updated = check_datetime(updated)


_resource = {"class": PixClaim, "name": "PixClaim"}


def create(claim, user=None):
    """# Create a PixClaim object
    Create a PixClaim to request the transfer of a PixKey to an account
    hosted at other Pix participants in the Stark Infra API.
    ## Parameters (required):
    - claim [PixClaim object]: PixClaim object to be created in the API.
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - PixClaim object with updated attributes.
    """
    return rest.post_single(resource=_resource, entity=claim, user=user)


def get(id, user=None):
    """# Retrieve a PixClaim object
    Retrieve a PixClaim object linked to your Workspace in the Stark Infra API by its id.
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - PixClaim object that corresponds to the given id.
    """
    return rest.get_id(id=id, resource=_resource, user=user)


def query(limit=None, after=None, before=None, status=None, ids=None, type=None, key_type=None, key_id=None, flow=None, tags=None, user=None):
    """# Retrieve PixClaims
    Receive a generator of PixClaim objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None]: date filter for objects created after a specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None]: date filter for objects created before a specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. ex: ["created", "failed", "delivered", "confirmed", "success", "canceled"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - type [string, default None]: filter for the type of retrieved PixClaims. Options: "ownership" or "portability"
    - key_type [string, default None]: filter for the PixKey type of retrieved PixClaims. Options: "cpf", "cnpj", "phone", "email" and "evp"
    - key_id [string, default None]: filter PixClaims linked to a specific PixKey id. ex: "+5511989898989"
    - flow [string, default None]: direction of the Pix Claim. Options: "in" if you received the PixClaim or "out" if you created the PixClaim.
    - tags [list of strings, default None]: list of strings to filter retrieved objects. ex: ["travel", "food"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - generator of PixClaim objects with updated attributes
    """

    return rest.get_stream(
        resource=_resource,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        status=status,
        ids=ids,
        type=type,
        key_type=key_type,
        key_id=key_id,
        flow=flow,
        tags=tags,
        user=user,
    )


def page(cursor=None, limit=None, after=None, before=None, status=None, ids=None, type=None, key_type=None, key_id=None, flow=None, tags=None, user=None):
    """# Retrieve paged PixClaims
    Receive a list of up to 100 PixClaim objects previously created in the Stark Infra API and the cursor to the next page.
    Use this function instead of query if you want to manually page your requests.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call.
    - limit [integer, default 100]: maximum number of objects to be retrieved. Max = 100. ex: 35
    - after [datetime.date or string, default None]: date filter for objects created after a specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None]: date filter for objects created before a specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. ex: ["created", "failed", "delivered", "confirmed", "success", "canceled"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - type [string, default None]: filter for the type of retrieved PixClaims. Options: "ownership" or "portability"
    - key_type [string, default None]: filter for the PixKey type of retrieved PixClaims. Options: "cpf", "cnpj", "phone", "email" and "evp"
    - key_id [string, default None]: filter PixClaims linked to a specific PixKey id. Example: "+5511989898989"
    - flow [string, default None]: direction of the Pix Claim. Options: "in" if you received the PixClaim or "out" if you created the PixClaim.
    - tags [list of strings, default None]: list of strings to filter retrieved objects. ex: ["travel", "food"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of PixClaim objects with updated attributes and cursor to retrieve the next page of PixClaim objects
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
        key_type=key_type,
        key_id=key_id,
        flow=flow,
        tags=tags,
        user=user,
    )


def update(id, status, reason=None, user=None):
    """# Update PixClaim entity
    Update a PixClaim parameters by passing id.
    ## Parameters (required):
    - id [string]: PixClaim id. ex: "5656565656565656"
    - status [string]: patched status for Pix Claim. Options: "confirmed" and "canceled"
    ## Parameters (optional):
    - reason [string, default: "userRequested"]: reason why the PixClaim is being patched. Options: "fraud", "userRequested", "accountClosure"
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - PixClaim with updated attributes
    """
    payload = {
        "reason": reason,
        "status": status,
    }
    return rest.patch_id(resource=_resource, id=id, user=user, payload=payload)
