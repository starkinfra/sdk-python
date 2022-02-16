from ..utils import rest
from ..utils.checks import check_datetime, check_date
from ..utils.resource import Resource
from ..utils.parse import parse_and_verify


class PixRequest(Resource):
    """# PixRequest object
    When you initialize a PixRequest, the entity will not be automatically
    created in the Stark Infra API. The 'create' function sends the objects
    to the Stark Infra API and returns the list of created objects.
    ## Parameters (required):
    - amount [integer]: amount in cents to be transferred. ex: 11234 (= R$ 112.34)
    - external_id [string]: url safe string that must be unique among all your PixRequests. Duplicated external IDs will cause failures. By default, this parameter will block any PixRequests that repeats amount and receiver information on the same date. ex: "my-internal-id-123456"
    - sender_name [string]: sender's full name. ex: "Anthony Edward Stark"
    - sender_tax_id [string]: sender's tax ID (CPF or CNPJ) with or without formatting. ex: "01234567890" or "20.018.183/0001-80"
    - sender_branch_code [string]: sender's bank account branch code. Use '-' in case there is a verifier digit. ex: "1357-9"
    - sender_account_number [string]: sender's bank account number. Use '-' before the verifier digit. ex: "876543-2"
    - sender_account_type [string, default "checking"]: sender's bank account type. ex: "checking", "savings", "salary" or "payment"
    - receiver_name [string]: receiver's full name. ex: "Anthony Edward Stark"
    - receiver_tax_id [string]: receiver's tax ID (CPF or CNPJ) with or without formatting. ex: "01234567890" or "20.018.183/0001-80"
    - receiver_bank_code [string]: receiver's bank institution code in Brazil. ex: "20018183" or "341"
    - receiver_account_number [string]: receiver's bank account number. Use '-' before the verifier digit. ex: "876543-2"
    - receiver_branch_code [string]: receiver's bank account branch code. Use '-' in case there is a verifier digit. ex: "1357-9"
    - receiver_account_type [string]: receiver's bank account type. ex: "checking", "savings", "salary" or "payment"
    - end_to_end_id [string]: central bank's unique transaction ID. ex: "E79457883202101262140HHX553UPqeq"
    ## Parameters (optional):
    - receiver_key_id [string, default None]: Receiver's dict key. Example: tax_id (CPF/CNPJ).
    - description [string, default None]: optional description to override default description to be shown in the bank statement. ex: "Payment for service #1234"
    - reconciliation_id [string, default None]: Reconciliation ID linked to this payment. ex: "b77f5236-7ab9-4487-9f95-66ee6eaf1781"
    - initiator_tax_id [string, default None]: Payment initiator's tax id (CPF/CNPJ). ex: "01234567890" or "20.018.183/0001-80"
    - cash_amount [integer, default None]: Amount to be withdrawal from the cashier in cents. ex: 1000 (= R$ 10.00)
    - cashier_bank_code [string, default None]: Cashier's bank code. ex: "00000000"
    - cashier_type [string, default None]: Cashier's type. ex: [merchant, other, participant]
    - tags [list of strings, default None]: list of strings for reference when searching for PixRequests. ex: ["employees", "monthly"]
    - method [string, default None]: execution  method for thr creation of the PIX. ex: "manual", "payerQrcode", "dynamicQrcode".
    ## Attributes (return-only):
    - id [string, default None]: unique id returned when the PixRequest is created. ex: "5656565656565656"
    - fee [integer, default None]: fee charged when PixRequest is paid. ex: 200 (= R$ 2.00)
    - status [string, default None]: current PixRequest status. ex: "registered" or "paid"
    - flow [string, default None]: direction of money flow. ex: "in" or "out"
    - sender_bank_code [string, default None]: sender's bank institution code in Brazil. If an ISPB (8 digits) is informed. ex: "20018183" or "341"
    - created [datetime.datetime, default None]: creation datetime for the PixRequest. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - updated [datetime.datetime, default None]: latest update datetime for the PixRequest. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, amount, external_id, sender_name, sender_tax_id, sender_branch_code,
                 sender_account_number, sender_account_type, receiver_name, receiver_tax_id, receiver_bank_code,
                 receiver_account_number, receiver_branch_code, receiver_account_type, end_to_end_id,
                 receiver_key_id=None, description=None, reconciliation_id=None, initiator_tax_id=None,
                 cash_amount=None, cashier_bank_code=None, cashier_type=None, tags=None, method=None, id=None, fee=None,
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
        self.receiver_key_id = receiver_key_id
        self.description = description
        self.reconciliation_id = reconciliation_id
        self.initiator_tax_id = initiator_tax_id
        self.cash_amount = cash_amount
        self.cashier_bank_code = cashier_bank_code
        self.cashier_type = cashier_type
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
    Send a list of PixRequest objects for creation in the Stark Infra API
    ## Parameters (required):
    - requests [list of PixRequest objects]: list of PixRequest objects to be created in the API
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
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
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - PixRequest object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def query(fields=None, limit=None, after=None, before=None, status=None, tags=None, ids=None, end_to_end_id=None,
          external_id=None, user=None):
    """# Retrieve PixRequests
    Receive a generator of PixRequest objects previously created in the Stark Infra API
    ## Parameters (optional):
    - fields [list of strings, default None]: parameters to be retrieved from PixRequest objects. ex: ["amount", "id"]
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None]: date filter for objects created or updated only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None]: date filter for objects created or updated only before specified date. ex: datetime.date(2020, 3, 10)
    - status [string, default None]: filter for status of retrieved objects. ex: "success" or "failed"
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - end_to_end_ids [list of strings, default None]: central bank's unique transaction IDs. ex: ["E79457883202101262140HHX553UPqeq", "E79457883202101262140HHX553UPxzx"]
    - external_ids [list of strings, default None]: url safe strings that must be unique among all your PixRequests. Duplicated external IDs will cause failures. By default, this parameter will block any PixRequests that repeats amount and receiver information on the same date. ex: ["my-internal-id-123456", "my-internal-id-654321"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - generator of PixRequest objects with updated attributes
    """
    return rest.get_stream(
        resource=_resource,
        fields=fields,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        status=status,
        tags=tags,
        ids=ids,
        end_to_end_id=end_to_end_id,
        external_id=external_id,
        user=user,
    )


def page(cursor=None, fields=None, limit=None, after=None, before=None, status=None, tags=None, ids=None,
         end_to_end_id=None, external_id=None, user=None):
    """# Retrieve paged PixRequests
    Receive a list of up to 100 PixRequest objects previously created in the Stark Infra API and the cursor to the next page.
    Use this function instead of query if you want to manually page your requests.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - fields [list of strings, default None]: parameters to be retrieved from PixRequest objects. ex: ["amount", "id"]
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None]: date filter for objects created or updated only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None]: date filter for objects created or updated only before specified date. ex: datetime.date(2020, 3, 10)
    - status [string, default None]: filter for status of retrieved objects. ex: "success" or "failed"
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - end_to_end_ids [list of strings, default None]: central bank's unique transaction IDs. ex: ["E79457883202101262140HHX553UPqeq", "E79457883202101262140HHX553UPxzx"]
    - external_ids [list of strings, default None]: url safe strings that must be unique among all your PixRequests. Duplicated external IDs will cause failures. By default, this parameter will block any PixRequests that repeats amount and receiver information on the same date. ex: ["my-internal-id-123456", "my-internal-id-654321"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - list of PixRequest objects with updated attributes
    - cursor to retrieve the next page of PixRequest objects
    """
    return rest.get_page(
        resource=_resource,
        cursor=cursor,
        fields=fields,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        status=status,
        tags=tags,
        ids=ids,
        end_to_end_id=end_to_end_id,
        external_id=external_id,
        user=user,
    )


def parse(content, signature, user=None):
    """# Create single authorized PixReversal object from a content string
    Create a single PixRequest object from a content string received from a handler listening at a subscribed user endpoint.
    If the provided digital signature does not check out with the StarkInfra public key, a
    starkinfra.exception.InvalidSignatureException will be raised.
    ## Parameters (required):
    - content [string]: response content from request received at user endpoint (not parsed)
    - signature [string]: base-64 digital signature received at response header "Digital-Signature"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - Parsed PixReversal object
    """

    return parse_and_verify(content, signature, user, _resource)
