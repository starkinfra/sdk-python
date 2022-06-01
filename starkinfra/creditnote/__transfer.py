from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime, check_datetime_or_date


class Transfer(Resource):
    """# creditnote.Transfer object
    Transfer sent to the credit receiver after the contract is signed.
    ## Parameters (required):
    - name [string]: receiver full name. ex: "Anthony Edward Stark"
    - tax_id [string]: receiver tax ID (CPF or CNPJ) with or without formatting. ex: "01234567890" or "20.018.183/0001-80"
    - bank_code [string]: code of the receiver bank institution in Brazil. ex: "20018183" or "341"
    - branch_code [string]: receiver bank account branch. Use '-' in case there is a verifier digit. ex: "1357-9"
    - account_number [string]: receiver bank account number. Use '-' before the verifier digit. ex: "876543-2"
    ## Parameters (optional):
    - account_type [string, default "checking"]: Receiver bank account type. This parameter only has effect on Pix Transfers. ex: "checking", "savings", "salary" or "payment"
    - tags [list of strings, default []]: list of strings for reference when searching for transfers. ex: ["employees", "monthly"]
    ## Attributes (return-only):
    - id [string]: unique id returned when the transfer is created. ex: "5656565656565656"
    - amount [integer]: amount in cents to be transferred. ex: 1234 (= R$ 12.34)
    - external_id [string]: url safe string that must be unique among all your transfers. Duplicated external_ids will cause failures. By default, this parameter will block any transfer that repeats amount and receiver information on the same date. ex: "my-internal-id-123456"
    - scheduled [datetime.date, datetime.datetime or string]: date or datetime when the transfer will be processed. May be pushed to next business day if necessary. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - description [string]: optional description to override default description to be shown in the bank statement. ex: "Payment for service #1234"
    - fee [integer]: fee charged when the Transfer is processed. ex: 200 (= R$ 2.00)
    - status [string]: current transfer status. ex: "success" or "failed"
    - transaction_ids [list of strings]: ledger Transaction IDs linked to this Transfer (if there are two, the second is the chargeback). ex: ["19827356981273"]
    - created [datetime.datetime]: creation datetime for the transfer. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - updated [datetime.datetime]: latest update datetime for the transfer. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, name, tax_id, bank_code, branch_code, account_number, account_type=None, tags=None, id=None,
                 amount=None, external_id=None, scheduled=None, description=None, fee=None, status=None,
                 transaction_ids=None, created=None, updated=None):
        Resource.__init__(self, id=id)

        self.name = name
        self.tax_id = tax_id
        self.bank_code = bank_code
        self.branch_code = branch_code
        self.account_number = account_number
        self.account_type = account_type
        self.tags = tags
        self.amount = amount
        self.external_id = external_id
        self.scheduled = check_datetime_or_date(scheduled)
        self.description = description
        self.fee = fee
        self.status = status
        self.transaction_ids = transaction_ids
        self.created = check_datetime(created)
        self.updated = check_datetime(updated)


_resource = {"class": Transfer, "name": "Transfer"}
