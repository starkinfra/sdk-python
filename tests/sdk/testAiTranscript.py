import starkinfra
from json import loads
from datetime import datetime
from unittest import TestCase, SkipTest, main
from unittest.mock import patch
from tests.utils.user import exampleProject
from tests.utils import aiFixtures
from tests.utils.aiFixtures import FakeResponse, queryOf


starkinfra.user = exampleProject

_transcript = {
    "id": "5147403464212480",
    "text": "This is a short recording used to test the transcription service.",
    "status": "success",
    "errors": [],
    "created": "2026-10-01T14:28:04.482326+00:00",
    "updated": "2026-10-01T14:28:05.752389+00:00",
}


class TestAiTranscript(TestCase):

    @classmethod
    def setUpClass(cls):
        audio = aiFixtures.speechAudio()
        if audio is None:
            raise SkipTest("the workspace has no finished speech to take an audio from")
        cls.transcript = starkinfra.aitranscript.create(starkinfra.AiTranscript(audio=audio))

    def test_create_returns_the_text(self):
        self.assertIsNotNone(self.transcript.id)
        self.assertEqual("success", self.transcript.status)
        self.assertIsInstance(self.transcript.text, str)
        self.assertIsInstance(self.transcript.created, datetime)

    def test_query_lists_the_created_transcript(self):
        self.assertIn(self.transcript.id, [entity.id for entity in starkinfra.aitranscript.query()])

    def test_query_with_limit_stops_at_the_limit(self):
        self.assertEqual(1, len(list(starkinfra.aitranscript.query(limit=1))))

    def test_page_returns_the_transcripts_and_a_cursor(self):
        transcripts, cursor = starkinfra.aitranscript.page(limit=1)
        self.assertEqual(1, len(transcripts))
        self.assertTrue(cursor is None or isinstance(cursor, str))

    def test_page_with_a_limit_above_the_maximum_raises_input_errors(self):
        with self.assertRaises(starkinfra.error.InputErrors):
            starkinfra.aitranscript.page(limit=101)


class TestAiTranscriptAtTheHttpBoundary(TestCase):

    def test_create_sends_only_the_audio(self):
        with patch("starkcore.utils.rest.post", return_value=FakeResponse({"transcript": _transcript})) as post:
            created = starkinfra.aitranscript.create(starkinfra.AiTranscript(audio="UklGRg=="))
        self.assertTrue(post.call_args.kwargs["url"].endswith("/v2/ai-transcript"))
        self.assertEqual({"audio": "UklGRg=="}, loads(post.call_args.kwargs["data"]))
        self.assertEqual("success", created.status)
        self.assertTrue(created.text.startswith("This is a short recording"))

    def test_page_returns_the_items_and_the_cursor(self):
        with patch("starkcore.utils.rest.get", return_value=FakeResponse({"cursor": "next-page", "transcripts": [_transcript]})) as get:
            transcripts, cursor = starkinfra.aitranscript.page(limit=1, cursor="current-page")
        self.assertEqual(["5147403464212480"], [transcript.id for transcript in transcripts])
        self.assertEqual("next-page", cursor)
        self.assertEqual({"limit": "1", "cursor": "current-page"}, queryOf(get.call_args.kwargs["url"]))

    def test_page_returns_a_null_cursor_on_the_last_page(self):
        with patch("starkcore.utils.rest.get", return_value=FakeResponse({"cursor": None, "transcripts": [_transcript]})):
            _, cursor = starkinfra.aitranscript.page()
        self.assertIsNone(cursor)


if __name__ == '__main__':
    main()
