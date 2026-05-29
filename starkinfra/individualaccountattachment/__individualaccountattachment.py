from base64 import b64encode
from ..utils import rest
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime, check_date


class IndividualAccountAttachment(Resource):
    """# IndividualAccountAttachment object
    You can create an IndividualAccountAttachment to attach images of documents
    to a specific IndividualAccountRequest. You must reference the desired IndividualAccountRequest by its id.
    When you initialize an IndividualAccountAttachment, the entity will not be automatically
    created in the Stark Infra API. The 'create' function sends the objects
    to the Stark Infra API and returns the list of created objects.
    ## Parameters (required):
    - type [string]: type of the IndividualAccountAttachment. Options: "drivers-license-front", "drivers-license-back", "identity-front" or "identity-back"
    - content [bytes]: raw image bytes of the picture. After encoding, becomes a data url. ex: open("file.png", "rb").read()
    - content_type [string]: content MIME type. This parameter is required as input only. ex: "image/png" or "image/jpeg"
    - account_request_id [string]: Unique id of the IndividualAccountRequest. ex: "5656565656565656"
    ## Parameters (optional):
    - tags [list of strings, default []]: list of strings for reference when searching for IndividualAccountAttachments. ex: ["employees", "monthly"]
    ## Attributes (return-only):
    - id [string]: unique id returned when the IndividualAccountAttachment is created. ex: "5656565656565656"
    - status [string]: current status of the IndividualAccountAttachment. ex: "created", "success", "failed" or "deleted"
    - created [datetime.datetime]: creation datetime for the IndividualAccountAttachment. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, type, content, account_request_id, content_type=None, tags=None, id=None, status=None,
                 created=None):
        Resource.__init__(self, id=id)

        self.type = type
        self.account_request_id = account_request_id
        self.tags = tags
        self.status = status
        self.created = check_datetime(created)
        self.content = content
        self.content_type = content_type

        if content_type:
            # content_type is input-only and is consumed here to build the data: URL;
            # it is never sent as its own wire field (M3). Only raw bytes can be
            # base64-encoded — a non-bytes content (e.g. an empty string) passes
            # through unchanged so the API owns the rejection (InputErrors).
            if isinstance(content, bytes):
                self.content = "data:{content_type};base64,{content}".format(
                    content_type=content_type,
                    content=b64encode(content).decode('utf-8')
                )
            self.content_type = None
        elif isinstance(content, bytes):
            # Without a content_type the SDK cannot build the data: URL, but raw bytes
            # are not JSON-serializable and would crash before the request is sent.
            # Base64-encode to a serializable string so the request reaches the API,
            # which then rejects it (InputErrors). Mirrors the PHP reference, which
            # only data-URL-encodes when contentType is present.
            self.content = b64encode(content).decode('utf-8')


_resource = {"class": IndividualAccountAttachment, "name": "IndividualAccountAttachment"}


def create(attachments, user=None):
    """# Create IndividualAccountAttachments
    Send a list of IndividualAccountAttachment objects for creation at the Stark Infra API
    ## Parameters (required):
    - attachments [list of IndividualAccountAttachment objects]: list of IndividualAccountAttachment objects to be created in the API
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of IndividualAccountAttachment objects with updated attributes
    """
    return rest.post_multi(resource=_resource, entities=attachments, user=user)


def get(id, user=None):
    """# Retrieve a specific IndividualAccountAttachment
    Receive a single IndividualAccountAttachment object previously created in the Stark Infra API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - IndividualAccountAttachment object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def query(limit=None, after=None, before=None, status=None, tags=None, ids=None, user=None):
    """# Retrieve IndividualAccountAttachments
    Receive a generator of IndividualAccountAttachment objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None]: date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None]: date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. ex: ["created", "success", "failed", "deleted"]
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - generator of IndividualAccountAttachment objects with updated attributes
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
    """# Retrieve paged IndividualAccountAttachments
    Receive a list of up to 100 IndividualAccountAttachment objects previously created in the Stark Infra API and the cursor to the next page.
    Use this function instead of query if you want to manually page your requests.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - limit [integer, default 100]: maximum number of objects to be retrieved. It must be an integer between 1 and 100. ex: 50
    - after [datetime.date or string, default None]: date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None]: date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. ex: ["created", "success", "failed", "deleted"]
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of IndividualAccountAttachment objects with updated attributes
    - cursor to retrieve the next page of IndividualAccountAttachment objects
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
    """# Delete an IndividualAccountAttachment entity
    Delete an IndividualAccountAttachment entity previously created in the Stark Infra API
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - deleted IndividualAccountAttachment object
    """
    return rest.delete_id(resource=_resource, id=id, user=user)
