from json import dumps
from ..utils import rest
from ..utils.parse import parse_and_verify
from starkcore.utils.api import api_json
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime, check_date


class PixRequest(Resource):
    """# PixRequest object
    PixRequests are used to receive or send instant payments to accounts
    hosted in any Pix participant.
    When you initialize a PixRequest, the entity will not be automatically
    created in the Stark Infra API. The 'create' function sends the objects
    to the Stark Infra API and returns the list of created objects.
    ## Parameters (required):
    - amount [integer]: amount in cents to be transferred. ex: 11234 (= R$ 112.34)
    - external_id [string]: string that must be unique among all your PixRequests. Duplicated external IDs will cause failures. By default, this parameter will block any PixRequests that repeats amount and receiver information on the same date. ex: "my-internal-id-123456"
    - sender_name [string]: sender's full name. ex: "Edward Stark"
    - sender_tax_id [string]: sender's tax ID (CPF or CNPJ) with or without formatting. ex: "01234567890" or "20.018.183/0001-80"
    - sender_branch_code [string]: sender's bank account branch code. Use '-' in case there is a verifier digit. ex: "1357-9"
    - sender_account_number [string]: sender's bank account number. Use '-' before the verifier digit. ex: "876543-2"
    - sender_account_type [string]: sender's bank account type. ex: "checking", "savings", "salary" or "payment"
    - receiver_name [string]: receiver's full name. ex: "Edward Stark"
    - receiver_tax_id [string]: receiver's tax ID (CPF or CNPJ) with or without formatting. ex: "01234567890" or "20.018.183/0001-80"
    - receiver_bank_code [string]: receiver's bank institution code in Brazil. ex: "20018183"
    - receiver_account_number [string]: receiver's bank account number. Use '-' before the verifier digit. ex: "876543-2"
    - receiver_branch_code [string]: receiver's bank account branch code. Use '-' in case there is a verifier digit. ex: "1357-9"
    - receiver_account_type [string]: receiver's bank account type. ex: "checking", "savings", "salary" or "payment"
    - end_to_end_id [string]: central bank's unique transaction ID. ex: "E79457883202101262140HHX553UPqeq"
    ## Parameters (conditionally-required):
    - cashier_type [string]: Cashier's type. Required if the cash_amount is different from 0. Options: "merchant", "participant" and "other"
    - cashier_bank_code [string]: Cashier's bank code. Required if the cash_amount is different from 0. ex: "20018183"
    ## Parameters (optional):
    - cash_amount [integer]: Amount to be withdrawn from the cashier in cents. ex: 1000 (= R$ 10.00)
    - receiver_key_id [string, default None]: receiver's dict key. ex: "20.018.183/0001-80"
    - description [string, default None]: optional description to override default description to be shown in the bank statement. ex: "Payment for service #1234"
    - reconciliation_id [string, default None]: Reconciliation ID linked to this payment. ex: "b77f5236-7ab9-4487-9f95-66ee6eaf1781"
    - initiator_tax_id [string, default None]: Payment initiator's tax id (CPF/CNPJ). ex: "01234567890" or "20.018.183/0001-80"
    - tags [list of strings, default []]: list of strings for reference when searching for PixRequests. ex: ["employees", "monthly"]
    - method [string, default None]: execution  method for thr creation of the Pix. ex: "manual", "payerQrcode", "dynamicQrcode"
    ## Attributes (return-only):
    - id [string]: unique id returned when the PixRequest is created. ex: "5656565656565656"
    - fee [integer]: fee charged when PixRequest is paid. ex: 200 (= R$ 2.00)
    - status [string]: current PixRequest status. ex: "created", "processing", "success", "failed"
    - flow [string]: direction of money flow. ex: "in" or "out"
    - sender_bank_code [string]: sender's bank institution code in Brazil. ex: "20018183"
    - created [datetime.datetime]: creation datetime for the PixRequest. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - updated [datetime.datetime]: latest update datetime for the PixRequest. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, amount, external_id, sender_name, sender_tax_id, sender_branch_code,
                 sender_account_number, sender_account_type, receiver_name, receiver_tax_id, receiver_bank_code,
                 receiver_account_number, receiver_branch_code, receiver_account_type, end_to_end_id,
                 cashier_type=None, cashier_bank_code=None, cash_amount=None, receiver_key_id=None, description=None, 
                 reconciliation_id=None, initiator_tax_id=None, tags=None, method=None, id=None, fee=None,
                 status=None, flow=None, sender_bank_code=None, created=None, updated=None):
        Resource.__init__(self, id=id)

        self.amount = amount
        self.external_id = external_id
        self.sender_name = sender_name
        self.sender_tax_id = sender_tax_id
        self.sender_branch_code = sender_branch_code
        self.sender_account_number = sender_account_number
        self.sender_account_type = sender_account_type
        self.receiver_name = receiver_name
        self.receiver_tax_id = receiver_tax_id
        self.receiver_bank_code = receiver_bank_code
        self.receiver_account_number = receiver_account_number
        self.receiver_branch_code = receiver_branch_code
        self.receiver_account_type = receiver_account_type
        self.end_to_end_id = end_to_end_id
        self.cashier_type = cashier_type
        self.cashier_bank_code = cashier_bank_code
        self.cash_amount = cash_amount
        self.receiver_key_id = receiver_key_id
        self.description = description
        self.reconciliation_id = reconciliation_id
        self.initiator_tax_id = initiator_tax_id
        self.tags = tags
        self.method = method
        self.fee = fee
        self.status = status
        self.flow = flow
        self.sender_bank_code = sender_bank_code
        self.created = check_datetime(created)
        self.updated = check_datetime(updated)


_resource = {"class": PixRequest, "name": "PixRequest"}


def create(requests, user=None):
    """# Create PixRequests
    Send a list of PixRequest objects for creation at the Stark Infra API
    ## Parameters (required):
    - requests [list of PixRequest objects]: list of PixRequest objects to be created in the API
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of PixRequest objects with updated attributes
    """
    return rest.post_multi(resource=_resource, entities=requests, user=user)


def get(id, user=None):
    """# Retrieve a specific PixRequest
    Receive a single PixRequest object previously created in the Stark Infra API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - PixRequest object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def query(limit=None, after=None, before=None, status=None, ids=None, end_to_end_ids=None,
          external_ids=None, tags=None, user=None):
    """# Retrieve PixRequests
    Receive a generator of PixRequest objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None]: date filter for objects created after a specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None]: date filter for objects created before a specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. ex: ["created", "processing", "success", "failed"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - end_to_end_ids [list of strings, default None]: central bank's unique transaction IDs. ex: ["E79457883202101262140HHX553UPqeq", "E79457883202101262140HHX553UPxzx"]
    - external_ids [list of strings, default None]: url safe strings that must be unique among all your PixRequests. Duplicated external IDs will cause failures. By default, this parameter will block any PixRequests that repeats amount and receiver information on the same date. ex: ["my-internal-id-123456", "my-internal-id-654321"]
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - generator of PixRequest objects with updated attributes
    """
    return rest.get_stream(
        resource=_resource,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        status=status,
        ids=ids,
        end_to_end_ids=end_to_end_ids,
        external_ids=external_ids,
        tags=tags,
        user=user,
    )


