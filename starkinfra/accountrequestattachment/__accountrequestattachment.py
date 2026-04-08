from base64 import b64encode
from ..utils import rest
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime, check_date


class AccountRequestAttachment(Resource):
    """# AccountRequestAttachment object
    You can create an Account Request Attachment to attach images of documents
    to a specific Individual Account Request. You must reference the desired Individual Account Request by its id.
    When you initialize an AccountRequestAttachment, the entity will not be automatically
    created in the Stark Infra API. The 'create' function sends the objects
    to the Stark Infra API and returns the list of created objects.
    ## Parameters (required):
    - type [string]: type of the AccountRequestAttachment. Options: "drivers-license-front", "drivers-license-back", "identity-front", "identity-back" or "selfie"
    - content [string]: Base64 data url of the picture. ex: data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAASABIAAD...
    - account_request_id [string]: Unique id of IndividualAccountRequest. ex: "5656565656565656"
    ## Parameters (optional):
    - content_type [string, default None]: content MIME type. This parameter is required as input only. ex: "image/png" or "image/jpeg"
    - tags [list of strings, default []]: list of strings for reference when searching for AccountRequestAttachments. ex: ["employees", "monthly"]
    ## Attributes (return-only):
    - id [string]: unique id returned when the AccountRequestAttachment is created. ex: "5656565656565656"
    - status [string]: current status of the AccountRequestAttachment. ex: "created"
    - created [datetime.datetime]: creation datetime for the AccountRequestAttachment. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, type, content, account_request_id, content_type=None, tags=None, id=None, status=None,
                 created=None):
        Resource.__init__(self, id=id)

        self.type = type
        self.content = content
        self.account_request_id = account_request_id
        self.tags = tags
        self.status = status
        self.created = check_datetime(created)

        if content_type:
            if not content:
                raise ValueError("content is required when content_type is provided")
            if isinstance(content, bytes):
                content = b64encode(content).decode()
            self.content = "data:" + content_type + ";base64," + content


_resource = {"class": AccountRequestAttachment, "name": "AccountRequestAttachment"}


def create(attachments, user=None):
    """# Create AccountRequestAttachments
    Send a list of AccountRequestAttachment objects for creation at the Stark Infra API
    ## Parameters (required):
    - attachments [list of AccountRequestAttachment objects]: list of AccountRequestAttachment objects to be created in the API
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of AccountRequestAttachment objects with updated attributes
    """
    return rest.post_multi(resource=_resource, entities=attachments, user=user)


def get(id, user=None):
    """# Retrieve a specific AccountRequestAttachment
    Receive a single AccountRequestAttachment object previously created in the Stark Infra API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - AccountRequestAttachment object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def query(limit=None, after=None, before=None, status=None, tags=None, ids=None, user=None):
    """# Retrieve AccountRequestAttachments
    Receive a generator of AccountRequestAttachment objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. ex: ["created", "canceled", "processing", "failed", "success"]
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - generator of AccountRequestAttachment objects with updated attributes
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
    """# Retrieve paged AccountRequestAttachments
    Receive a list of up to 100 AccountRequestAttachment objects previously created in the Stark Infra API and the cursor to the next page.
    Use this function instead of query if you want to manually page your requests.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - limit [integer, default 100]: maximum number of objects to be retrieved. It must be an integer between 1 and 100. ex: 50
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. ex: ["created", "canceled", "processing", "failed", "success"]
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of AccountRequestAttachment objects with updated attributes
    - cursor to retrieve the next page of AccountRequestAttachment objects
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
