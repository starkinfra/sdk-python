import starkinfra
from json import loads
from datetime import datetime
from unittest import TestCase, main
from unittest.mock import patch
from tests.utils.user import exampleProject
from tests.utils import aiFixtures
from tests.utils.aiFixtures import FakeResponse, queryOf


starkinfra.user = exampleProject

_messages = [
    {"id": "5642368648740864", "chatId": "5632499082330112", "sender": "user", "text": "Say hello.", "speech": "Say hello.",
     "metadata": {}, "model": "bender-1.0", "created": "2026-10-01T14:28:02.652375+00:00"},
    {"id": "5079418695319552", "chatId": "5632499082330112", "sender": "system", "text": "Hello!", "speech": "Hello!",
     "metadata": {"order_id": "123"}, "model": "bender-1.0", "created": "2026-10-01T14:28:02.653375+00:00"},
]


class TestAiMessage(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.chat = aiFixtures.chat()
        cls.posted = starkinfra.aimessage.create(
            starkinfra.AiMessage(chat_id=cls.chat.id, text="Say hello and mention order 123."),
            expand=["chat_name"],
        )

    def test_create_returns_the_user_message_and_the_answer(self):
        self.assertEqual(["user", "system"], [message.sender for message in self.posted])
        for message in self.posted:
            self.assertEqual(self.chat.id, message.chat_id)
            self.assertIsInstance(message.created, datetime)
            self.assertTrue(message.chat_name)

    def test_the_answer_carries_a_metadata_dict(self):
        self.assertIsInstance(self.posted[1].metadata, dict)

    def test_query_returns_the_whole_history(self):
        found = list(starkinfra.aimessage.query(chat_id=self.chat.id))
        self.assertEqual({message.id for message in self.posted}, {message.id for message in found})

    def test_query_with_limit_stops_at_the_limit(self):
        self.assertEqual(1, len(list(starkinfra.aimessage.query(chat_id=self.chat.id, limit=1))))

    def test_page_returns_a_cursor_that_leads_to_the_next_page(self):
        first, cursor = starkinfra.aimessage.page(chat_id=self.chat.id, limit=1)
        self.assertEqual(1, len(first))
        self.assertIsNotNone(cursor)
        second, _ = starkinfra.aimessage.page(chat_id=self.chat.id, cursor=cursor, limit=1)
        self.assertEqual(1, len(second))
        self.assertNotEqual(first[0].id, second[0].id)

    def test_query_without_chat_id_returns_the_messages_of_the_workspace(self):
        found = list(starkinfra.aimessage.query(limit=5))
        self.assertTrue(found)
        self.assertLessEqual(len(found), 5)

    def test_page_with_a_limit_above_the_maximum_raises_input_errors(self):
        with self.assertRaises(starkinfra.error.InputErrors):
            starkinfra.aimessage.page(chat_id=self.chat.id, limit=101)

    def test_create_in_an_unknown_chat_raises_input_errors(self):
        with self.assertRaises(starkinfra.error.InputErrors):
            starkinfra.aimessage.create(starkinfra.AiMessage(chat_id="0000000000000000", text="hi"))


class TestAiMessageAtTheHttpBoundary(TestCase):

    def test_create_sends_expand_in_the_query_string_and_not_in_the_body(self):
        body = {"chatName": "Greeting", "messages": _messages}
        with patch("starkcore.utils.rest.post", return_value=FakeResponse(body)) as post:
            messages = starkinfra.aimessage.create(
                starkinfra.AiMessage(chat_id="5632499082330112", text="Say hello.", model="prime-1.0"),
                expand=["chat_name"],
            )
        self.assertTrue(post.call_args.kwargs["url"].endswith("/v2/ai-message?expand=chatName"))
        self.assertEqual({"chatId": "5632499082330112", "text": "Say hello.", "model": "prime-1.0"}, loads(post.call_args.kwargs["data"]))
        self.assertEqual(["user", "system"], [message.sender for message in messages])
        self.assertEqual({"Greeting"}, {message.chat_name for message in messages})

    def test_create_without_model_and_expand_sends_a_null_model_and_no_query_string(self):
        with patch("starkcore.utils.rest.post", return_value=FakeResponse({"messages": _messages})) as post:
            messages = starkinfra.aimessage.create(starkinfra.AiMessage(chat_id="5632499082330112", text="Say hello."))
        self.assertTrue(post.call_args.kwargs["url"].endswith("/v2/ai-message"))
        self.assertEqual({"chatId": "5632499082330112", "text": "Say hello.", "model": None}, loads(post.call_args.kwargs["data"]))
        self.assertEqual([None, None], [message.chat_name for message in messages])

    def test_query_follows_the_cursor_until_it_runs_out(self):
        pages = [
            FakeResponse({"cursor": "next-page", "messages": [_messages[0]]}),
            FakeResponse({"cursor": None, "messages": [_messages[1]]}),
        ]
        with patch("starkcore.utils.rest.get", side_effect=pages) as get:
            found = list(starkinfra.aimessage.query(chat_id="5632499082330112"))
        self.assertEqual(["5642368648740864", "5079418695319552"], [message.id for message in found])
        self.assertIn("chatId=5632499082330112", get.call_args_list[0].kwargs["url"])
        self.assertIn("cursor=next-page", get.call_args_list[1].kwargs["url"])

    def test_query_without_chat_id_does_not_send_it(self):
        with patch("starkcore.utils.rest.get", return_value=FakeResponse({"cursor": None, "messages": _messages})) as get:
            found = list(starkinfra.aimessage.query())
        self.assertEqual(2, len(found))
        self.assertEqual({}, queryOf(get.call_args.kwargs["url"]))

    def test_page_returns_the_items_and_the_cursor(self):
        with patch("starkcore.utils.rest.get", return_value=FakeResponse({"cursor": "next-page", "messages": _messages})) as get:
            messages, cursor = starkinfra.aimessage.page(chat_id="5632499082330112", limit=2, cursor="current-page")
        self.assertEqual(2, len(messages))
        self.assertEqual("next-page", cursor)
        self.assertEqual({"chatId": "5632499082330112", "limit": "2", "cursor": "current-page"}, queryOf(get.call_args.kwargs["url"]))

    def test_page_without_chat_id_does_not_send_it(self):
        with patch("starkcore.utils.rest.get", return_value=FakeResponse({"cursor": None, "messages": _messages})) as get:
            _, cursor = starkinfra.aimessage.page()
        self.assertIsNone(cursor)
        self.assertEqual({}, queryOf(get.call_args.kwargs["url"]))


if __name__ == '__main__':
    main()
