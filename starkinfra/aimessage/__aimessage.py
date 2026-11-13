from ..utils import rest
from starkcore.utils.api import from_api_json, endpoint
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime


class AiMessage(Resource):
    """# AiMessage object
    An AiMessage is a single turn of an AiChat. You post what the user said and the same call returns the user's
    message and the agent's answer.
    When you initialize an AiMessage, the entity will not be automatically
    created in the Stark Infra API. The 'create' function sends the object
    to the Stark Infra API and returns the user's message and the agent's answer.
    ## Parameters (required):
    - chat_id [string]: id of the AiChat to post to. ex: "5656565656565656"
    - text [string]: content of the user's message. Between 1 and 50000 characters. ex: "What is the status of my order?"
    ## Parameters (optional):
    - model [string, default None]: AI model to use for this turn only. Options: "bender-1.0", "prime-1.0". The API defaults to the agent's own model.
    ## Attributes (return-only):
    - id [string]: unique id of the AiMessage. ex: "5656565656565656"
    - sender [string]: who wrote the message. Options: "user", "system". The agent's answers are sent by "system".
    - speech [string]: version of the text written to be heard rather than read, ready to be sent to AiSpeech. Only filled when the agent has a voice.
    - metadata [dict]: structured data the agent extracted, shaped by the agent's metadata_schema. The keys are the agent's, exactly as it declared them.
    - chat_name [string]: title of the chat. Only present when create is called with expand=["chat_name"].
    - created [datetime.datetime]: creation datetime for the AiMessage. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, chat_id, text, model=None, id=None, sender=None, speech=None, metadata=None, chat_name=None,
                 created=None):
        Resource.__init__(self, id=id)

        self.chat_id = chat_id
        self.text = text
        self.model = model
        self.sender = sender
        self.speech = speech
        self.metadata = metadata
        self.chat_name = chat_name
        self.created = check_datetime(created)


_resource = {"class": AiMessage, "name": "AiMessage"}


def create(message, expand=None, user=None):
    """# Create an AiMessage
    Post the user's message to an AiChat. The call waits for the agent and returns both messages.
    The API answers with a list and takes expand in the query string, so this function does not go through the standard create of the core.
    ## Parameters (required):
    - message [AiMessage object]: AiMessage object with chat_id and text, to be created in the API.
    ## Parameters (optional):
    - expand [list of strings, default None]: extra attributes to compute. Options: "chat_name", which returns the chat title on every message, useful on the first turn, when the title is generated.
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list with the user's AiMessage and the agent's AiMessage
    """
    payload = {"chatId": message.chat_id, "text": message.text, "model": message.model}
    response = rest.post_raw(path=endpoint(_resource), payload=payload, query={"expand": expand}, user=user)
    content = response.json()
    messages = [from_api_json(_resource, entity) for entity in content["messages"]]
    for entity in messages:
        entity.chat_name = content.get("chatName")
    return messages


def query(limit=None, chat_id=None, user=None):
    """# Retrieve AiMessages
    Receive a generator of the AiMessage objects previously created in the Stark Infra API, newest first, following the cursor until the history ends.
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - chat_id [string, default None]: id of the AiChat whose messages you want. Without it, the messages of every chat in your workspace are returned. ex: "5656565656565656"
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - generator of AiMessage objects with updated attributes
    """
    return rest.get_stream(resource=_resource, limit=limit, chat_id=chat_id, user=user)


def page(cursor=None, limit=None, chat_id=None, user=None):
    """# Retrieve paged AiMessages
    Receive a list of up to 100 AiMessage objects, newest first, and the cursor to the next page.
    Use this function instead of query if you want to manually page your requests.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - limit [integer, default 100]: maximum number of objects to be retrieved. Max = 100. ex: 35
    - chat_id [string, default None]: id of the AiChat whose messages you want. Without it, the messages of every chat in your workspace are returned. ex: "5656565656565656"
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of AiMessage objects with updated attributes
    - cursor to retrieve the next page of AiMessage objects
    """
    return rest.get_page(resource=_resource, chat_id=chat_id, cursor=cursor, limit=limit, user=user)
