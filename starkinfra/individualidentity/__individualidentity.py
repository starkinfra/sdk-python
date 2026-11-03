from ..utils import rest
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime, check_date


class IndividualIdentity(Resource):
    """# IndividualIdentity object
    An IndividualIdentity runs an identity verification on an individual (CPF). It is created with the
    proofs the holder must submit, and the API returns the validator_link the holder opens to submit them.
    When delivery_method is "automatic", Stark Infra e-mails that link to the holder.
    When you initialize a IndividualIdentity, the entity will not be automatically
    created in the Stark Infra API. The 'create' function sends the objects
    to the Stark Infra API and returns the list of created objects.
    ## Parameters (required):
    - name [string]: individual's full name. ex: "Edward Stark"
    - delivery_method [string]: how the validator_link reaches the holder. Options: "automatic", "manual"
    - proofs [list of strings]: proofs the holder must submit; each one must be enabled on the workspace's Identity Profile. Options: "identity", "biometric"
    ## Parameters (conditionally required):
    - email [string, default None]: individual's e-mail, where the validator_link is sent. Required when delivery_method is "automatic". ex: "edward.stark@example.com"
    ## Parameters (optional):
    - tax_id [string, default None]: individual's tax ID (CPF). It can also be set later with update. ex: "012.345.678-90"
    - phone [string, default None]: individual's phone number in international format. The API returns it in national format. ex: "+5511987654321"
    - tags [list of strings, default None]: list of strings for reference when searching for IndividualIdentities. ex: ["employees", "monthly"]
    ## Attributes (return-only):
    - id [string]: unique id returned when the IndividualIdentity is created. ex: "5656565656565656"
    - status [string]: current status of the IndividualIdentity. Options: "created", "processing", "pending", "success", "failed"
    - validator_link [string]: link the holder opens to submit each proof. ex: "https://identity.starkinfra.com/validator-link?info=eyJpZGVudGl0eUlkIjoiNTY1NjU2NTY1NjU2NTY1NiJ9"
    - source_id [string]: id of the object that originated the IndividualIdentity. ex: "5656565656565656"
    - source_type [string]: type of the object that originated the IndividualIdentity. ex: "external"
    - workspace_id [string]: id of the workspace that owns the IndividualIdentity. ex: "5656565656565656"
    - created [datetime.datetime]: creation datetime for the IndividualIdentity. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - updated [datetime.datetime]: latest update datetime for the IndividualIdentity. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, name, delivery_method, proofs, email=None, tax_id=None, phone=None, tags=None, id=None,
                 status=None, validator_link=None, source_id=None, source_type=None, workspace_id=None,
                 created=None, updated=None):
        Resource.__init__(self, id=id)

        self.name = name
        self.delivery_method = delivery_method
        self.proofs = proofs
        self.email = email
        self.tax_id = tax_id
        self.phone = phone
        self.tags = tags
        self.status = status
        self.validator_link = validator_link
        self.source_id = source_id
        self.source_type = source_type
        self.workspace_id = workspace_id
        self.created = check_datetime(created)
        self.updated = check_datetime(updated)


_resource = {"class": IndividualIdentity, "name": "IndividualIdentity"}


def create(identities, user=None):
    """# Create IndividualIdentities
    Send a list of IndividualIdentity objects for creation at the Stark Infra API
    ## Parameters (required):
    - identities [list of IndividualIdentity objects]: list of IndividualIdentity objects to be created in the API
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of IndividualIdentity objects with updated attributes
    """
    return rest.post_multi(resource=_resource, entities=identities, user=user)


def get(id, user=None):
    """# Retrieve a specific IndividualIdentity
    Receive a single IndividualIdentity object previously created in the Stark Infra API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - IndividualIdentity object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def query(limit=None, status=None, tags=None, ids=None, after=None, before=None, tax_ids=None, email=None,
          user=None):
    """# Retrieve IndividualIdentities
    Receive a generator of IndividualIdentity objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. ex: ["created", "processing", "pending", "success", "failed"]
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - tax_ids [list of strings, default None]: list of tax IDs to filter retrieved objects, formatted as the API returns them. ex: ["012.345.678-90"]
    - email [string, default None]: e-mail to filter retrieved objects. ex: "edward.stark@example.com"
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - generator of IndividualIdentity objects with updated attributes
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
        email=email,
        user=user,
    )


def page(cursor=None, limit=None, status=None, tags=None, ids=None, after=None, before=None, tax_ids=None,
         email=None, user=None):
    """# Retrieve paged IndividualIdentities
    Receive a list of up to 100 IndividualIdentity objects previously created in the Stark Infra API and the cursor to the next page.
    Use this function instead of query if you want to manually page your requests.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - limit [integer, default 100]: maximum number of objects to be retrieved. It must be an integer between 1 and 100. ex: 50
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. ex: ["created", "processing", "pending", "success", "failed"]
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - tax_ids [list of strings, default None]: list of tax IDs to filter retrieved objects, formatted as the API returns them. ex: ["012.345.678-90"]
    - email [string, default None]: e-mail to filter retrieved objects. ex: "edward.stark@example.com"
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of IndividualIdentity objects with updated attributes
    - cursor to retrieve the next page of IndividualIdentity objects
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
        email=email,
        user=user,
    )


def update(id, tax_id, user=None):
    """# Update IndividualIdentity entity
    Update an IndividualIdentity by passing id. tax_id is the only field the API accepts in an update.
    ## Parameters (required):
    - id [string]: IndividualIdentity id. ex: '5656565656565656'
    - tax_id [string]: individual's tax ID (CPF). ex: "012.345.678-90"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - target IndividualIdentity with updated attributes
    """
    payload = {
        "tax_id": tax_id
    }
    return rest.patch_id(resource=_resource, id=id, user=user, payload=payload)


def cancel(id, user=None):
    """# Cancel a IndividualIdentity entity
    Cancel a IndividualIdentity entity previously created in the Stark Infra API
    ## Parameters (required):
    - id [string]: IndividualIdentity unique id. ex: "6306109539221504"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - canceled IndividualIdentity object
    """
    return rest.delete_id(resource=_resource, id=id, user=user)
