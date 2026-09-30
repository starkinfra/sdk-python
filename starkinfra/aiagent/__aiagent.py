from ..utils import rest
from ..aiknowledgebase.__aiknowledgebase import _resource as _knowledge_base_resource
from starkcore.utils.api import from_api_json, endpoint, last_name, last_name_plural
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime


class AiAgent(Resource):
    """# AiAgent object
    An AiAgent is the configuration of an assistant: the model, the instructions, the knowledge it may consult and
    the voice it speaks with. The agent never changes during a conversation; the conversation lives in an AiChat
    and each turn is an AiMessage.
    When you initialize an AiAgent, the entity will not be automatically
    created in the Stark Infra API. The 'create' function sends the object
    to the Stark Infra API and returns the created object.
    ## Parameters (required):
    - name [string]: name of the agent. Between 1 and 100 characters. ex: "Support assistant"
    - model [string]: AI model the agent runs on. Options: "bender-1.0" for everyday conversations, "prime-1.0" for harder reasoning.
    ## Parameters (optional):
    - system_prompt [string, default None]: instructions that define the agent's persona, tone and domain behavior. Up to 100000 characters. The API falls back to its default assistant prompt when omitted.
    - voice_id [string, default None]: id of the AiVoice the agent speaks with. When set, every reply also carries a speech string ready to be sent to AiSpeech. The API does not check that the voice exists.
    - knowledge_base_ids [list of strings, default None]: ids of up to 100 AiKnowledgeBases the agent retrieves from before answering. The API does not check that they exist.
    - metadata_schema [dict, default None]: flat dict whose keys are the fields the agent must extract on every reply. Each field takes a "type" (string, integer, number, boolean or array), an optional "description" of up to 2000 characters, an optional "enum" of up to 20 strings for string fields. The keys are yours and are sent exactly as written. ex: {"order_id": {"type": "string", "description": "Order the customer mentions"}}
    ## Attributes (return-only):
    - id [string]: unique id returned when the AiAgent is created. ex: "5656565656565656"
    - knowledge_bases [list of AiKnowledgeBase objects]: the knowledge bases themselves. Only present when requested with expand=["knowledge_bases"].
    - created [datetime.datetime]: creation datetime for the AiAgent. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - updated [datetime.datetime]: latest update datetime for the AiAgent. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, name, model, system_prompt=None, voice_id=None, knowledge_base_ids=None, metadata_schema=None,
                 id=None, knowledge_bases=None, created=None, updated=None):
        Resource.__init__(self, id=id)

        self.name = name
        self.model = model
        self.system_prompt = system_prompt
        self.voice_id = voice_id
        self.knowledge_base_ids = knowledge_base_ids
        self.metadata_schema = metadata_schema
        self.knowledge_bases = _parse_knowledge_bases(knowledge_bases)
        self.created = check_datetime(created)
        self.updated = check_datetime(updated)


def _parse_knowledge_bases(knowledge_bases):
    if knowledge_bases is None:
        return None
    return [
        knowledge_base if not isinstance(knowledge_base, dict)
        else from_api_json(_knowledge_base_resource, knowledge_base)
        for knowledge_base in knowledge_bases
    ]


_resource = {"class": AiAgent, "name": "AiAgent"}


def create(agent, user=None):
    """# Create an AiAgent
    Send an AiAgent object for creation at the Stark Infra API. Attributes that are None are sent as null.
    The keys of metadata_schema are sent exactly as written, so this function does not go through the case conversion of the core.
    ## Parameters (required):
    - agent [AiAgent object]: AiAgent object to be created in the API.
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - AiAgent object with updated attributes
    """
    payload = {
        "name": agent.name,
        "model": agent.model,
        "systemPrompt": agent.system_prompt,
        "voiceId": agent.voice_id,
        "knowledgeBaseIds": agent.knowledge_base_ids,
        "metadataSchema": agent.metadata_schema,
    }
    response = rest.post_raw(path=endpoint(_resource), payload=payload, user=user)
    return from_api_json(_resource, response.json()[last_name(_resource)])


def get(id, expand=None, user=None):
    """# Retrieve a specific AiAgent
    Receive a single AiAgent object previously created in the Stark Infra API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - expand [list of strings, default None]: extra attributes to compute. Options: "knowledge_bases".
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - AiAgent object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, expand=expand, user=user)


def query(limit=None, expand=None, user=None):
    """# Retrieve AiAgents
    Receive a generator of AiAgent objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - expand [list of strings, default None]: extra attributes to compute. Options: "knowledge_bases".
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - generator of AiAgent objects with updated attributes
    """
    return rest.get_stream(resource=_resource, limit=limit, expand=expand, user=user)


def page(cursor=None, limit=None, expand=None, user=None):
    """# Retrieve paged AiAgents
    Receive a list of up to 100 AiAgent objects previously created in the Stark Infra API and the cursor to the next page.
    Use this function instead of query if you want to manually page your requests.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - limit [integer, default 100]: maximum number of objects to be retrieved. Max = 100. ex: 35
    - expand [list of strings, default None]: extra attributes to compute. Options: "knowledge_bases".
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of AiAgent objects with updated attributes
    - cursor to retrieve the next page of AiAgent objects
    """
    return rest.get_page(resource=_resource, cursor=cursor, limit=limit, expand=expand, user=user)


def update(id, name=None, model=None, system_prompt=None, voice_id=None, knowledge_base_ids=None,
           metadata_schema=None, user=None):
    """# Update AiAgent entity
    Update an AiAgent's parameters by passing its id. The API keeps every parameter you do not give.
    To clear a parameter, send an empty value: "" for system_prompt and voice_id, [] for knowledge_base_ids, {} for metadata_schema.
    The keys of metadata_schema are sent exactly as written, so this function does not go through the case conversion of the core.
    ## Parameters (required):
    - id [string]: AiAgent unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - name [string, default None]: new name for the agent. Between 1 and 100 characters.
    - model [string, default None]: new AI model. Options: "bender-1.0", "prime-1.0"
    - system_prompt [string, default None]: new instructions for the agent. Up to 100000 characters.
    - voice_id [string, default None]: new AiVoice id.
    - knowledge_base_ids [list of strings, default None]: the AiKnowledgeBase ids the agent should end up with. Replaces the current list.
    - metadata_schema [dict, default None]: new schema of the structured data the agent must extract.
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - AiAgent with updated attributes
    """
    payload = {
        "name": name,
        "model": model,
        "systemPrompt": system_prompt,
        "voiceId": voice_id,
        "knowledgeBaseIds": knowledge_base_ids,
        "metadataSchema": metadata_schema,
    }
    response = rest.patch_raw(path="{endpoint}/{id}".format(endpoint=endpoint(_resource), id=id), payload=payload, user=user)
    return from_api_json(_resource, response.json()[last_name(_resource)])


def delete(ids, user=None):
    """# Delete AiAgents
    Delete up to 100 AiAgents at once.
    ## Parameters (required):
    - ids [list of strings]: ids of the AiAgents to be deleted. Up to 100 ids. ex: ["5656565656565656", "4545454545454545"]
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of deleted AiAgent objects
    """
    response = rest.delete_raw(path=endpoint(_resource), query={"ids": ids}, user=user)
    return [from_api_json(_resource, entity) for entity in response.json()[last_name_plural(_resource)]]
