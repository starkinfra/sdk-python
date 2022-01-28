from ..utils import rest
from ..utils.checks import check_datetime, check_date
from ..utils.resource import Resource


class PixRequest(Resource):
    """# PixRequest object
    When you initialize a PixRequest, the entity will not be automatically
    created in the Stark Infra API. The 'create' function sends the objects
    to the Stark Infra API and returns the list of created objects.
    ## Parameters (required):
    - amount [integer]: amount in cents to be transferred. ex: 1234 (= R$ 12.34)
    - external_id [string, default None]: url safe string that must be unique among all your pix requests. Duplicated external_ids will cause failures. By default, this parameter will block any pix request that repeats amount and receiver information on the same date. ex: "my-internal-id-123456"
    - sender_name [string]: sender full name. ex: "Anthony Edward Stark"
    - sender_tax_id [string]: sender tax ID (CPF or CNPJ) with or without formatting. ex: "01234567890" or "20.018.183/0001-80"
    - sender_branch_code [string]: sender bank account branch. Use '-' in case there is a verifier digit. ex: "1357-9"
    - sender_account_number [string]: sender bank account number. Use '-' before the verifier digit. ex: "876543-2"
    - sender_account_type [string, default "checking"]: sender bank account type. ex: "checking", "savings", "salary" or "payment"
    - receiver_name [string]: receiver full name. ex: "Anthony Edward Stark"
    - receiver_tax_id [string]: receiver tax ID (CPF or CNPJ) with or without formatting. ex: "01234567890" or "20.018.183/0001-80"
    - receiver_bank_code [string]: code of the receiver bank institution in Brazil. If an ISPB (8 digits) is informed. ex: "20018183" or "341"
    - receiver_account_number [string]: receiver bank account number. Use '-' before the verifier digit. ex: "876543-2"
    - receiver_branch_code [string]: receiver bank account branch. Use '-' in case there is a verifier digit. ex: "1357-9"
    - receiver_account_type [string]: receiver bank account type. ex: "checking", "savings", "salary" or "payment"
    - end_to_end_id [string]: central bank's unique transaction ID. ex: "E79457883202101262140HHX553UPqeq"
    ## Parameters (optional):
    - sender_account_type [string, default "checking"]: Sender bank account type. ex: "checking", "savings", "salary" or "payment"
    - sender_bank_code [string]: code of the sender bank institution in Brazil. If an ISPB (8 digits) is informed. ex: "20018183" or "341"
    - reconciliation_id [string]: Reconciliation ID linked to this payment. ex: "txId", "payment-123"
    - receiver_key_id [string]:
    - description [string, default None]: optional description to override default description to be shown in the bank statement. ex: "Payment for service #1234"
    - flow [string]: money flow in or out of the account. ex: "in" or "out"
    - method [string]:
    - initiator_tax_id [string]:
    - cash_amount [string]:
    - cashier_bank_code [string]:
    - cashier_type [string]:
    - tags [string]: [list of strings]: list of strings for reference when searching for pix requests. ex: ["employees", "monthly"]
    ## Attributes (return-only):
    - id [string, default None]: unique id returned when the pix request is created. ex: "5656565656565656"
    - fee [integer, default None]: fee charged when pix request o is paid. ex: 200 (= R$ 2.00)
    - status [string]: current PixRequest status. ex: "registered" or "paid"
    - transaction_id [string]: ledger transaction ids linked to this pix request. ex: ["19827356981273"]
    - created [datetime.datetime, default None]: creation datetime for the pix request. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - updated [datetime.datetime, default None]: latest update datetime for the pix request. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, amount,  external_id, sender_name, sender_tax_id, sender_branch_code,
                 sender_account_number, sender_account_type, receiver_name, receiver_tax_id, receiver_bank_code,
                 receiver_account_number, receiver_branch_code, receiver_account_type, end_to_end_id,
                 receiver_key_id=None, sender_bank_code=None, reconciliation_id=None, description=None, flow=None,
                 method=None, initiator_tax_id=None, cash_amount=None, cashier_bank_code=None, cashier_type=None,
                 tags=None, id=None, fee=None, status=None, transaction_id=None, created=None, updated=None):
        Resource.__init__(self, id=id)

        self.amount = amount
        self.external_id = external_id
        self.sender_name = sender_name
        self.sender_tax_id = sender_tax_id
        self.sender_bank_code = sender_bank_code
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
        self.reconciliation_id = reconciliation_id
        self.description = description
        self.method = method
        self.initiator_tax_id = initiator_tax_id
        self.cash_amount = cash_amount
        self.cashier_type = cashier_type
        self.cashier_bank_code = cashier_bank_code
        self.flow = flow
        self.tags = tags
        self.fee = fee
        self.status = status
        self.transaction_id = transaction_id
        self.created = check_datetime(created)
        self.updated = check_datetime(updated)


_resource = {"class": PixRequest, "name": "PixRequest"}


def create(requests, user=None):
    """# Create PixRequest
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


def query(limit=None, after=None, before=None, transaction_ids=None, status=None, tags=None, ids=None, user=None):
    """# Retrieve PixRequests
    Receive a generator of PixRequest objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None]: date filter for objects created or updated only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None]: date filter for objects created or updated only before specified date. ex: datetime.date(2020, 3, 10)
    - transaction_ids [list of strings, default None]: list of transaction IDs linked to the desired pix requests. ex: ["5656565656565656", "4545454545454545"]
    - status [string, default None]: filter for status of retrieved objects. ex: "success" or "failed"
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - generator of PixRequest objects with updated attributes
    """
    return rest.get_stream(
        resource=_resource,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        transaction_ids=transaction_ids,
        status=status,
        tags=tags,
        ids=ids,
        user=user,
    )


def page(cursor=None, limit=None, after=None, before=None, transaction_ids=None, status=None, tags=None, ids=None, user=None):
    """# Retrieve paged PixRequests
    Receive a list of up to 100 PixRequest objects previously created in the Stark Infra API and the cursor to the next page.
    Use this function instead of query if you want to manually page your requests.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None]: date filter for objects created or updated only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None]: date filter for objects created or updated only before specified date. ex: datetime.date(2020, 3, 10)
    - transaction_ids [list of strings, default None]: list of transaction IDs linked to the desired pix requests. ex: ["5656565656565656", "4545454545454545"]
    - status [string, default None]: filter for status of retrieved objects. ex: "success" or "failed"
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
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
        transaction_ids=transaction_ids,
        status=status,
        tags=tags,
        ids=ids,
        user=user,
    )