def page(cursor=None, limit=None, after=None, before=None, status=None, ids=None,
         end_to_end_ids=None, external_ids=None, tags=None, user=None):
    """# Retrieve paged PixRequests
    Receive a list of up to 100 PixRequest objects previously created in the Stark Infra API and the cursor to the next page.
    Use this function instead of query if you want to manually page your requests.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - limit [integer, default 100]: maximum number of objects to be retrieved. Max = 100. ex: 35
    - after [datetime.date or string, default None]: date filter for objects created after a specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None]: date filter for objects created before a specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. ex: ["created", "processing", "success", "failed"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - end_to_end_ids [list of strings, default None]: central bank's unique transaction IDs. ex: ["E79457883202101262140HHX553UPqeq", "E79457883202101262140HHX553UPxzx"]
    - external_ids [list of strings, default None]: url safe strings that must be unique among all your PixRequests. Duplicated external IDs will cause failures. By default, this parameter will block any PixRequests that repeats amount and receiver information on the same date. ex: ["my-internal-id-123456", "my-internal-id-654321"]
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of PixRequest objects with updated attributes
    - cursor to retrieve the next page of PixRequest objects
    """
    return rest.get_page(
        resource=_resource,
        cursor=cursor,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        status=status,
        ids=ids,
        end_to_end_ids=end_to_end_ids,
        external_ids=external_ids,
        tags=tags,
        user=user,
    )


def parse(content, signature, user=None):
    """# Create a single verified PixRequest object from a content string
    Create a single PixRequest object from a content string received from a handler listening at the request url.
    If the provided digital signature does not check out with the StarkInfra public key, a
    starkinfra.error.InvalidSignatureError will be raised.
    ## Parameters (required):
    - content [string]: response content from request received at user endpoint (not parsed)
    - signature [string]: base-64 digital signature received at response header "Digital-Signature"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - Parsed PixRequest object
    """
    request = parse_and_verify(
        content=content,
        signature=signature,
        user=user,
        resource=_resource
    )

    request.fee = request.fee or 0
    request.tags = request.tags or []
    request.external_id = request.external_id or ""
    request.description = request.description or ""
    
    return request


def response(status, reason=None):
    """# Helps you respond to a PixRequest authorization.
    Authorization requests will be posted at your registered
    endpoint whenever inbound PixRequests are received.
    ## Parameters (required):
    - status [string]: response to the authorization. ex: "approved" or "denied"
    ## Parameters (conditionally required):
    - reason [string, default None]: denial reason. Required if the status is "denied". Options: "invalidAccountNumber", "blockedAccount", "accountClosed", "invalidAccountType", "invalidTransactionType", "taxIdMismatch", "invalidTaxId", "orderRejected", "reversalTimeExpired", "settlementFailed"
    ## Return:
    - Dumped JSON string that must be returned to us
    """
    params = {
        "authorization": {
            "status": status,
            "reason": reason,
        }
    }
    return dumps(api_json(params))
