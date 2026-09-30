import starkinfra
from json import loads
from datetime import datetime
from unittest import TestCase, SkipTest, main
from unittest.mock import patch
from tests.utils.user import exampleProject
from tests.utils import aiFixtures
from tests.utils.aiFixtures import FakeResponse, queryOf


starkinfra.user = exampleProject

_voice = {
    "id": "5631671361601536",
    "name": "Helena",
    "description": "Calm voice",
    "language": "portuguese",
    "gender": "female",
    "status": "processing",
    "errors": [],
    "created": "2026-10-01T14:28:24.566332+00:00",
    "updated": "2026-10-01T14:28:24.566342+00:00",
}


class TestAiVoice(TestCase):

    @classmethod
    def setUpClass(cls):
        audio = aiFixtures.speechAudio()
        if audio is None:
            raise SkipTest("the workspace has no finished speech to take an audio from")
        cls.audio = audio
        cls.voice = starkinfra.aivoice.create(starkinfra.AiVoice(audio=audio, name="sdk-python test"))

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "voice"):
            starkinfra.aivoice.delete([cls.voice.id])

    def test_create_returns_a_processing_voice(self):
        self.assertIsNotNone(self.voice.id)
        self.assertEqual("processing", self.voice.status)
        self.assertEqual("sdk-python test", self.voice.name)
        self.assertIsInstance(self.voice.created, datetime)
        self.assertIsNone(self.voice.audio)

    def test_query_lists_the_created_voice_without_the_audio(self):
        listed = {voice.id: voice for voice in starkinfra.aivoice.query()}
        self.assertIn(self.voice.id, listed)
        self.assertIsNone(listed[self.voice.id].audio)
        self.assertIsInstance(listed[self.voice.id].errors, list)

    def test_query_with_limit_stops_at_the_limit(self):
        self.assertEqual(1, len(list(starkinfra.aivoice.query(limit=1))))

    def test_page_returns_the_voices_and_a_cursor(self):
        voices, cursor = starkinfra.aivoice.page(limit=1)
        self.assertEqual(1, len(voices))
        self.assertTrue(cursor is None or isinstance(cursor, str))

    def test_page_with_a_limit_above_the_maximum_raises_input_errors(self):
        with self.assertRaises(starkinfra.error.InputErrors):
            starkinfra.aivoice.page(limit=101)

    def test_delete_returns_the_deleted_voice(self):
        extra = starkinfra.aivoice.create(starkinfra.AiVoice(audio=self.audio, name="sdk-python delete test"))
        deleted = starkinfra.aivoice.delete([extra.id])
        self.assertEqual([extra.id], [voice.id for voice in deleted])


class TestAiVoiceAtTheHttpBoundary(TestCase):

    def test_create_sends_the_attributes_that_are_set(self):
        voice = starkinfra.AiVoice(audio="UklGRg==", name="Helena", description="Calm voice", language="portuguese", gender="female")
        with patch("starkcore.utils.rest.post", return_value=FakeResponse({"voice": _voice})) as post:
            created = starkinfra.aivoice.create(voice)
        self.assertTrue(post.call_args.kwargs["url"].endswith("/v2/ai-voice"))
        self.assertEqual(
            {"audio": "UklGRg==", "name": "Helena", "description": "Calm voice", "language": "portuguese", "gender": "female"},
            loads(post.call_args.kwargs["data"]),
        )
        self.assertEqual("5631671361601536", created.id)
        self.assertEqual("processing", created.status)
        self.assertIsInstance(created.created, datetime)

    def test_create_omits_the_optional_fields_it_was_not_given(self):
        with patch("starkcore.utils.rest.post", return_value=FakeResponse({"voice": _voice})) as post:
            starkinfra.aivoice.create(starkinfra.AiVoice(audio="UklGRg=="))
        self.assertEqual({"audio": "UklGRg=="}, loads(post.call_args.kwargs["data"]))

    def test_delete_sends_ids_in_the_query_string_and_returns_the_deleted_objects(self):
        with patch("starkcore.utils.rest.delete", return_value=FakeResponse({"voices": [_voice]})) as delete:
            deleted = starkinfra.aivoice.delete(ids=["5631671361601536", "5631671361601537"])
        self.assertTrue(delete.call_args.kwargs["url"].endswith("/v2/ai-voice?ids=5631671361601536%2C5631671361601537"))
        self.assertEqual("", delete.call_args.kwargs["data"])
        self.assertEqual(["5631671361601536"], [voice.id for voice in deleted])

    def test_page_returns_the_items_and_the_cursor(self):
        with patch("starkcore.utils.rest.get", return_value=FakeResponse({"cursor": "next-page", "voices": [_voice]})) as get:
            voices, cursor = starkinfra.aivoice.page(limit=1, cursor="current-page")
        self.assertEqual(["5631671361601536"], [voice.id for voice in voices])
        self.assertEqual("next-page", cursor)
        self.assertEqual({"limit": "1", "cursor": "current-page"}, queryOf(get.call_args.kwargs["url"]))

    def test_page_returns_a_null_cursor_on_the_last_page(self):
        with patch("starkcore.utils.rest.get", return_value=FakeResponse({"cursor": None, "voices": [_voice]})):
            _, cursor = starkinfra.aivoice.page()
        self.assertIsNone(cursor)


if __name__ == '__main__':
    main()
