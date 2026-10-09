import starkinfra
from json import loads
from datetime import datetime
from unittest import TestCase, SkipTest, main
from unittest.mock import patch
from tests.utils.user import exampleProject
from tests.utils.aiFixtures import FakeResponse, queryOf


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


class TestAiSpeechAtTheHttpBoundary(TestCase):

    def test_create_sends_only_the_voice_and_the_text(self):
        with patch("starkcore.utils.rest.post", return_value=FakeResponse({"speech": _speech})) as post:
            created = starkinfra.aispeech.create(starkinfra.AiSpeech(voice_id="5632499082330112", text="Short test."))
        self.assertTrue(post.call_args.kwargs["url"].endswith("/v2/ai-speech"))
        self.assertEqual({"voiceId": "5632499082330112", "text": "Short test."}, loads(post.call_args.kwargs["data"]))
        self.assertEqual("5632499082330112", created.voice_id)
        self.assertEqual("SUQzBAAAAAAA", created.audio)

    def test_query_reads_the_speeches_key_and_sends_expand_and_limit(self):
        with patch("starkcore.utils.rest.get", return_value=FakeResponse({"cursor": None, "speeches": [_speech]})) as get:
            found = list(starkinfra.aispeech.query(expand=["voice_name"], limit=1))
        self.assertEqual(["5646488461901824"], [speech.id for speech in found])
        self.assertEqual({"expand": "voiceName", "limit": "1"}, queryOf(get.call_args.kwargs["url"]))

    def test_query_follows_the_cursor_until_it_runs_out(self):
        second = dict(_speech, id="5646488461901825")
        pages = [
            FakeResponse({"cursor": "next-page", "speeches": [_speech]}),
            FakeResponse({"cursor": None, "speeches": [second]}),
        ]
        with patch("starkcore.utils.rest.get", side_effect=pages) as get:
            found = list(starkinfra.aispeech.query())
        self.assertEqual(["5646488461901824", "5646488461901825"], [speech.id for speech in found])
        self.assertNotIn("cursor", queryOf(get.call_args_list[0].kwargs["url"]))
        self.assertEqual("next-page", queryOf(get.call_args_list[1].kwargs["url"])["cursor"])

    def test_query_with_a_limit_asks_for_the_rest_on_each_page_and_stops_at_the_limit(self):
        first = [dict(_speech, id=str(1000 + n)) for n in range(100)]
        second = [dict(_speech, id=str(2000 + n)) for n in range(50)]
        pages = [
            FakeResponse({"cursor": "second-page", "speeches": first}),
            FakeResponse({"cursor": "third-page", "speeches": second}),
        ]
        with patch("starkcore.utils.rest.get", side_effect=pages) as get:
            found = list(starkinfra.aispeech.query(limit=150))
        self.assertEqual(150, len(found))
        self.assertEqual(2, get.call_count)
        self.assertEqual("100", queryOf(get.call_args_list[0].kwargs["url"])["limit"])
        self.assertEqual("50", queryOf(get.call_args_list[1].kwargs["url"])["limit"])

    def test_query_with_a_limit_follows_empty_pages(self):
        pages = [
            FakeResponse({"cursor": "second-page", "speeches": []}),
            FakeResponse({"cursor": "third-page", "speeches": [_speech]}),
            FakeResponse({"cursor": None, "speeches": [dict(_speech, id="5646488461901825")]}),
        ]
        with patch("starkcore.utils.rest.get", side_effect=pages) as get:
            found = list(starkinfra.aispeech.query(limit=2))
        self.assertEqual(2, len(found))
        self.assertEqual(3, get.call_count)

    def test_page_returns_the_items_and_the_cursor(self):
        with patch("starkcore.utils.rest.get", return_value=FakeResponse({"cursor": "next-page", "speeches": [_speech]})) as get:
            speeches, cursor = starkinfra.aispeech.page(limit=1, cursor="current-page", expand=["voice_name"])
        self.assertEqual(["5646488461901824"], [speech.id for speech in speeches])
        self.assertEqual("next-page", cursor)
        self.assertEqual({"limit": "1", "cursor": "current-page", "expand": "voiceName"}, queryOf(get.call_args.kwargs["url"]))

    def test_page_returns_a_null_cursor_on_the_last_page(self):
        with patch("starkcore.utils.rest.get", return_value=FakeResponse({"cursor": None, "speeches": [_speech]})):
            _, cursor = starkinfra.aispeech.page()
        self.assertIsNone(cursor)


if __name__ == '__main__':
    main()
