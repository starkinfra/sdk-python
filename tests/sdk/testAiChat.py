import starkinfra
from json import loads
from unittest import TestCase, main
from unittest.mock import patch
from tests.utils.user import exampleProject
from tests.utils import aiFixtures
from tests.utils.aiFixtures import FakeResponse, queryOf


starkinfra.user = exampleProject

_chat = {
    "id": "5761660895625216",
    "agentId": "5740688905863168",
    "title": "Support chat",
    "tags": ["customer-123", "whatsapp"],
    "context": {"name": "Ana", "balance": 1520.33},
    "updated": "2026-09-30T15:42:58.464506+00:00",
}


class TestAiChat(TestCase):

    def test_create_returns_the_chat(self):
        chat = aiFixtures.chat()
        self.assertIsNotNone(chat.id)
        self.assertEqual(aiFixtures.agent().id, chat.agent_id)
        self.assertEqual([], chat.tags)
        self.assertEqual({}, chat.context)

    def test_create_keeps_the_tags_and_the_context_keys_as_written(self):
        chat = starkinfra.aichat.create(starkinfra.AiChat(
            agent_id=aiFixtures.agent().id,
            tags=["sdk-python", "tagged"],
            context={"customer_name": "Ana", "balance": 1520.33},
        ))
        try:
            self.assertEqual(["sdk-python", "tagged"], chat.tags)
            self.assertEqual({"customer_name": "Ana", "balance": 1520.33}, chat.context)
        finally:
            starkinfra.aichat.delete([chat.id])

    def test_get_and_expand_agent_name(self):
        chat = aiFixtures.chat()
        self.assertIsNone(starkinfra.aichat.get(chat.id).agent_name)
        self.assertEqual(aiFixtures.agent().name, starkinfra.aichat.get(chat.id, expand=["agent_name"]).agent_name)

    def test_query(self):
        chat = aiFixtures.chat()
        self.assertIn(chat.id, [entity.id for entity in starkinfra.aichat.query()])

    def test_query_with_limit_stops_at_the_limit(self):
        aiFixtures.chat()
        self.assertEqual(1, len(list(starkinfra.aichat.query(limit=1))))

    def test_query_filters_by_tags(self):
        chat = starkinfra.aichat.create(starkinfra.AiChat(agent_id=aiFixtures.agent().id, tags=["sdk-python-filter"]))
        try:
            found = list(starkinfra.aichat.query(tags=["sdk-python-filter", "unused"]))
            self.assertEqual([chat.id], [entity.id for entity in found])
        finally:
            starkinfra.aichat.delete([chat.id])

    def test_page_returns_the_chats_and_a_cursor_to_the_next_page(self):
        chat = aiFixtures.chat()
        found = []
        cursor = None
        while True:
            chats, cursor = starkinfra.aichat.page(limit=1, cursor=cursor)
            self.assertLessEqual(len(chats), 1)
            found.extend(chats)
            if cursor is None:
                break
        self.assertIn(chat.id, [entity.id for entity in found])

    def test_update_changes_only_the_title(self):
        chat = aiFixtures.chat()
        try:
            updated = starkinfra.aichat.update(chat.id, title="renamed-by-sdk")
            self.assertEqual("renamed-by-sdk", updated.title)
            self.assertEqual(chat.agent_id, updated.agent_id)
        finally:
            starkinfra.aichat.update(chat.id, title=chat.title)

    def test_update_replaces_the_tags_and_the_context_and_empty_values_clear_them(self):
        chat = starkinfra.aichat.create(starkinfra.AiChat(agent_id=aiFixtures.agent().id, tags=["before"], context={"a": 1}))
        try:
            updated = starkinfra.aichat.update(chat.id, tags=["after"], context={"b": 2})
            self.assertEqual(["after"], updated.tags)
            self.assertEqual({"b": 2}, updated.context)
            cleared = starkinfra.aichat.update(chat.id, tags=[], context={})
            self.assertEqual([], cleared.tags)
            self.assertEqual({}, cleared.context)
        finally:
            starkinfra.aichat.delete([chat.id])

    def test_delete_returns_the_deleted_chats(self):
        chat = starkinfra.aichat.create(starkinfra.AiChat(agent_id=aiFixtures.agent().id, title="sdk-python-delete"))
        self.assertEqual([chat.id], [entity.id for entity in starkinfra.aichat.delete([chat.id])])

    def test_create_with_unknown_agent_raises_input_errors(self):
        with self.assertRaises(starkinfra.error.InputErrors):
            starkinfra.aichat.create(starkinfra.AiChat(agent_id="0000000000000000"))

    def test_get_unknown_id_raises_input_errors(self):
        with self.assertRaises(starkinfra.error.InputErrors):
            starkinfra.aichat.get("0000000000000000")


