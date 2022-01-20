from ..utils import rest
from ..utils.checks import check_datetime, check_date
from ..utils.resource import Resource


class PixRequest(Resource):
    """# Transfer object
    When you initialize a Transfer, the entity will not be automatically
    created in the Stark Bank API. The 'create' function sends the objects
    to the Stark Bank API and returns the list of created objects.
    ## Parameters (required):
    - amount [integer]: amount in cents to be transferred. ex: 1234 (= R$ 12.34)
    - name [string]: receiver full name. ex: "Anthony Edward Stark"
    - tax_id [string]: receiver tax ID (CPF or CNPJ) with or without formatting. ex: "01234567890" or "20.018.183/0001-80"
    - bank_code [string]: code of the receiver bank institution in Brazil. If an ISPB (8 digits) is informed, a PIX transfer will be created, else a TED will be issued. ex: "20018183" or "341"
    - branch_code [string]: receiver bank account branch. Use '-' in case there is a verifier digit. ex: "1357-9"
    - account_number [string]: receiver bank account number. Use '-' before the verifier digit. ex: "876543-2"
    ## Parameters (optional):
    - account_type [string, default "checking"]: Receiver bank account type. This parameter only has effect on Pix Transfers. ex: "checking", "savings", "salary" or "payment"
    - external_id [string, default None]: url safe string that must be unique among all your transfers. Duplicated external_ids will cause failures. By default, this parameter will block any transfer that repeats amount and receiver information on the same date. ex: "my-internal-id-123456"
    - scheduled [datetime.date, datetime.datetime or string, default now]: date or datetime when the transfer will be processed. May be pushed to next business day if necessary. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - description [string, default None]: optional description to override default description to be shown in the bank statement. ex: "Payment for service #1234"
    - tags [list of strings]: list of strings for reference when searching for transfers. ex: ["employees", "monthly"]
    ## Attributes (return-only):
    - id [string, default None]: unique id returned when the transfer is created. ex: "5656565656565656"
    - fee [integer, default None]: fee charged when the Transfer is processed. ex: 200 (= R$ 2.00)
    - status [string, default None]: current transfer status. ex: "success" or "failed"
    - transaction_ids [list of strings, default None]: ledger Transaction IDs linked to this Transfer (if there are two, the second is the chargeback). ex: ["19827356981273"]
    - created [datetime.datetime, default None]: creation datetime for the transfer. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - updated [datetime.datetime, default None]: latest update datetime for the transfer. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, amount, external_id, sender_name, sender_tax_id, sender_branch_code,
                 sender_account_number, sender_account_type, receiver_name, receiver_tax_id, receiver_bank_code,
                 receiver_account_number, receiver_branch_code, receiver_account_type, end_to_end_id,
                 sender_bank_code=None, fee=None, status=None, transaction_ids=None, reconciliation_id=None, description=None,
                 receiver_key_id=None,  flow=None, method=None, initiator_tax_id=None, cash_amount=None, cashier_bank_code=None,
                 cashier_type=None, tags=None, created=None, updated=None, id=None):
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
        self.receiver_branch_code = receiver_branch_code
        self.receiver_account_number = receiver_account_number
        self.receiver_account_type = receiver_account_type
        self.end_to_end_id = end_to_end_id
        self.fee = fee
        self.status = status
        self.transaction_ids = transaction_ids
        self.reconciliation_id = reconciliation_id
        self.description = description
        self.receiver_key_id = receiver_key_id
        self.flow = flow
        self.method = method
        self.initiator_tax_id = initiator_tax_id
        self.cash_amount = cash_amount
        self.cashier_bank_code = cashier_bank_code
        self.cashier_type = cashier_type
        self.tags = tags
        self.created = check_datetime(created)
        self.updated = check_datetime(updated)


_resource = {"class": PixRequest, "name": "PixRequest"}


def create(requests, user=None):
    """# Create Transfers
    Send a list of Transfer objects for creation in the Stark Bank API
    ## Parameters (required):
    - transfers [list of Transfer objects]: list of Transfer objects to be created in the API
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkbank.user was set before function call
    ## Return:
    - list of Transfer objects with updated attributes
    """
    return rest.post_multi(resource=_resource, entities=requests, user=user)


def query(limit=None, after=None, before=None, transaction_ids=None, status=None, tax_id=None, sort=None, tags=None, ids=None, user=None):
    """# Retrieve Transfers
    Receive a generator of Transfer objects previously created in the Stark Bank API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None]: date filter for objects created or updated only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None]: date filter for objects created or updated only before specified date. ex: datetime.date(2020, 3, 10)
    - transaction_ids [list of strings, default None]: list of transaction IDs linked to the desired transfers. ex: ["5656565656565656", "4545454545454545"]
    - status [string, default None]: filter for status of retrieved objects. ex: "success" or "failed"
    - tax_id [string, default None]: filter for transfers sent to the specified tax ID. ex: "012.345.678-90"
    - sort [string, default "-created"]: sort order considered in response. Valid options are "created", "-created", "updated" or "-updated".
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkbank.user was set before function call
    ## Return:
    - generator of Transfer objects with updated attributes
    """
    return rest.get_stream(
        resource=_resource,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        transaction_ids=transaction_ids,
        status=status,
        tax_id=tax_id,
        sort=sort,
        tags=tags,
        ids=ids,
        user=user,
    )


def page(cursor=None, limit=None, after=None, before=None, transaction_ids=None, status=None, tax_id=None, sort=None, tags=None, ids=None, user=None):
    """# Retrieve paged Transfers
    Receive a list of up to 100 Transfer objects previously created in the Stark Bank API and the cursor to the next page.
    Use this function instead of query if you want to manually page your requests.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - limit [integer, default 100]: maximum number of objects to be retrieved. It must be an integer between 1 and 100. ex: 50
    - after [datetime.date or string, default None]: date filter for objects created or updated only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None]: date filter for objects created or updated only before specified date. ex: datetime.date(2020, 3, 10)
    - transaction_ids [list of strings, default None]: list of transaction IDs linked to the desired transfers. ex: ["5656565656565656", "4545454545454545"]
    - status [string, default None]: filter for status of retrieved objects. ex: "success" or "failed"
    - tax_id [string, default None]: filter for transfers sent to the specified tax ID. ex: "012.345.678-90"
    - sort [string, default "-created"]: sort order considered in response. Valid options are "created", "-created", "updated" or "-updated".
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkbank.user was set before function call
    ## Return:
    - list of Transfer objects with updated attributes
    - cursor to retrieve the next page of Transfer objects
    """
    return rest.get_page(
        resource=_resource,
        cursor=cursor,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        transaction_ids=transaction_ids,
        status=status,
        tax_id=tax_id,
        sort=sort,
        tags=tags,
        ids=ids,
        user=user,
    )
