from ..utils import rest
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime, check_date


class PixKey(Resource):
    """# PixKey object
    PixKeys link bank account information to key ids.
    Key ids are a convenient way to search and pass bank account information.
    When you initialize a Pix Key, the entity will not be automatically
    created in the Stark Infra API. The 'create' function sends the objects
    to the Stark Infra API and returns the created object.
    ## Parameters (required):
    - account_created [datetime.date, datetime.datetime or string]: opening Date or DateTime for the linked account. ex: "2022-01-01T12:00:00:00"
    - account_number [string]: number of the linked account. ex: "76543"
    - account_type [string]: type of the linked account. Options: "checking", "savings", "salary" or "payment"
    - branch_code [string]: branch code of the linked account. ex: 1234"
    - name [string]: holder's name of the linked account. ex: "Jamie Lannister"
    - tax_id [string]: holder's taxId (CPF/CNPJ) of the linked account. ex: "012.345.678-90"
    ## Parameters (optional):
    - id [string, default None]: id of the registered PixKey. Allowed types are: CPF, CNPJ, phone number or email. If this parameter is not passed, an EVP will be created. ex: "+5511989898989"
    - tags [list of strings, default []]]: list of strings for reference when searching for PixKeys. ex: ["employees", "monthly"]
    ## Attributes (return-only):
    - owned [datetime.datetime]: datetime when the key was owned by the holder. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - owner_type [string]: type of the owner of the PixKey. Options: "business" or "individual"
    - status [string]: current PixKey status. Options: "created", "registered", "canceled", "failed"
    - bank_code [string]: bank_code of the account linked to the Pix Key. ex: "20018183"
    - bank_name [string]: name of the bank that holds the account linked to the PixKey. ex: "StarkBank"
    - type [string]: type of the PixKey. Options: "cpf", "cnpj", "phone", "email" and "evp"
    - created [datetime.datetime]: creation datetime for the PixKey. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, account_created, account_number, account_type, branch_code, name, tax_id, id=None, tags=None,
                 owned=None, owner_type=None, status=None, bank_code=None, bank_name=None, type=None, created=None):
        Resource.__init__(self, id=id)

        self.account_created = check_datetime(account_created)
        self.account_number = account_number
        self.account_type = account_type
        self.branch_code = branch_code
        self.name = name
        self.tax_id = tax_id
        self.tags = tags
        self.owned = check_datetime(owned)
        self.owner_type = owner_type
        self.status = status
        self.bank_code = bank_code
        self.bank_name = bank_name
        self.type = type
        self.created = check_datetime(created)


_resource = {"class": PixKey, "name": "PixKey"}


def create(key, user=None):
    """# Create a PixKey object
    Create a PixKey linked to a specific account in the Stark Infra API
    ## Parameters (optional):
    - key [PixKey object]: PixKey object to be created in the API.
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - PixKey object with updated attributes.
    """
    return rest.post_single(resource=_resource, entity=key, user=user)


def get(id, payer_id, end_to_end_id=None, user=None):
    """# Retrieve a PixKey object
    Retrieve the PixKey object linked to your Workspace in the Stark Infra API by its id.
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    - payer_id [string]: tax id (CPF/CNPJ) of the individual or business requesting the PixKey information. This id is used by the Central Bank to limit request rates. ex: "20.018.183/0001-80"
    ## Parameters (optional):
    - end_to_end_id [string, default None]: central bank's unique transaction id. If the request results in the creation of a PixRequest, the same endToEndId should be used. If this parameter is not passed, one endToEndId will be automatically created. Example: "E00002649202201172211u34srod19le"
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - PixKey object that corresponds to the given id.
    """

    return rest.get_id(id=id, payer_id=payer_id, end_to_end_id=end_to_end_id, resource=_resource, user=user)


def query(limit=None, after=None, before=None, status=None, tags=None, ids=None, type=None, user=None):
    """# Retrieve PixKeys
    Receive a generator of PixKey objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None]: date filter for objects created after a specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None]: date filter for objects created before a specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. ex: ["created", "registered", "canceled", "failed"]
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - type [string, default None]: filter for the type of retrieved PixKeys. Options: "cpf", "cnpj", "phone", "email" and "evp"
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - generator of PixKey objects with updated attributes
    """
    return rest.get_stream(
        resource=_resource,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        status=status,
        tags=tags,
        ids=ids,
        type=type,
        user=user,
    )


def page(cursor=None, limit=None, after=None, before=None, status=None, tags=None, ids=None, type=None,
         user=None):
    """# Retrieve paged PixKeys
    Receive a generator of PixKey objects previously created in the Stark Infra API
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call.
    - limit [integer, default 100]: maximum number of objects to be retrieved. Max = 100. ex: 35
    - after [datetime.date or string, default None]: date filter for objects created after a specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None]: date filter for objects created before a specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. ex: ["created", "registered", "canceled", "failed"]
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - type [string, default None]: filter for the type of retrieved PixKeys. Options: "cpf", "cnpj", "phone", "email" and "evp"
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - cursor to retrieve the next page of PixKey objects
    - generator of PixKey objects with updated attributes
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
        type=type,
        user=user,
    )


def update(id, reason, account_created=None, account_number=None, account_type=None, branch_code=None, name=None,
           user=None):
    """# Update PixKey entity
    Update a PixKey parameters by passing id.
    ## Parameters (required):
    - id [string]: PixKey id. Allowed types are: CPF, CNPJ, phone number or email. ex: "5656565656565656"
    - reason [string]: reason why the PixKey is being patched. Options: "branchTransfer", "reconciliation" or "userRequested"
    ## Parameters (optional):
    - account_created [datetime.date, datetime.datetime or string, default None]: opening Date or DateTime for the account to be linked. ex: "2022-01-01"
    - account_number [string, default None]: number of the account to be linked. ex: "76543"
    - account_type [string, default None]: type of the account to be linked. Options: "checking", "savings", "salary" or "payment"
    - branch_code [string, default None]: branch code of the account to be linked. ex: 1234"
    - name [string, default None]: holder's name of the account to be linked. ex: "Jamie Lannister"
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - PixKey with updated attributes
    """
    payload = {
        "reason": reason,
        "account_created": account_created,
        "account_number": account_number,
        "account_type": account_type,
        "branch_code": branch_code,
        "name": name,
    }
    return rest.patch_id(resource=_resource, id=id, user=user, payload=payload)


def cancel(id, user=None):
    """# Cancel a PixKey entity
    Cancel a PixKey entity previously created in the Stark Infra API
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - canceled pixKey object
    """
    return rest.delete_id(resource=_resource, id=id, user=user)
