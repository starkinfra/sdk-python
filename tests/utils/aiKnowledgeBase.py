from uuid import uuid4
import starkinfra


def generateExampleAiKnowledgeBase():
    return starkinfra.AiKnowledgeBase(
        name="sdk-python-{}".format(uuid4().hex[:12]),
        root_url="https://docs.starkinfra.com",
        is_recursive=False,
        tags=["sdk-python", "test"],
    )
