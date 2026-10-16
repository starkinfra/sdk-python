import starkinfra
from datetime import datetime
from unittest import TestCase, main
from tests.utils.user import exampleProject
from tests.utils import aiFixtures


starkinfra.user = exampleProject

_agent = {
    "id": "5740688905863168",
    "name": "Support assistant",
    "model": "bender-1.0",
    "systemPrompt": "Answer in one short sentence.",
    "voiceId": "",
    "knowledgeBaseIds": ["5083538508480512"],
    "metadataSchema": {"order_id": {"type": "string"}},
    "created": "2026-09-30T15:42:56.879325+00:00",
    "updated": "2026-09-30T15:42:56.879334+00:00",
}


class TestAiAgent(TestCase):

    def test_create_returns_the_agent_with_the_schema_keys_in_camel_case(self):
        agent = aiFixtures.agent()
        self.assertIsNotNone(agent.id)
        self.assertEqual("bender-1.0", agent.model)
        self.assertEqual([aiFixtures.knowledgeBase().id], agent.knowledge_base_ids)
        self.assertEqual(["orderId"], list(agent.metadata_schema))
        self.assertIsInstance(agent.created, datetime)

    def test_get_and_expand_knowledge_bases(self):
        agent = aiFixtures.agent()
        plain = starkinfra.aiagent.get(agent.id)
        self.assertEqual(agent.id, plain.id)
        self.assertIsNone(plain.knowledge_bases)
        expanded = starkinfra.aiagent.get(agent.id, expand=["knowledge_bases"])
        self.assertEqual([aiFixtures.knowledgeBase().id], [kb.id for kb in expanded.knowledge_bases])
        self.assertIsInstance(expanded.knowledge_bases[0], starkinfra.AiKnowledgeBase)

    def test_query_with_limit_stops_at_the_limit(self):
        aiFixtures.agent()
        self.assertEqual(1, len(list(starkinfra.aiagent.query(limit=1))))

    def test_page_returns_the_agents_and_a_cursor_to_the_next_page(self):
        agent = aiFixtures.agent()
        found = []
        cursor = None
        while True:
            agents, cursor = starkinfra.aiagent.page(limit=1, cursor=cursor)
            self.assertLessEqual(len(agents), 1)
            found.extend(agents)
            if cursor is None:
                break
        self.assertIn(agent.id, [entity.id for entity in found])
        self.assertEqual(len(found), len({entity.id for entity in found}))

    def test_update_keeps_the_knowledge_bases_it_was_not_asked_to_change(self):
        agent = aiFixtures.agent()
        original = starkinfra.aiagent.get(agent.id)
        try:
            renamed = starkinfra.aiagent.update(agent.id, name="renamed-by-sdk")
            self.assertEqual("renamed-by-sdk", renamed.name)
            self.assertEqual([aiFixtures.knowledgeBase().id], renamed.knowledge_base_ids)
            self.assertEqual(["orderId"], list(renamed.metadata_schema))
        finally:
            starkinfra.aiagent.update(agent.id, name=original.name)

    def test_update_with_an_empty_list_clears_the_knowledge_bases(self):
        agent = starkinfra.aiagent.create(aiFixtures.generateExampleAiAgent(knowledge_base_ids=[aiFixtures.knowledgeBase().id]))
        try:
            cleared = starkinfra.aiagent.update(agent.id, knowledge_base_ids=[])
            self.assertEqual([], cleared.knowledge_base_ids)
        finally:
            starkinfra.aiagent.delete([agent.id])

    def test_update_with_an_empty_system_prompt_and_voice_clears_them(self):
        agent = starkinfra.aiagent.create(aiFixtures.generateExampleAiAgent())
        try:
            cleared = starkinfra.aiagent.update(agent.id, system_prompt="", voice_id="")
            self.assertEqual("", cleared.system_prompt)
            self.assertEqual("", cleared.voice_id)
        finally:
            starkinfra.aiagent.delete([agent.id])

    def test_delete_returns_the_deleted_agents(self):
        agent = starkinfra.aiagent.create(aiFixtures.generateExampleAiAgent())
        deleted = starkinfra.aiagent.delete([agent.id])
        self.assertEqual([agent.id], [entity.id for entity in deleted])

    def test_create_with_invalid_model_raises_input_errors(self):
        with self.assertRaises(starkinfra.error.InputErrors):
            starkinfra.aiagent.create(starkinfra.AiAgent(name="invalid", model="gpt"))

    def test_page_with_a_limit_above_the_maximum_raises_input_errors(self):
        with self.assertRaises(starkinfra.error.InputErrors):
            starkinfra.aiagent.page(limit=101)

    def test_get_unknown_id_raises_input_errors(self):
        with self.assertRaises(starkinfra.error.InputErrors):
            starkinfra.aiagent.get("0000000000000000")


if __name__ == '__main__':
    main()