class TestAiChatAtTheHttpBoundary(TestCase):

    def test_create_sends_only_the_creatable_fields_and_does_not_touch_the_context_keys(self):
        returned = starkinfra.AiChat(
            agent_id="5740688905863168", title="Support chat", tags=["customer-123"], context={"customer_name": "Ana"},
            id="5761660895625216", agent_name="Support assistant", updated="2026-09-30T15:42:58+00:00",
        )
        with patch("starkcore.utils.rest.post", return_value=FakeResponse({"chat": _chat})) as post:
            starkinfra.aichat.create(returned)
        self.assertEqual({
            "agentId": "5740688905863168",
            "title": "Support chat",
            "tags": ["customer-123"],
            "context": {"customer_name": "Ana"},
        }, loads(post.call_args.kwargs["data"]))

    def test_update_names_every_field_and_sends_none_for_the_ones_not_given(self):
        with patch("starkcore.utils.rest.patch", return_value=FakeResponse({"chat": _chat})) as patch_request:
            starkinfra.aichat.update("5761660895625216", title="New title")
        self.assertEqual(
            {"title": "New title", "agentId": None, "tags": None, "context": None},
            loads(patch_request.call_args.kwargs["data"]),
        )

    def test_update_sends_tags_and_context_as_they_came(self):
        with patch("starkcore.utils.rest.patch", return_value=FakeResponse({"chat": _chat})) as patch_request:
            starkinfra.aichat.update("5761660895625216", tags=[], context={"customer_name": "Ana"})
        body = loads(patch_request.call_args.kwargs["data"])
        self.assertEqual([], body["tags"])
        self.assertEqual({"customer_name": "Ana"}, body["context"])

    def test_query_sends_the_tags_as_a_comma_separated_list(self):
        with patch("starkcore.utils.rest.get", return_value=FakeResponse({"cursor": None, "chats": [_chat]})) as get:
            found = list(starkinfra.aichat.query(tags=["customer-123", "whatsapp"], expand=["agent_name"]))
        self.assertEqual(["5761660895625216"], [chat.id for chat in found])
        self.assertEqual({"tags": "customer-123,whatsapp", "expand": "agentName"}, queryOf(get.call_args.kwargs["url"]))

    def test_page_returns_the_items_and_the_cursor(self):
        with patch("starkcore.utils.rest.get", return_value=FakeResponse({"cursor": "next-page", "chats": [_chat]})) as get:
            chats, cursor = starkinfra.aichat.page(limit=1, cursor="current-page", tags=["whatsapp"])
        self.assertEqual(["5761660895625216"], [chat.id for chat in chats])
        self.assertEqual("next-page", cursor)
        self.assertEqual({"limit": "1", "cursor": "current-page", "tags": "whatsapp"}, queryOf(get.call_args.kwargs["url"]))

    def test_page_returns_a_null_cursor_on_the_last_page(self):
        with patch("starkcore.utils.rest.get", return_value=FakeResponse({"cursor": None, "chats": [_chat]})):
            _, cursor = starkinfra.aichat.page()
        self.assertIsNone(cursor)


if __name__ == '__main__':
    main()
