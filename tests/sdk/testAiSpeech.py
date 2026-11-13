import starkinfra
from datetime import datetime
from unittest import TestCase, SkipTest, main
from tests.utils.user import exampleProject


starkinfra.user = exampleProject

_speech = {
    "id": "5646488461901824",
    "voiceId": "5632499082330112",
    "text": "Short test.",
    "status": "success",
    "audio": "SUQzBAAAAAAA",
    "errors": [],
    "created": "2026-10-01T14:28:06.942491+00:00",
    "updated": "2026-10-01T14:28:07.605185+00:00",
}


class TestAiSpeech(TestCase):

    @classmethod
    def setUpClass(cls):
        ready = next((voice for voice in starkinfra.aivoice.query() if voice.status == "success"), None)
        if ready is None:
            raise SkipTest("the workspace has no ready voice to speak with")
        cls.speech = starkinfra.aispeech.create(starkinfra.AiSpeech(voice_id=ready.id, text="Short test."))

    def test_create_returns_the_synthesized_audio(self):
        self.assertIsNotNone(self.speech.id)
        self.assertEqual("success", self.speech.status)
        self.assertEqual("Short test.", self.speech.text)
        self.assertTrue(self.speech.audio)
        self.assertIsInstance(self.speech.created, datetime)

    def test_get_returns_the_audio(self):
        fetched = starkinfra.aispeech.get(self.speech.id)
        self.assertEqual(self.speech.id, fetched.id)
        self.assertTrue(fetched.audio)

    def test_get_and_expand_voice_name(self):
        self.assertTrue(starkinfra.aispeech.get(self.speech.id, expand=["voice_name"]).voice_name)

    def test_get_unknown_id_raises_input_errors(self):
        with self.assertRaises(starkinfra.error.InputErrors):
            starkinfra.aispeech.get("0000000000000000")

    def test_query_leaves_the_audio_out(self):
        for speech in starkinfra.aispeech.query():
            self.assertIsNotNone(speech.id)
            self.assertIsNone(speech.audio)
            self.assertIsInstance(speech.created, datetime)

    def test_query_with_limit_stops_at_the_limit(self):
        self.assertEqual(1, len(list(starkinfra.aispeech.query(limit=1))))

    def test_page_returns_the_speeches_and_a_cursor(self):
        speeches, cursor = starkinfra.aispeech.page(limit=1)
        self.assertEqual(1, len(speeches))
        self.assertTrue(cursor is None or isinstance(cursor, str))

    def test_page_with_a_limit_above_the_maximum_raises_input_errors(self):
        with self.assertRaises(starkinfra.error.InputErrors):
            starkinfra.aispeech.page(limit=101)


if __name__ == '__main__':
    main()
