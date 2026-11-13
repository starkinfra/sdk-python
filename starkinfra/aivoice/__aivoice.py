from ..utils import rest
from starkcore.utils.api import from_api_json, endpoint, last_name_plural
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime


class AiVoice(Resource):
    """# AiVoice object
    An AiVoice is a voice cloned from a recording you upload. Once cloned, it can read any text out loud through
    an AiSpeech, and it can be attached to an AiAgent so every reply carries a speech ready to be synthesized.
    Cloning is asynchronous: the voice is created in "processing" status and moves to "success" when it is ready
    to speak, or to "failed" when the recording could not be cloned.
    When you initialize an AiVoice, the entity will not be automatically
    created in the Stark Infra API. The 'create' function sends the object
    to the Stark Infra API and returns the created object.
    ## Parameters (required):
    - audio [string]: base64-encoded recording of the speaker. MP3, WAV, OGG, FLAC and WebM are accepted. Up to 10000000 characters.
    ## Parameters (optional):
    - name [string, default None]: name of the voice. Up to 100 characters. Defaults to the voice's own id. ex: "Helena"
    - description [string, default None]: free-text description of the voice. Up to 1000 characters.
    - language [string, default None]: language the voice speaks. Options: "portuguese", "english". The API defaults to "portuguese".
    - gender [string, default None]: gender of the voice. Options: "male", "female", "neutral"
    ## Attributes (return-only):
    - id [string]: unique id returned when the AiVoice is created. This is the voice_id you send to other AI resources. ex: "5656565656565656"
    - status [string]: current status of the voice. Options: "processing", "success", "failed". Only a voice in "success" can speak.
    - errors [list of strings]: reasons the cloning failed. Empty while the voice is healthy.
    - created [datetime.datetime]: creation datetime for the AiVoice. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - updated [datetime.datetime]: latest update datetime for the AiVoice. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, audio=None, name=None, description=None, language=None, gender=None, id=None, status=None,
                 errors=None, created=None, updated=None):
        Resource.__init__(self, id=id)

        self.audio = audio
        self.name = name
        self.description = description
        self.language = language
        self.gender = gender
        self.status = status
        self.errors = errors
        self.created = check_datetime(created)
        self.updated = check_datetime(updated)


_resource = {"class": AiVoice, "name": "AiVoice"}


def create(voice, user=None):
    """# Create an AiVoice
    Send an AiVoice object for creation at the Stark Infra API and start cloning it.
    The call returns immediately with the voice in "processing" status.
    ## Parameters (required):
    - voice [AiVoice object]: AiVoice object to be created in the API.
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - AiVoice object with updated attributes
    """
    return rest.post_single(resource=_resource, entity=voice, user=user)


def query(limit=None, user=None):
    """# Retrieve AiVoices
    Receive a generator of AiVoice objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - generator of AiVoice objects with updated attributes
    """
    return rest.get_stream(resource=_resource, limit=limit, user=user)


def page(cursor=None, limit=None, user=None):
    """# Retrieve paged AiVoices
    Receive a list of up to 100 AiVoice objects previously created in the Stark Infra API and the cursor to the next page.
    Use this function instead of query if you want to manually page your requests.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - limit [integer, default 100]: maximum number of objects to be retrieved. Max = 100. ex: 35
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of AiVoice objects with updated attributes
    - cursor to retrieve the next page of AiVoice objects
    """
    return rest.get_page(resource=_resource, cursor=cursor, limit=limit, user=user)


def delete(ids, user=None):
    """# Delete AiVoices
    Delete up to 100 AiVoices at once.
    ## Parameters (required):
    - ids [list of strings]: ids of the AiVoices to be deleted. Up to 100 ids. ex: ["5656565656565656", "4545454545454545"]
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of deleted AiVoice objects
    """
    response = rest.delete_raw(path=endpoint(_resource), query={"ids": ids}, user=user)
    return [from_api_json(_resource, entity) for entity in response.json()[last_name_plural(_resource)]]
