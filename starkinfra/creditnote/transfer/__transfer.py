from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime, check_datetime_or_date


class Transfer(Resource):
    """# creditnote.Transfer object
    Transfer object to be created and sent to the credit receiver.
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

    def __init__(self, amount, name, tax_id, bank_code, branch_code, account_number, account_type=None,
                 external_id=None, scheduled=None, description=None, transaction_ids=None, fee=None, tags=None,
                 status=None, id=None, created=None, updated=None):
        Resource.__init__(self, id=id)

        self.tax_id = tax_id
        self.amount = amount
        self.name = name
        self.bank_code = bank_code
        self.branch_code = branch_code
        self.account_number = account_number
        self.account_type = account_type
        self.external_id = external_id
        self.scheduled = check_datetime_or_date(scheduled)
        self.description = description
        self.tags = tags
        self.fee = fee
        self.status = status
        self.created = check_datetime(created)
        self.updated = check_datetime(updated)
        self.transaction_ids = transaction_ids


_resource = {"class": Transfer, "name": "Transfer"}
