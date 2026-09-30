from ..utils import rest
from starkcore.utils.api import from_api_json, endpoint, last_name, last_name_plural
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime


class AiChat(Resource):
    """# AiChat object
    An AiChat is one conversation thread with an AiAgent and holds the history. Each turn is an AiMessage.
    When you initialize an AiChat, the entity will not be automatically
    created in the Stark Infra API. The 'create' function sends the object
    to the Stark Infra API and returns the created object.
    ## Parameters (required):
    - agent_id [string]: id of the AiAgent that will answer in this chat. ex: "5656565656565656"
    ## Parameters (optional):
    - title [string, default None]: title of the conversation. Up to 100 characters. When omitted, the first message posted to the chat generates one.
    - tags [list of strings, default None]: tags to find the chat later. Up to 30 tags. ex: ["customer-123", "whatsapp"]
    - context [dict, default None]: what the agent should know about the person it is talking to, read before every reply as data and never as instructions. Up to 16384 bytes. The keys are yours and are sent exactly as written. ex: {"name": "Ana", "balance": 1520.33}
    ## Attributes (return-only):
    - id [string]: unique id returned when the AiChat is created. ex: "5656565656565656"
    - agent_name [string]: name of the agent. Only present when requested with expand=["agent_name"].
    - updated [datetime.datetime]: latest update datetime for the AiChat. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, agent_id, title=None, tags=None, context=None, id=None, agent_name=None, updated=None):
        Resource.__init__(self, id=id)

        self.agent_id = agent_id
        self.title = title
        self.tags = tags
        self.context = context
        self.agent_name = agent_name
        self.updated = check_datetime(updated)


_resource = {"class": AiChat, "name": "AiChat"}


def create(chat, user=None):
    """# Create an AiChat
    Send an AiChat object for creation at the Stark Infra API. Attributes that are None are sent as null.
    The keys of context are sent exactly as written, so this function does not go through the case conversion of the core.
    ## Parameters (required):
    - chat [AiChat object]: AiChat object to be created in the API.
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - AiChat object with updated attributes
    """
    payload = {
        "agentId": chat.agent_id,
        "title": chat.title,
        "tags": chat.tags,
        "context": chat.context,
    }
    response = rest.post_raw(path=endpoint(_resource), payload=payload, user=user)
    return from_api_json(_resource, response.json()[last_name(_resource)])


def get(id, expand=None, user=None):
    """# Retrieve a specific AiChat
    Receive a single AiChat object previously created in the Stark Infra API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - expand [list of strings, default None]: extra attributes to compute. Options: "agent_name".
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - AiChat object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, expand=expand, user=user)


def query(limit=None, expand=None, tags=None, user=None):
    """# Retrieve AiChats
    Receive a generator of AiChat objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - expand [list of strings, default None]: extra attributes to compute. Options: "agent_name".
    - tags [list of strings, default None]: up to 30 tags. Returns the chats that contain any of them. ex: ["customer-123", "whatsapp"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - generator of AiChat objects with updated attributes
    """
    return rest.get_stream(resource=_resource, limit=limit, expand=expand, tags=tags, user=user)


def page(cursor=None, limit=None, expand=None, tags=None, user=None):
    """# Retrieve paged AiChats
    Receive a list of up to 100 AiChat objects previously created in the Stark Infra API and the cursor to the next page.
    Use this function instead of query if you want to manually page your requests.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - limit [integer, default 100]: maximum number of objects to be retrieved. Max = 100. ex: 35
    - expand [list of strings, default None]: extra attributes to compute. Options: "agent_name".
    - tags [list of strings, default None]: up to 30 tags. Returns the chats that contain any of them. ex: ["customer-123", "whatsapp"]
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of AiChat objects with updated attributes
    - cursor to retrieve the next page of AiChat objects
    """
    return rest.get_page(resource=_resource, cursor=cursor, limit=limit, expand=expand, tags=tags, user=user)


def update(id, title=None, agent_id=None, tags=None, context=None, user=None):
    """# Update AiChat entity
    Update an AiChat's parameters by passing its id. The API keeps every parameter you do not give.
    To clear a parameter, send an empty value: [] for tags, {} for context.
    The keys of context are sent exactly as written, so this function does not go through the case conversion of the core.
    ## Parameters (required):
    - id [string]: AiChat unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - title [string, default None]: new title for the conversation. Up to 100 characters.
    - agent_id [string, default None]: id of the AiAgent that should answer from now on.
    - tags [list of strings, default None]: the tags the chat should end up with. Replaces the current list.
    - context [dict, default None]: the context the agent should read from now on. Replaces the current one.
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - AiChat with updated attributes
    """
    payload = {
        "title": title,
        "agentId": agent_id,
        "tags": tags,
        "context": context,
    }
    response = rest.patch_raw(path="{endpoint}/{id}".format(endpoint=endpoint(_resource), id=id), payload=payload, user=user)
    return from_api_json(_resource, response.json()[last_name(_resource)])


def delete(ids, user=None):
    """# Delete AiChats
    Delete up to 100 AiChats at once, with their messages.
    ## Parameters (required):
    - ids [list of strings]: ids of the AiChats to be deleted. Up to 100 ids. ex: ["5656565656565656", "4545454545454545"]
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of deleted AiChat objects
    """
    response = rest.delete_raw(path=endpoint(_resource), query={"ids": ids}, user=user)
    return [from_api_json(_resource, entity) for entity in response.json()[last_name_plural(_resource)]]
