from ..utils import rest
from starkcore.utils.api import from_api_json, endpoint
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime


class AiSpeech(Resource):
    """# AiSpeech object
    An AiSpeech is one text read out loud by an AiVoice. The speech is synthesized when it is created and comes
    back as a base64 MP3 in the audio attribute.
    When you initialize an AiSpeech, the entity will not be automatically
    created in the Stark Infra API. The 'create' function sends the object
    to the Stark Infra API and returns the created object.
    ## Parameters (required):
    - voice_id [string]: id of the AiVoice that should read the text. Only a voice in "success" can speak. ex: "5656565656565656"
    - text [string]: text to read out loud. Between 1 and 100000 characters. ex: "Hello, how can I help you?"
    ## Attributes (return-only):
    - id [string]: unique id returned when the AiSpeech is created. ex: "5656565656565656"
    - status [string]: current status of the speech. Options: "processing", "success", "failed"
    - audio [string]: base64-encoded MP3 of the speech. Left out of query results; get returns it.
    - voice_name [string]: name of the voice. Only present when requested with expand=["voice_name"].
    - errors [list of strings]: reasons the synthesis failed. Empty when it worked.
    - created [datetime.datetime]: creation datetime for the AiSpeech. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - updated [datetime.datetime]: latest update datetime for the AiSpeech. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, voice_id, text, id=None, status=None, audio=None, voice_name=None, errors=None, created=None,
                 updated=None):
        Resource.__init__(self, id=id)

        self.voice_id = voice_id
        self.text = text
        self.status = status
        self.audio = audio
        self.voice_name = voice_name
        self.errors = errors
        self.created = check_datetime(created)
        self.updated = check_datetime(updated)


_resource = {"class": AiSpeech, "name": "AiSpeech"}


def create(speech, user=None):
    """# Create an AiSpeech
    Send an AiSpeech object for creation at the Stark Infra API. The audio is synthesized during the call.
    ## Parameters (required):
    - speech [AiSpeech object]: AiSpeech object to be created in the API.
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - AiSpeech object with updated attributes
    """
    return rest.post_single(resource=_resource, entity=speech, user=user)


def get(id, expand=None, user=None):
    """# Retrieve a specific AiSpeech
    Receive a single AiSpeech object previously created in the Stark Infra API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - expand [list of strings, default None]: extra attributes to compute. Options: "voice_name".
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - AiSpeech object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, expand=expand, user=user)


def query(limit=None, expand=None, user=None):
    """# Retrieve AiSpeeches
    Receive a generator of AiSpeech objects previously created in the Stark Infra API, following the cursor until the list ends. The audio is left out of the results.
    The core derives the response key from the resource name and reads "speechs", but the API answers "speeches", so the list is read here.
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - expand [list of strings, default None]: extra attributes to compute. Options: "voice_name".
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - generator of AiSpeech objects with updated attributes
    """
    cursor = None
    remaining = limit
    while True:
        speeches, cursor = page(cursor=cursor, limit=min(remaining, 100) if remaining else None, expand=expand, user=user)
        for speech in speeches:
            yield speech
        if remaining:
            remaining -= len(speeches)
        if not cursor or (limit and remaining <= 0):
            break


def page(cursor=None, limit=None, expand=None, user=None):
    """# Retrieve paged AiSpeeches
    Receive a list of up to 100 AiSpeech objects previously created in the Stark Infra API and the cursor to the next page. The audio is left out of the results.
    Use this function instead of query if you want to manually page your requests.
    The core derives the response key from the resource name and reads "speechs", but the API answers "speeches", so the list is read here.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - limit [integer, default 100]: maximum number of objects to be retrieved. Max = 100. ex: 35
    - expand [list of strings, default None]: extra attributes to compute. Options: "voice_name".
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of AiSpeech objects with updated attributes
    - cursor to retrieve the next page of AiSpeech objects
    """
    response = rest.get_raw(path=endpoint(_resource), query={"expand": expand, "limit": limit, "cursor": cursor}, user=user)
    content = response.json()
    return [from_api_json(_resource, entity) for entity in content["speeches"]], content.get("cursor")
