import starkinfra
from datetime import datetime
from unittest import TestCase, main
from tests.utils.user import exampleProject
from tests.utils.aiKnowledgeBase import generateExampleAiKnowledgeBase


starkinfra.user = exampleProject


class TestAiKnowledgeBase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.knowledgeBase = starkinfra.aiknowledgebase.create(generateExampleAiKnowledgeBase())

    @classmethod
    def tearDownClass(cls):
        starkinfra.aiknowledgebase.delete(ids=[cls.knowledgeBase.id])

    def test_create_returns_processing_knowledge_base(self):
        self.assertIsNotNone(self.knowledgeBase.id)
        self.assertEqual("processing", self.knowledgeBase.status)
        self.assertEqual("https://docs.starkinfra.com", self.knowledgeBase.root_url)
        self.assertIs(False, self.knowledgeBase.is_recursive)
        self.assertEqual(["sdk-python", "test"], self.knowledgeBase.tags)
        self.assertIsInstance(self.knowledgeBase.created, datetime)
        self.assertIsInstance(self.knowledgeBase.updated, datetime)

    def test_get(self):
        fetched = starkinfra.aiknowledgebase.get(self.knowledgeBase.id)
        self.assertEqual(self.knowledgeBase.id, fetched.id)
        self.assertEqual(self.knowledgeBase.name, fetched.name)

    def test_query_filters_by_ids(self):
        found = list(starkinfra.aiknowledgebase.query(ids=[self.knowledgeBase.id]))
        self.assertEqual([self.knowledgeBase.id], [entity.id for entity in found])

    def test_query_filters_by_name_and_status(self):
        current = starkinfra.aiknowledgebase.get(self.knowledgeBase.id)
        found = list(starkinfra.aiknowledgebase.query(name=current.name, status=current.status))
        self.assertIn(self.knowledgeBase.id, [entity.id for entity in found])

    def test_query_with_limit_stops_at_the_limit(self):
        self.assertEqual(1, len(list(starkinfra.aiknowledgebase.query(limit=1))))

    def test_page_filters_by_ids_and_returns_a_cursor(self):
        found, cursor = starkinfra.aiknowledgebase.page(ids=[self.knowledgeBase.id], limit=1)
        self.assertEqual([self.knowledgeBase.id], [entity.id for entity in found])
        self.assertTrue(cursor is None or isinstance(cursor, str))

    def test_page_with_a_limit_above_the_maximum_raises_input_errors(self):
        with self.assertRaises(starkinfra.error.InputErrors):
            starkinfra.aiknowledgebase.page(limit=101)

    def test_query_without_match_is_empty(self):
        found = list(starkinfra.aiknowledgebase.query(name="no-knowledge-base-has-this-name"))
        self.assertEqual([], found)

    def test_update_changes_name_and_tags_only(self):
        try:
            updated = starkinfra.aiknowledgebase.update(self.knowledgeBase.id, name="renamed-by-sdk", tags=["renamed"])
            self.assertEqual("renamed-by-sdk", updated.name)
            self.assertEqual(["renamed"], updated.tags)
            self.assertEqual(self.knowledgeBase.root_url, updated.root_url)
        finally:
            starkinfra.aiknowledgebase.update(
                self.knowledgeBase.id,
                name=self.knowledgeBase.name,
                tags=self.knowledgeBase.tags,
            )


class TestAiKnowledgeBaseErrors(TestCase):

    def test_create_with_invalid_root_url_raises_input_errors(self):
        invalid = starkinfra.AiKnowledgeBase(name="invalid", root_url="not-a-url")
        with self.assertRaises(starkinfra.error.InputErrors):
            starkinfra.aiknowledgebase.create(invalid)

    def test_get_unknown_id_raises_input_errors(self):
        with self.assertRaises(starkinfra.error.InputErrors):
            starkinfra.aiknowledgebase.get("0000000000000000")


_knowledge_base = {
    "id": "6767676767676767",
    "name": "Public Documentation",
    "rootUrl": "https://docs.starkinfra.com",
    "isRecursive": True,
    "status": "success",
    "tags": ["support"],
    "created": "2022-01-01T00:00:00.000000+00:00",
    "updated": "2022-01-02T00:00:00.000000+00:00",
}


if __name__ == '__main__':
    main()
