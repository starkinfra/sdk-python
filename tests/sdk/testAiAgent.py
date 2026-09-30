import starkinfra
from json import loads
from datetime import datetime
from unittest import TestCase, main
from unittest.mock import patch
from tests.utils.user import exampleProject
from tests.utils import aiFixtures
from tests.utils.aiFixtures import FakeResponse, queryOf


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

    def test_create_returns_the_agent_with_the_schema_keys_as_written(self):
        agent = aiFixtures.agent()
        self.assertIsNotNone(agent.id)
        self.assertEqual("bender-1.0", agent.model)
        self.assertEqual([aiFixtures.knowledgeBase().id], agent.knowledge_base_ids)
        self.assertEqual(["order_id"], list(agent.metadata_schema))
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
            self.assertEqual(["order_id"], list(renamed.metadata_schema))
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


class TestAiAgentAtTheHttpBoundary(TestCase):

    def test_create_does_not_touch_the_schema_keys(self):
        returned = starkinfra.AiAgent(
            name="Support assistant", model="bender-1.0", system_prompt="Be brief.", voice_id="5632499082330112",
            knowledge_base_ids=["5083538508480512"], metadata_schema={"order_id": {"type": "string"}, "isUrgent": {"type": "boolean"}},
            id="5740688905863168", created="2026-09-30T15:42:56+00:00", updated="2026-09-30T15:42:56+00:00",
        )
        with patch("starkcore.utils.rest.post", return_value=FakeResponse({"agent": _agent})) as post:
            starkinfra.aiagent.create(returned)
        self.assertEqual({
            "name": "Support assistant",
            "model": "bender-1.0",
            "systemPrompt": "Be brief.",
            "voiceId": "5632499082330112",
            "knowledgeBaseIds": ["5083538508480512"],
            "metadataSchema": {"order_id": {"type": "string"}, "isUrgent": {"type": "boolean"}},
        }, loads(post.call_args.kwargs["data"]))

    def test_create_sends_an_empty_voice_as_it_came(self):
        with patch("starkcore.utils.rest.post", return_value=FakeResponse({"agent": _agent})) as post:
            starkinfra.aiagent.create(starkinfra.AiAgent(name="a", model="bender-1.0", voice_id=""))
        self.assertEqual("", loads(post.call_args.kwargs["data"])["voiceId"])

    def test_update_does_not_read_the_agent_first(self):
        with patch("starkcore.utils.rest.get") as get, \
                patch("starkcore.utils.rest.patch", return_value=FakeResponse({"agent": _agent})) as patch_request:
            starkinfra.aiagent.update("5740688905863168", name="Renamed")
        get.assert_not_called()
        self.assertEqual(
            {"name": "Renamed", "model": None, "systemPrompt": None, "voiceId": None, "knowledgeBaseIds": None, "metadataSchema": None},
            loads(patch_request.call_args.kwargs["data"]),
        )

    def test_update_sends_empty_values_to_clear_the_fields(self):
        with patch("starkcore.utils.rest.patch", return_value=FakeResponse({"agent": _agent})) as patch_request:
            starkinfra.aiagent.update("5740688905863168", system_prompt="", voice_id="", knowledge_base_ids=[], metadata_schema={})
        body = loads(patch_request.call_args.kwargs["data"])
        self.assertEqual("", body["systemPrompt"])
        self.assertEqual("", body["voiceId"])
        self.assertEqual([], body["knowledgeBaseIds"])
        self.assertEqual({}, body["metadataSchema"])

    def test_page_returns_the_items_and_the_cursor(self):
        with patch("starkcore.utils.rest.get", return_value=FakeResponse({"cursor": "next-page", "agents": [_agent]})) as get:
            agents, cursor = starkinfra.aiagent.page(limit=1, cursor="current-page", expand=["knowledge_bases"])
        self.assertEqual(["5740688905863168"], [agent.id for agent in agents])
        self.assertEqual("next-page", cursor)
        self.assertEqual({"limit": "1", "cursor": "current-page", "expand": "knowledgeBases"}, queryOf(get.call_args.kwargs["url"]))

    def test_page_returns_a_null_cursor_on_the_last_page(self):
        with patch("starkcore.utils.rest.get", return_value=FakeResponse({"cursor": None, "agents": [_agent]})) as get:
            _, cursor = starkinfra.aiagent.page()
        self.assertIsNone(cursor)
        self.assertEqual({}, queryOf(get.call_args.kwargs["url"]))

    def test_delete_sends_ids_in_the_query_string(self):
        with patch("starkcore.utils.rest.delete", return_value=FakeResponse({"agents": [_agent]})) as delete:
            deleted = starkinfra.aiagent.delete(["5740688905863168", "5740688905863169"])
        self.assertTrue(delete.call_args.kwargs["url"].endswith("/v2/ai-agent?ids=5740688905863168%2C5740688905863169"))
        self.assertEqual("", delete.call_args.kwargs["data"])
        self.assertEqual(["5740688905863168"], [agent.id for agent in deleted])


if __name__ == '__main__':
    main()
