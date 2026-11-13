import starkinfra
from datetime import datetime
from unittest import TestCase, SkipTest, main
from tests.utils.user import exampleProject
from tests.utils import aiFixtures


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


if __name__ == '__main__':
    main()
