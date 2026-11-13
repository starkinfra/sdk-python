from ..utils import rest
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime


class AiTranscript(Resource):
    """# AiTranscript object
    An AiTranscript is the text of an audio file you upload, from any speaker, cloned or not.
    When you initialize an AiTranscript, the entity will not be automatically
    created in the Stark Infra API. The 'create' function sends the object
    to the Stark Infra API and returns the created object.
    ## Parameters (required):
    - audio [string]: base64-encoded audio to transcribe. Up to 10000000 characters. The format is read from the file's own header.
    ## Attributes (return-only):
    - id [string]: unique id returned when the AiTranscript is created. ex: "5656565656565656"
    - text [string]: transcribed text.
    - status [string]: current status of the transcript. Options: "processing", "success", "failed"
    - errors [list of strings]: reasons the transcription failed. Empty when it worked.
    - created [datetime.datetime]: creation datetime for the AiTranscript. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - updated [datetime.datetime]: latest update datetime for the AiTranscript. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, audio=None, id=None, text=None, status=None, errors=None, created=None, updated=None):
        Resource.__init__(self, id=id)

        self.audio = audio
        self.text = text
        self.status = status
        self.errors = errors
        self.created = check_datetime(created)
        self.updated = check_datetime(updated)


_resource = {"class": AiTranscript, "name": "AiTranscript"}


def create(transcript, user=None):
    """# Create an AiTranscript
    Send an AiTranscript object for creation at the Stark Infra API. The audio is transcribed during the call.
    ## Parameters (required):
    - transcript [AiTranscript object]: AiTranscript object to be created in the API.
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - AiTranscript object with updated attributes
    """
    return rest.post_single(resource=_resource, entity=transcript, user=user)


def query(limit=None, user=None):
    """# Retrieve AiTranscripts
    Receive a generator of AiTranscript objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - generator of AiTranscript objects with updated attributes
    """
    return rest.get_stream(resource=_resource, limit=limit, user=user)


def page(cursor=None, limit=None, user=None):
    """# Retrieve paged AiTranscripts
    Receive a list of up to 100 AiTranscript objects previously created in the Stark Infra API and the cursor to the next page.
    Use this function instead of query if you want to manually page your requests.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - limit [integer, default 100]: maximum number of objects to be retrieved. Max = 100. ex: 35
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of AiTranscript objects with updated attributes
    - cursor to retrieve the next page of AiTranscript objects
    """
    return rest.get_page(resource=_resource, cursor=cursor, limit=limit, user=user)
