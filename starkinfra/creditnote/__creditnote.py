from ..utils import rest
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime, check_date


class CreditNote(Resource):
    """# CreditNote object
    CreditNotes are used to generate CCB contracts between you and your customers.
    When you initialize a CreditNote, the entity will not be automatically
    created in the Stark Infra API. The 'create' function sends the objects
    to the Stark Infra API and returns the list of created objects.
    ## Parameters (required):
    - template_id [string]: ID of the contract template on which the credit note will be based. ex: template_id="0123456789101112"
    - name [string]: credit receiver's full name. ex: name="Edward Stark"
    - tax_id [string]: credit receiver's tax ID (CPF or CNPJ). ex: "20.018.183/0001-80"
    - nominal_amount [integer]: amount in cents transferred to the credit receiver, before deductions. ex: nominal_amount=11234 (= R$ 112.34)
    - scheduled [datetime.date, datetime.datetime or string, default now]: date of transfer execution. ex: scheduled=datetime(2020, 3, 10)
    - invoices [list of Invoice objects]: list of Invoice objects to be created and sent to the credit receiver. ex: invoices=[Invoice(), Invoice()]
    - transfer [Transfer object]: Transfer object to be created and sent to the credit receiver. ex: transfer=Transfer()
    - signers [list of dictionaries]: signer's name, e-mail and delivery method for the contract. ex: signers=[{"name": "Tony Stark", "contact": "tony@starkindustries.com", "method": "link"}]
    Parameters (optional):
    - rebate_amount [integer, default None]: credit analysis fee deducted from lent amount. ex: rebate_amount=11234 (= R$ 112.34)
    - tags [list of strings, default None]: list of strings for reference when searching for CreditNotes. ex: tags=["employees", "monthly"]
    - externalId [string]: url safe string that must be unique among all your CreditNotes. ex: externalId="my-internal-id-123456"
    Attributes (return-only):
    - id [string, default None]: unique id returned when the CreditNote is created. ex: "5656565656565656"
    - interest [float]: yearly effective interest rate of the credit note, in percentage. ex: 12.5
    - created [datetime.datetime, default None]: creation datetime for the CreditNote. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - updated [datetime.datetime, default None]: latest update datetime for the CreditNote. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, template_id, name, tax_id, nominal_amount, scheduled, invoices, transfer, signers,
                 external_id=None, interest=None, rebate_amount=None, tags=None, created=None, updated=None, id=None):
        Resource.__init__(self, id=id)

        self.template_id = template_id
        self.name = name
        self.tax_id = tax_id
        self.nominal_amount = nominal_amount
        self.scheduled = scheduled
        self.invoices = invoices
        self.transfer = transfer
        self.signers = signers
        self.external_id = external_id
        self.interest = interest
        self.rebate_amount = rebate_amount
        self.tags = tags
        self.created = check_datetime(created)
        self.updated = check_datetime(updated)


_resource = {"class": CreditNote, "name": "CreditNote"}


def create(notes, user=None):
    """# Create CreditNotes
    Send a list of CreditNote objects for creation in the Stark Bank API
    ## Parameters (required):
    - notes [list of CreditNote objects]: list of CreditNote objects to be created in the API
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - list of CreditNote objects with updated attributes
    """
    return rest.post_multi(resource=_resource, entities=notes, user=user)


def get(id, user=None):
    """# Retrieve a specific CreditNote
    Receive a single CreditNote object previously created in the Stark Bank API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - CreditNote object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def query(limit=None, status=None, tags=None, ids=None, after=None, before=None, user=None):
    """# Retrieve CreditNotes
    Receive a generator of CreditNote objects previously created in the Stark Bank API
    ## Parameters (optional):
    - limit [integer, default 100]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - status [string, default None]: filter for status of retrieved objects. ex: "paid" or "registered"
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
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
    Receive a list of up to 100 CreditNote objects previously created in the Stark Bank API and the cursor to the next page.
    Use this function instead of query if you want to manually page your requests.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - limit [integer, default 100]: maximum number of objects to be retrieved. It must be an integer between 1 and 100. ex: 50
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - status [string, default None]: filter for status of retrieved objects. ex: "paid" or "registered"
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
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

def delete(id, user=None):
    """# Cancel a Credit Note entity
    Cancel a Credit Note entity previously created in the Stark Infra API
    ## Parameters (required):
    - id [string]: Credit Note unique id. ex: "6306109539221504"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - deleted Credit Note object
    """
    return rest.delete_id(resource=_resource, id=id, user=user)
