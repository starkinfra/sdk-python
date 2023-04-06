from base64 import b64encode
from ..utils import rest
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime, check_date


class IndividualDocument(Resource):
    """# IndividualDocument object
    Individual documents are images containing either side of a document or a selfie
    to be used in a matching validation. When created, they must be attached to an individual
    identity to be used for its validation.
    When you initialize a IndividualDocument, the entity will not be automatically
    created in the Stark Infra API. The 'create' function sends the objects
    to the Stark Infra API and returns the list of created objects.
    ## Parameters (required):
    - type [string]: type of the IndividualDocument. Options: "drivers-license-front", "drivers-license-back", "identity-front", "identity-back" or "selfie"
    - content [string]: Base64 data url of the picture. ex: data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAASABIAAD...
    - content_type [string]: content MIME type. This parameter is required as input only. ex: "image/png" or "image/jpeg"
    - identity_id [string]: unique id of IndividualIdentity. ex: "5656565656565656"
    ## Parameters (optional):
    - tags [list of strings, default []]: list of strings for reference when searching for IndividualDocuments. ex: ["employees", "monthly"]
    ## Attributes (return-only):
    - id [string]: unique id returned when the IndividualDocument is created. ex: "5656565656565656"
    - status [string]: current status of the IndividualDocument. Options: "created", "canceled", "processing", "failed", "success"
    - created [datetime.datetime]: creation datetime for the IndividualDocument. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, type, content, identity_id, content_type=None, tags=None, id=None, status=None, created=None):
        Resource.__init__(self, id=id)
        self.type = type
        self.identity_id = identity_id
        self.tags = tags
        self.status = status
        self.created = check_datetime(created)
        self.content = content
        self.content_type = content_type

        if content_type:
            self.content = "data:{content_type};base64,{content}".format(
                content_type=content_type,
                content=b64encode(content).decode('utf-8')
            )
            self.content_type = None


_resource = {"class": IndividualDocument, "name": "IndividualDocument"}


def create(documents, user=None):
    """# Create IndividualDocuments
    Send a list of IndividualDocument objects for creation at the Stark Infra API
    ## Parameters (required):
    - documents [list of IndividualDocument objects]: list of IndividualDocument objects to be created in the API
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of IndividualDocument objects with updated attributes
    """
    return rest.post_multi(resource=_resource, entities=documents, user=user)


def get(id, user=None):
    """# Retrieve a specific IndividualDocument
    Receive a single IndividualDocument object previously created in the Stark Infra API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - IndividualDocument object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def query(limit=None, status=None, tags=None, ids=None, after=None, before=None, user=None):
    """# Retrieve IndividualDocuments
    Receive a generator of IndividualDocument objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. Options: ["created", "canceled", "processing", "failed", "success"]
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - generator of IndividualDocument objects with updated attributes
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
    """# Retrieve paged IndividualDocuments
    Receive a list of up to 100 IndividualDocument objects previously created in the Stark Infra API and the cursor to the next page.
    Use this function instead of query if you want to manually page your requests.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - limit [integer, default 100]: maximum number of objects to be retrieved. It must be an integer between 1 and 100. ex: 50
    - after [datetime.date or string, default None] date filter for objects created only after specified date. ex: datetime.date(2020, 3, 10)
    - before [datetime.date or string, default None] date filter for objects created only before specified date. ex: datetime.date(2020, 3, 10)
    - status [list of strings, default None]: filter for status of retrieved objects. Options: ["created", "canceled", "processing", "failed", "success"]
    - tags [list of strings, default None]: tags to filter retrieved objects. ex: ["tony", "stark"]
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of IndividualDocument objects with updated attributes
    - cursor to retrieve the next page of IndividualDocument objects
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

