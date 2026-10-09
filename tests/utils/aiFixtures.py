import atexit
from json import dumps
from urllib.parse import urlparse, parse_qs
from uuid import uuid4
import starkinfra


_created = {"knowledgeBase": None, "agent": None, "chat": None}


def _name(prefix):
    return "{}-{}".format(prefix, uuid4().hex[:12])


def knowledgeBase():
    if _created["knowledgeBase"] is None:
        _created["knowledgeBase"] = starkinfra.aiknowledgebase.create(starkinfra.AiKnowledgeBase(
            name=_name("sdk-python-kb"),
            root_url="https://docs.starkinfra.com",
            is_recursive=False,
            tags=["sdk-python", "test"],
        ))
    return _created["knowledgeBase"]


def agent():
    if _created["agent"] is None:
        _created["agent"] = starkinfra.aiagent.create(generateExampleAiAgent(knowledge_base_ids=[knowledgeBase().id]))
    return _created["agent"]


def chat():
    if _created["chat"] is None:
        _created["chat"] = starkinfra.aichat.create(starkinfra.AiChat(agent_id=agent().id, title=_name("sdk-python-chat")))
    return _created["chat"]


def generateExampleAiAgent(knowledge_base_ids=None):
    return starkinfra.AiAgent(
        name=_name("sdk-python-agent"),
        model="bender-1.0",
        system_prompt="Answer in one short sentence.",
        knowledge_base_ids=knowledge_base_ids,
        metadata_schema={"order_id": {"type": "string", "description": "Order the customer mentions"}},
    )


def queryOf(url):
    return {key: values[0] for key, values in parse_qs(urlparse(url).query).items()}


def speechAudio():
    finished = next((speech for speech in starkinfra.aispeech.query() if speech.status == "success"), None)
    if finished is None:
        return None
    return starkinfra.aispeech.get(finished.id).audio


def _cleanup():
    for key, module in [("chat", starkinfra.aichat), ("agent", starkinfra.aiagent), ("knowledgeBase", starkinfra.aiknowledgebase)]:
        entity = _created[key]
        if entity is None:
            continue
        module.delete([entity.id])


atexit.register(_cleanup)


class FakeResponse:

    def __init__(self, body):
        self.status_code = 200
        self.content = dumps(body).encode("utf-8")
        self.headers = {}
