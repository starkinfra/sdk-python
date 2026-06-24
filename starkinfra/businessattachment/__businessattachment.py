from base64 import b64encode
from ..utils import rest
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime, check_date


class BusinessAttachment(Resource):
    """# BusinessAttachment object
    A BusinessAttachment represents a document (articles of incorporation, bylaws, etc.) sent
    to a BusinessIdentity. You must reference the desired BusinessIdentity by its id.
    A BusinessIdentity accepts at most 2 attachments.
    When you initialize a BusinessAttachment, the entity will not be automatically
    created in the Stark Infra API. The 'create' function sends the objects
    to the Stark Infra API and returns the list of created objects.
    ## Parameters (required):
    - name [string]: name of the document. Must be unique among the identity's "created" attachments. ex: "articles-of-incorporation.pdf"
    - content [string]: Base64 data url of the document. ex: data:application/pdf;base64,JVBERi0xLjQ...
    - business_identity_id [string]: unique id of the BusinessIdentity this attachment belongs to. ex: "5656565656565656"
    ## Parameters (optional):
    - content_type [string, default None]: content MIME type. This parameter is required as input only. ex: "application/pdf", "image/png" or "image/jpeg"
    - tags [list of strings, default []]: list of strings for reference when searching for BusinessAttachments. ex: ["doc-principal"]
    ## Attributes (return-only):
    - id [string]: unique id returned when the BusinessAttachment is created. ex: "5656565656565656"
    - attachment_id [string]: id of the document in the external ms-attachment. ex: "5104320788332544"
    - status [string]: current status of the BusinessAttachment. ex: "created", "canceled", "approved", "denied"
    - created [datetime.datetime]: creation datetime for the BusinessAttachment. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - updated [datetime.datetime]: latest update datetime for the BusinessAttachment. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, name, content, business_identity_id, content_type=None, tags=None, id=None, attachment_id=None,
                 status=None, created=None, updated=None):
        Resource.__init__(self, id=id)

        self.name = name
        self.content = content
        self.business_identity_id = business_identity_id
        self.tags = tags
        self.attachment_id = attachment_id
        self.status = status
        self.created = check_datetime(created)
        self.updated = check_datetime(updated)

        if content_type:
            if not content:
                raise ValueError("content is required when content_type is provided")
            if isinstance(content, bytes):
                content = b64encode(content).decode()
            self.content = "data:" + content_type + ";base64," + content


_resource = {"class": BusinessAttachment, "name": "BusinessAttachment"}


def create(attachments, user=None):
    """# Create BusinessAttachments
    Send a list of BusinessAttachment objects for creation at the Stark Infra API
    ## Parameters (required):
    - attachments [list of BusinessAttachment objects]: list of BusinessAttachment objects to be created in the API
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of BusinessAttachment objects with updated attributes
    """
    return rest.post_multi(resource=_resource, entities=attachments, user=user)


def get(id, expand=None, user=None):
    """# Retrieve a specific BusinessAttachment
    Receive a single BusinessAttachment object previously created in the Stark Infra API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - expand [list of strings, default None]: fields to expand information. ex: ["content"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - BusinessAttachment object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, expand=expand, user=user)


def query(limit=None, after=None, before=None, status=None, tags=None, ids=None, user=None):
    """# Retrieve BusinessAttachments
    Receive a generator of BusinessAttachment objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. ex: ["created", "canceled", "approved", "denied"]
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - generator of BusinessAttachment objects with updated attributes
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


def page(cursor=None, limit=None, after=None, before=None, status=None, tags=None, ids=None, user=None):
    """# Retrieve paged BusinessAttachments
    Receive a list of up to 100 BusinessAttachment objects previously created in the Stark Infra API and the cursor to the next page.
    Use this function instead of query if you want to manually page your requests.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - limit [integer, default 100]: maximum number of objects to be retrieved. It must be an integer between 1 and 100. ex: 50
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. ex: ["created", "canceled", "approved", "denied"]
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of BusinessAttachment objects with updated attributes
    - cursor to retrieve the next page of BusinessAttachment objects
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
    """# Cancel a BusinessAttachment entity
    Cancel a BusinessAttachment entity previously created in the Stark Infra API. Only attachments
    in the 'created' status can be canceled.
    ## Parameters (required):
    - id [string]: BusinessAttachment unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - canceled BusinessAttachment object
    """
    return rest.delete_id(resource=_resource, id=id, user=user)
