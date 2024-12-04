from ..utils import rest
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime_or_date


class BrcodePreview(Resource):
    """# BrcodePreview object
    The BrcodePreview object is used to preview information from a BR Code before paying it.
    When you initialize a BrcodePreview, the entity will not be automatically
    created in the Stark Infra API. The 'create' function sends the objects
    to the Stark Infra API and returns the created object.
    ## Parameters (required):
    - id [string]: BR Code from a Pix payment. This is also de information directly encoded in a QR Code. ex: "00020126580014br.gov.bcb.pix0136a629532e-7693-4846-852d-1bbff817b5a8520400005303986540510.005802BR5908T'Challa6009Sao Paulo62090505123456304B14A"
    - payer_id [string]: tax id (CPF/CNPJ) of the individual or business requesting the PixKey information. This id is used by the Central Bank to limit request rates. ex: "20.018.183/0001-80"
    ## Parameters (optional):
    - end_to_end_id [string]: central bank's unique transaction ID. ex: "E79457883202101262140HHX553UPqeq"
    ## Attributes (return-only):
    - account_number [string]: Payment receiver account number. ex: "1234567"
    - account_type [string]: Payment receiver account type. ex: "checking"
    - amount [integer]: Value in cents that this payment is expecting to receive. If 0, any value is accepted. ex: 123 (= R$1,23)
    - amount_type [string]: amount type of the Brcode. If the amount type is "custom" the Brcode's amount can be changed by the sender at the moment of payment. Options: "fixed" or "custom"
    - bank_code [string]: Payment receiver bank code. ex: "20018183"
    - branch_code [string]: Payment receiver branch code. ex: "0001"
    - cash_amount [integer]: Amount to be withdrawn from the cashier in cents. ex: 1000 (= R$ 10.00)
    - cashier_bank_code [string]: Cashier's bank code. ex: "20018183"
    - cashier_type [string]: Cashier's type. Options: "merchant", "participant" and "other"
    - discount_amount [integer]: Discount value calculated over nominal_amount. ex: 3000
    - fine_amount [integer]: Fine value calculated over nominal_amount. ex: 20000
    - interest_amount [integer]: Interest value calculated over nominal_amount. ex: 10000
    - key_id [string]: Receiver's PixKey id. ex: "+5511989898989"
    - name [string]: Payment receiver name. ex: "Tony Stark"
    - nominal_amount [integer]: Brcode emission amount, without fines, fees and discounts. ex: 1234 (= R$ 12.34)
    - reconciliation_id [string]: Reconciliation ID linked to this payment. If the brcode is dynamic, the reconciliation_id will have from 26 to 35 alphanumeric characters, ex: "cd65c78aeb6543eaaa0170f68bd741ee". If the brcode is static, the reconciliation_id will have up to 25 alphanumeric characters "ah27s53agj6493hjds6836v49"
    - reduction_amount [integer]: Reduction value to discount from nominal_amount. ex: 1000
    - scheduled [datetime.datetime]: date of payment execution. ex: datetime(2020, 3, 10)
    - status [string]: Payment status. ex: "active", "paid", "canceled" or "unknown"
    - tax_id [string]: Payment receiver tax ID. ex: "012.345.678-90"
    """

    def __init__(self, id, payer_id, account_number=None, account_type=None, amount=None, amount_type=None, bank_code=None,
                 branch_code=None, cash_amount=None, cashier_bank_code=None, cashier_type=None, discount_amount=None,
                 fine_amount=None, interest_amount=None, key_id=None, name=None, nominal_amount=None, end_to_end_id=None,
                 reconciliation_id=None, reduction_amount=None, scheduled=None, status=None, tax_id=None, description=None):
        Resource.__init__(self, id=id)
        
        self.payer_id = payer_id
        self.end_to_end_id = end_to_end_id
        self.account_number = account_number
        self.account_type = account_type
        self.amount = amount
        self.amount_type = amount_type
        self.bank_code = bank_code
        self.branch_code = branch_code
        self.cash_amount = cash_amount
        self.cashier_bank_code = cashier_bank_code
        self.cashier_type = cashier_type
        self.discount_amount = discount_amount
        self.fine_amount = fine_amount
        self.interest_amount = interest_amount
        self.key_id = key_id
        self.name = name
        self.nominal_amount = nominal_amount
        self.reconciliation_id = reconciliation_id
        self.reduction_amount = reduction_amount
        self.scheduled = check_datetime_or_date(scheduled)
        self.status = status
        self.tax_id = tax_id
        self.description = description


_resource = {"class": BrcodePreview, "name": "BrcodePreview"}


def create(previews, user=None):
    """# Retrieve BrcodePreviews
    Process BR Codes before paying them.
    ## Parameters (required):
    - previews [list of BrcodePreview objects]: List of BrcodePreview objects to preview. ex: [starkinfra.BrcodePreview("00020126580014br.gov.bcb.pix0136a629532e-7693-4846-852d-1bbff817b5a8520400005303986540510.005802BR5908T'Challa6009Sao Paulo62090505123456304B14A")]
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of BrcodePreview objects with updated attributes
    """
    return rest.post_multi(
        resource=_resource,
        entities=previews,
        user=user,
    )
