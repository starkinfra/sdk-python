from ..utils import rest
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime, check_date


class BusinessIdentity(Resource):
    """# BusinessIdentity object
    A BusinessIdentity represents the identity verification of a company (PJ), identified by
    its tax ID (CNPJ). It holds the company's registration data, the list of representatives,
    the attached documents, the extracted signature rules and the final verification status.
    When you initialize a BusinessIdentity, the entity will not be automatically
    created in the Stark Infra API. The 'create' function sends the objects
    to the Stark Infra API and returns the list of created objects.
    ## Parameters (required):
    - tax_id [string]: company's tax ID (CNPJ). ex: "20.018.183/0001-80"
    ## Parameters (optional):
    - tags [list of strings, default []]: list of strings for reference when searching for BusinessIdentities. ex: ["onboarding-123"]
    ## Attributes (return-only):
    - id [string]: unique id returned when the BusinessIdentity is created. ex: "5656565656565656"
    - name [string]: company's legal name, filled from the bureau. ex: "STARK BANK S.A."
    - tax_id_status [string]: status of the CNPJ at the bureau. ex: "active", "blocked", "pending"
    - insight_tax_id [string]: tax ID extracted from the document by the insight. ex: "20.018.183/0001-80"
    - insight_document_type [string]: document type detected by the insight. ex: "articles-of-incorporation"
    - num_pages [integer]: number of pages of the document. ex: 5
    - representatives [string]: JSON string of the company's representatives. ex: "[{\"name\": \"Edward Stark\", \"qualification\": \"Diretor\"}]"
    - attachments [list of strings]: list of attached documents references. ex: ["attachment/5656565656565656"]
    - rules [string]: JSON string of the complemented signature rules.
    - status [string]: current status of the BusinessIdentity. ex: "created", "pending", "canceled", "processing", "success", "failed"
    - created [datetime.datetime]: creation datetime for the BusinessIdentity. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - updated [datetime.datetime]: latest update datetime for the BusinessIdentity. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, tax_id, tags=None, id=None, name=None, tax_id_status=None, insight_tax_id=None,
                 insight_document_type=None, num_pages=None, representatives=None, attachments=None, rules=None,
                 status=None, created=None, updated=None):
        Resource.__init__(self, id=id)

        self.tax_id = tax_id
        self.tags = tags
        self.name = name
        self.tax_id_status = tax_id_status
        self.insight_tax_id = insight_tax_id
        self.insight_document_type = insight_document_type
        self.num_pages = num_pages
        self.representatives = representatives
        self.attachments = attachments
        self.rules = rules
        self.status = status
        self.created = check_datetime(created)
        self.updated = check_datetime(updated)


_resource = {"class": BusinessIdentity, "name": "BusinessIdentity"}


def create(identities, user=None):
    """# Create BusinessIdentities
    Send a list of BusinessIdentity objects for creation at the Stark Infra API
    ## Parameters (required):
    - identities [list of BusinessIdentity objects]: list of BusinessIdentity objects to be created in the API
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of BusinessIdentity objects with updated attributes
    """
    return rest.post_multi(resource=_resource, entities=identities, user=user)


def get(id, user=None):
    """# Retrieve a specific BusinessIdentity
    Receive a single BusinessIdentity object previously created in the Stark Infra API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - BusinessIdentity object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def query(limit=None, after=None, before=None, status=None, tags=None, ids=None, tax_ids=None, user=None):
    """# Retrieve BusinessIdentities
    Receive a generator of BusinessIdentity objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. ex: ["created", "pending", "canceled", "processing", "success", "failed"]
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - tax_ids [list of strings, default None]: list of company tax IDs (CNPJ) to filter retrieved objects. ex: ["20.018.183/0001-80"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - generator of BusinessIdentity objects with updated attributes
    """
    return rest.get_stream(
        resource=_resource,
        limit=limit,
        after=check_date(after),
        before=check_date(before),
        status=status,
        tags=tags,
        ids=ids,
        tax_ids=tax_ids,
        user=user,
    )


def page(cursor=None, limit=None, after=None, before=None, status=None, tags=None, ids=None, tax_ids=None, user=None):
    """# Retrieve paged BusinessIdentities
    Receive a list of up to 100 BusinessIdentity objects previously created in the Stark Infra API and the cursor to the next page.
    Use this function instead of query if you want to manually page your requests.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - limit [integer, default 100]: maximum number of objects to be retrieved. It must be an integer between 1 and 100. ex: 50
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. ex: ["created", "pending", "canceled", "processing", "success", "failed"]
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - tax_ids [list of strings, default None]: list of company tax IDs (CNPJ) to filter retrieved objects. ex: ["20.018.183/0001-80"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of BusinessIdentity objects with updated attributes
    - cursor to retrieve the next page of BusinessIdentity objects
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
        tax_ids=tax_ids,
        user=user,
    )


def update(id, status=None, tags=None, user=None):
    """# Update BusinessIdentity entity
    Update a BusinessIdentity by passing id.
    ## Parameters (required):
    - id [string]: BusinessIdentity id. ex: '5656565656565656'
    ## Parameters (optional):
    - status [string]: You may send the BusinessIdentity to processing by passing 'processing' in the status. The identity must have attachments.
    - tags [list of strings]: list of strings for reference when searching for BusinessIdentities. ex: ["onboarding-123"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - target BusinessIdentity with updated attributes
    """
    payload = {
        "status": status,
        "tags": tags,
    }
    return rest.patch_id(resource=_resource, id=id, user=user, payload=payload)


def cancel(id, user=None):
    """# Cancel a BusinessIdentity entity
    Cancel a BusinessIdentity entity previously created in the Stark Infra API. Only identities
    in the 'created' or 'pending' status can be canceled.
    ## Parameters (required):
    - id [string]: BusinessIdentity unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - canceled BusinessIdentity object
    """
    return rest.delete_id(resource=_resource, id=id, user=user)
