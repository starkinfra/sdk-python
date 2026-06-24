from ..utils import rest
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime, check_date


class PixInternalTransactionReport(Resource):
    """# PixInternalTransactionReport object
    PixInternalTransactionReports are used to report transactions that happened
    internally, outside of the SPI, to the Central Bank so they are reflected in
    the participant's statements.
    When you initialize a PixInternalTransactionReport, the entity will not be
    automatically created in the Stark Infra API. The 'create' function sends the
    objects to the Stark Infra API and returns the list of created objects.
    ## Parameters (required):
    - amount [integer]: amount of the reported transaction in cents. ex: 1234 (= R$ 12.34)
    - created [datetime.datetime or string]: datetime when the reported transaction occurred. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - end_to_end_id [string]: central bank's unique transaction id. ex: "E20018183202201201213u34sav898j"
    - method [string]: method used to process the reported transaction. ex: "manual", "key", "staticQrcode", "dynamicQrcode"
    - reference_type [string]: type of the reported transaction. Options: "request", "reversal"
    - sender_account_number [string]: sender's bank account number. ex: "76543"
    - sender_branch_code [string]: sender's bank account branch code. ex: "1234"
    - sender_account_type [string]: sender's bank account type. Options: "checking", "savings", "salary" or "payment"
    - sender_bank_code [string]: sender's participant code (ISPB). ex: "20018183"
    - sender_tax_id [string]: sender's tax ID (CPF/CNPJ) with or without formatting. ex: "01234567890" or "20.018.183/0001-80"
    - receiver_account_number [string]: receiver's bank account number. ex: "76543"
    - receiver_branch_code [string]: receiver's bank account branch code. ex: "1234"
    - receiver_account_type [string]: receiver's bank account type. Options: "checking", "savings", "salary" or "payment"
    - receiver_bank_code [string]: receiver's participant code (ISPB). ex: "20018183"
    - receiver_tax_id [string]: receiver's tax ID (CPF/CNPJ) with or without formatting. ex: "01234567890" or "20.018.183/0001-80"
    ## Parameters (optional):
    - receiver_key_id [string, default None]: receiver's Pix Key used in the reported transaction. ex: "+5511989898989"
    - return_id [string, default None]: central bank's unique reversal transaction id. Required when reference_type is "reversal". ex: "D20018183202201201213u34sav898j"
    ## Attributes (return-only):
    - id [string]: unique id returned when the PixInternalTransactionReport is created. ex: "5656565656565656"
    - status [string]: current PixInternalTransactionReport status. ex: "created", "processing", "success", "failed"
    - updated [datetime.datetime]: latest update datetime for the PixInternalTransactionReport. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, amount, created, end_to_end_id, method, reference_type, sender_account_number,
                 sender_branch_code, sender_account_type, sender_bank_code, sender_tax_id, receiver_account_number,
                 receiver_branch_code, receiver_account_type, receiver_bank_code, receiver_tax_id, receiver_key_id=None,
                 return_id=None, id=None, status=None, updated=None):
        Resource.__init__(self, id=id)

        self.amount = amount
        self.created = check_datetime(created)
        self.end_to_end_id = end_to_end_id
        self.method = method
        self.reference_type = reference_type
        self.sender_account_number = sender_account_number
        self.sender_branch_code = sender_branch_code
        self.sender_account_type = sender_account_type
        self.sender_bank_code = sender_bank_code
        self.sender_tax_id = sender_tax_id
        self.receiver_account_number = receiver_account_number
        self.receiver_branch_code = receiver_branch_code
        self.receiver_account_type = receiver_account_type
        self.receiver_bank_code = receiver_bank_code
        self.receiver_tax_id = receiver_tax_id
        self.receiver_key_id = receiver_key_id
        self.return_id = return_id
        self.status = status
        self.updated = check_datetime(updated)


_resource = {"class": PixInternalTransactionReport, "name": "PixInternalTransactionReport"}


def create(reports, user=None):
    """# Create PixInternalTransactionReports
    Send a list of PixInternalTransactionReport objects for creation at the Stark Infra API
    ## Parameters (required):
    - reports [list of PixInternalTransactionReport objects]: list of PixInternalTransactionReport objects to be created in the API
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of PixInternalTransactionReport objects with updated attributes
    """
    return rest.post_multi(resource=_resource, entities=reports, user=user)


def get(id, user=None):
    """# Retrieve a specific PixInternalTransactionReport
    Receive a single PixInternalTransactionReport object previously created in the Stark Infra API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - PixInternalTransactionReport object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def query(limit=None, after=None, before=None, status=None, ids=None, user=None):
    """# Retrieve PixInternalTransactionReports
    Receive a generator of PixInternalTransactionReport objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None]: date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None]: date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. ex: ["created", "processing", "success", "failed"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - generator of PixInternalTransactionReport objects with updated attributes
    """
    return rest.get_stream(
        resource=_resource,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        status=status,
        ids=ids,
        user=user,
    )


def page(cursor=None, limit=None, after=None, before=None, status=None, ids=None, user=None):
    """# Retrieve paged PixInternalTransactionReports
    Receive a list of up to 100 PixInternalTransactionReport objects previously created in the Stark Infra API and the cursor to the next page.
    Use this function instead of query if you want to manually page your requests.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - limit [integer, default 100]: maximum number of objects to be retrieved. It must be an integer between 1 and 100. ex: 50
    - after [datetime.date or string, default None]: date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None]: date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. ex: ["created", "processing", "success", "failed"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of PixInternalTransactionReport objects with updated attributes
    - cursor to retrieve the next page of PixInternalTransactionReport objects
    """
    return rest.get_page(
        resource=_resource,
        cursor=cursor,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        status=status,
        ids=ids,
        user=user,
    )
