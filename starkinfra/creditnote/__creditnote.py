from datetime import date, datetime
from .invoice.__invoice import Invoice
from .invoice.__invoice import _resource as _invoice_resource
from ..creditsigner.__creditsigner import CreditSigner
from ..creditsigner.__creditsigner import _resource as _creditsigner_resource
from .__transfer import Transfer
from .__transfer import _resource as _transfer_resource
from ..utils import rest
from starkcore.utils.api import from_api_json
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime, check_date, check_datetime_or_date


class CreditNote(Resource):
    """# CreditNote object
    CreditNotes are used to generate CCB contracts between you and your customers.
    When you initialize a CreditNote, the entity will not be automatically
    created in the Stark Infra API. The 'create' function sends the objects
    to the Stark Infra API and returns the list of created objects.
    ## Parameters (required):
    - template_id [string]: ID of the contract template on which the CreditNote will be based. ex: "0123456789101112"
    - name [string]: credit receiver's full name. ex: "Edward Stark"
    - tax_id [string]: credit receiver's tax ID (CPF or CNPJ). ex: "20.018.183/0001-80"
    - scheduled [datetime.date, datetime.datetime or string]: date of transfer execution. ex: datetime(2020, 3, 10)
    - invoices [list of Invoice objects]: list of Invoice objects to be created and sent to the credit receiver. ex: [Invoice(), Invoice()]
    - payment [creditnote.Transfer]: payment entity to be created and sent to the credit receiver. ex: creditnote.Transfer()
    - signers [list of CreditSigner objects]: signer's name, contact and delivery method for the signature request. ex: [CreditSigner(), CreditSigner()]
    - external_id [string]: a string that must be unique among all your CreditNotes, used to avoid resource duplication. ex: "my-internal-id-123456"
    - street_line_1 [string]: credit receiver main address. ex: "Av. Paulista, 200"
    - street_line_2 [string]: credit receiver address complement. ex: "Apto. 123"
    - district [string]: credit receiver address district / neighbourhood. ex: "Bela Vista"
    - city [string]: credit receiver address city. ex: "Rio de Janeiro"
    - state_code [string]: credit receiver address state. ex: "GO"
    - zip_code [string]: credit receiver address zip code. ex: "01311-200"
    ## Parameters (conditionally required):
    - payment_type [string]: payment type, inferred from the payment parameter if it is not a dictionary. ex: "transfer"
    - nominal_amount [integer]: CreditNote value in cents. The nominal_amount parameter is required when amount is not sent. ex: 1234 (= R$ 12.34)
    - amount [integer]: amount in cents transferred to the credit receiver, before deductions. The amount parameter is required when nominal_amount is not sent. ex: 1234 (= R$ 12.34)
    ## Parameters (optional):
    - rebate_amount [integer, default 0]: credit analysis fee deducted from lent amount. ex: 11234 (= R$ 112.34)
    - tags [list of strings, default []]: list of strings for reference when searching for CreditNotes. ex: ["employees", "monthly"]
    - expiration [integer or datetime.timedelta, default 604800 (7 days)]: time interval in seconds between scheduled date and expiration date. ex 123456789
    ## Attributes (return-only):
    - id [string]: unique id returned when the CreditNote is created. ex: "5656565656565656"
    - document_id [string]: ID of the signed document to execute this CreditNote. ex: "4545454545454545"
    - status [string]: current status of the CreditNote. ex: "canceled", "created", "expired", "failed", "processing", "signed", "success"
    - transaction_ids [list of strings]: ledger transaction ids linked to this CreditNote. ex: ["19827356981273"]
    - workspace_id [string]: ID of the Workspace that generated this CreditNote. ex: "4545454545454545"
    - tax_amount [integer]: tax amount included in the CreditNote. ex: 100
    - nominal_interest [float]: yearly nominal interest rate of the CreditNote, in percentage. ex: 11.5
    - interest [float]: yearly effective interest rate of the CreditNote, in percentage. ex: 12.5
    - created [datetime.datetime]: creation datetime for the CreditNote. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - updated [datetime.datetime]: latest update datetime for the CreditNote. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, template_id, name, tax_id, scheduled, invoices, payment, signers, external_id,
                 street_line_1, street_line_2, district, city, state_code, zip_code, payment_type=None,
                 nominal_amount=None, amount=None, rebate_amount=None, tags=None, expiration=None, id=None,
                 document_id=None, status=None, transaction_ids=None, workspace_id=None, tax_amount=None,
                 nominal_interest=None, interest=None, created=None, updated=None):
        Resource.__init__(self, id=id)

        self.template_id = template_id
        self.name = name
        self.tax_id = tax_id
        self.scheduled = check_datetime_or_date(scheduled)
        self.invoices = _parse_invoices(invoices)
        self.signers = _parse_signers(signers)
        self.external_id = external_id
        self.street_line_1 = street_line_1
        self.street_line_2 = street_line_2
        self.district = district
        self.city = city
        self.state_code = state_code
        self.zip_code = zip_code
        self.nominal_amount = nominal_amount
        self.amount = amount
        self.rebate_amount = rebate_amount
        self.tags = tags
        self.expiration = expiration
        self.document_id = document_id
        self.status = status
        self.transaction_ids = transaction_ids
        self.workspace_id = workspace_id
        self.tax_amount = tax_amount
        self.nominal_interest = nominal_interest
        self.interest = interest
        self.created = check_datetime(created)
        self.updated = check_datetime(updated)

        self.payment, self.payment_type = _parse_payment(payment=payment, payment_type=payment_type)


_resource = {"class": CreditNote, "name": "CreditNote"}


def _parse_signers(signers):
    parsed_signers = []
    for signer in signers:
        if isinstance(signer, CreditSigner):
            parsed_signers.append(signer)
            continue
        parsed_signers.append(from_api_json(_creditsigner_resource, signer))
    return parsed_signers


def _parse_invoices(invoices):
    parsed_invoices = []
    for invoice in invoices:
        if isinstance(invoice, Invoice):
            parsed_invoices.append(invoice)
            continue
        parsed_invoices.append(from_api_json(_invoice_resource, invoice))
    return parsed_invoices


def _parse_payment(payment, payment_type):
    if isinstance(payment, dict):
        try:
            return from_api_json(*({
                "transfer": _transfer_resource,
            }[payment_type], payment)), payment_type
        except KeyError:
            return payment, payment_type

    if payment_type:
        return payment, payment_type

    if isinstance(payment, Transfer):
        return payment, "transfer"

    raise Exception(
        "payment must be either "
        "a dictionary"
        ", a starkinfra.creditnote.Transfer"
        ", but not a {}".format(type(payment))
    )


def create(notes, user=None):
    """# Create CreditNotes
    Send a list of CreditNote objects for creation at the Stark Infra API
    ## Parameters (required):
    - notes [list of CreditNote objects]: list of CreditNote objects to be created in the API
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of CreditNote objects with updated attributes
    """
    return rest.post_multi(resource=_resource, entities=notes, user=user)


def get(id, user=None):
    """# Retrieve a specific CreditNote
    Receive a single CreditNote object previously created in the Stark Infra API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - CreditNote object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def query(limit=None, status=None, tags=None, ids=None, after=None, before=None, user=None):
    """# Retrieve CreditNotes
    Receive a generator of CreditNote objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. ex: ["canceled", "created", "expired", "failed", "processing", "signed", "success"]
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - generator of CreditNote objects with updated attributes
    """
    return rest.get_stream(
        resource=_resource,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        status=status,
        tags=tags,
        ids=ids,
        user=user,
    )


def page(cursor=None, limit=None, status=None, tags=None, ids=None, after=None, before=None, user=None):
    """# Retrieve paged CreditNotes
    Receive a list of up to 100 CreditNote objects previously created in the Stark Infra API and the cursor to the next page.
    Use this function instead of query if you want to manually page your requests.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - limit [integer, default 100]: maximum number of objects to be retrieved. It must be an integer between 1 and 100. ex: 50
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. ex: ["canceled", "created", "expired", "failed", "processing", "signed", "success"]
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of CreditNote objects with updated attributes
    - cursor to retrieve the next page of CreditNote objects
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
        user=user,
    )


def cancel(id, user=None):
    """# Cancel a CreditNote entity
    Cancel a CreditNote entity previously created in the Stark Infra API
    ## Parameters (required):
    - id [string]: CreditNote unique id. ex: "6306109539221504"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - canceled CreditNote object
    """
    return rest.delete_id(resource=_resource, id=id, user=user)


def pdf(noteId, user=None):
    """# Retrieve CCB disbursement
    Receive a CCB disbursement pdf file.
    ## Parameters (required):
    - noteId [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - Transfer pdf file
    """
    return rest.get_content(resource=_resource, id=noteId, user=user, sub_resource_name="payment/pdf")
