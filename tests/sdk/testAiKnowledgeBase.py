import starkinfra
from json import loads
from datetime import datetime
from unittest import TestCase, main
from unittest.mock import patch
from tests.utils.user import exampleProject
from tests.utils.aiFixtures import FakeResponse, queryOf
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


class TestAiKnowledgeBaseAtTheHttpBoundary(TestCase):

    def test_hosts_groups_pages_by_host_with_snake_case_keys(self):
        body = {"hosts": {"docs.starkinfra.com": [{
            "originalUrl": "https://docs.starkinfra.com/get-started",
            "status": "success",
            "storageUrl": "https://storage.googleapis.com/ai-knowledge/6767676767676767/get-started.md",
        }]}}
        with patch("starkcore.utils.rest.get", return_value=FakeResponse(body)) as get:
            hosts = starkinfra.aiknowledgebase.hosts("6767676767676767")
        self.assertTrue(get.call_args.kwargs["url"].endswith("/v2/ai-knowledge-base/6767676767676767/hosts"))
        self.assertEqual({"docs.starkinfra.com": [{
            "original_url": "https://docs.starkinfra.com/get-started",
            "status": "success",
            "storage_url": "https://storage.googleapis.com/ai-knowledge/6767676767676767/get-started.md",
        }]}, hosts)

    def test_create_sends_the_attributes_that_are_set(self):
        body = {"knowledgeBase": {
            "id": "6767676767676767",
            "name": "Public Documentation",
            "rootUrl": "https://docs.starkinfra.com",
            "isRecursive": False,
            "status": "processing",
            "tags": [],
            "created": "2022-01-01T00:00:00.000000+00:00",
            "updated": "2022-01-01T00:00:00.000000+00:00",
        }}
        returned = starkinfra.AiKnowledgeBase(
            name="Public Documentation",
            root_url="https://docs.starkinfra.com",
            is_recursive=False,
            tags=[],
        )
        with patch("starkcore.utils.rest.post", return_value=FakeResponse(body)) as post:
            starkinfra.aiknowledgebase.create(returned)
        self.assertEqual({
            "name": "Public Documentation",
            "rootUrl": "https://docs.starkinfra.com",
            "isRecursive": False,
            "tags": [],
        }, loads(post.call_args.kwargs["data"]))

    def test_delete_sends_ids_in_the_query_string_and_returns_the_deleted_objects(self):
        body = {"knowledgeBases": [{
            "id": "6767676767676767",
            "name": "Public Documentation",
            "rootUrl": "https://docs.starkinfra.com",
            "isRecursive": True,
            "status": "success",
            "tags": ["support"],
            "created": "2022-01-01T00:00:00.000000+00:00",
            "updated": "2022-01-02T00:00:00.000000+00:00",
        }]}
        with patch("starkcore.utils.rest.delete", return_value=FakeResponse(body)) as delete:
            deleted = starkinfra.aiknowledgebase.delete(ids=["6767676767676767", "6767676767676768"])
        url = delete.call_args.kwargs["url"]
        self.assertTrue(url.endswith("/v2/ai-knowledge-base?ids=6767676767676767%2C6767676767676768"), url)
        self.assertEqual("", delete.call_args.kwargs["data"])
        self.assertEqual(["6767676767676767"], [entity.id for entity in deleted])
        self.assertEqual("Public Documentation", deleted[0].name)

    def test_page_returns_the_items_and_the_cursor_with_the_filters(self):
        body = {"cursor": "next-page", "knowledgeBases": [_knowledge_base]}
        with patch("starkcore.utils.rest.get", return_value=FakeResponse(body)) as get:
            found, cursor = starkinfra.aiknowledgebase.page(
                limit=1, cursor="current-page", ids=["6767676767676767", "6767676767676768"], name="Docs", status="success",
            )
        self.assertEqual(["6767676767676767"], [entity.id for entity in found])
        self.assertEqual("next-page", cursor)
        self.assertEqual({
            "limit": "1", "cursor": "current-page", "ids": "6767676767676767,6767676767676768", "name": "Docs",
            "status": "success",
        }, queryOf(get.call_args.kwargs["url"]))

    def test_query_with_a_limit_asks_for_the_rest_on_each_page_and_stops_at_the_limit(self):
        first = [dict(_knowledge_base, id=str(1000 + n)) for n in range(100)]
        second = [dict(_knowledge_base, id=str(2000 + n)) for n in range(50)]
        pages = [
            FakeResponse({"cursor": "second-page", "knowledgeBases": first}),
            FakeResponse({"cursor": "third-page", "knowledgeBases": second}),
        ]
        with patch("starkcore.utils.rest.get", side_effect=pages) as get:
            found = list(starkinfra.aiknowledgebase.query(limit=150))
        self.assertEqual(150, len(found))
        self.assertEqual(2, get.call_count)
        self.assertEqual("100", queryOf(get.call_args_list[0].kwargs["url"])["limit"])
        self.assertEqual("50", queryOf(get.call_args_list[1].kwargs["url"])["limit"])

    def test_query_with_a_limit_follows_empty_pages(self):
        pages = [
            FakeResponse({"cursor": "second-page", "knowledgeBases": []}),
            FakeResponse({"cursor": "third-page", "knowledgeBases": [_knowledge_base]}),
            FakeResponse({"cursor": None, "knowledgeBases": [dict(_knowledge_base, id="6767676767676768")]}),
        ]
        with patch("starkcore.utils.rest.get", side_effect=pages) as get:
            found = list(starkinfra.aiknowledgebase.query(limit=2))
        self.assertEqual(2, len(found))
        self.assertEqual(3, get.call_count)

    def test_update_sends_only_the_given_fields(self):
        with patch("starkcore.utils.rest.patch", return_value=FakeResponse({"knowledgeBase": _knowledge_base})) as patch_request:
            starkinfra.aiknowledgebase.update("6767676767676767", name="Renamed", tags=[])
        self.assertEqual({"name": "Renamed", "tags": []}, loads(patch_request.call_args.kwargs["data"]))

    def test_page_returns_a_null_cursor_on_the_last_page(self):
        with patch("starkcore.utils.rest.get", return_value=FakeResponse({"cursor": None, "knowledgeBases": [_knowledge_base]})):
            _, cursor = starkinfra.aiknowledgebase.page()
        self.assertIsNone(cursor)

    def test_query_follows_the_cursor_through_empty_pages_until_it_runs_out(self):
        second = dict(_knowledge_base, id="6767676767676768")
        pages = [
            FakeResponse({"cursor": "second-page", "knowledgeBases": []}),
            FakeResponse({"cursor": "third-page", "knowledgeBases": [_knowledge_base]}),
            FakeResponse({"cursor": None, "knowledgeBases": [second]}),
        ]
        with patch("starkcore.utils.rest.get", side_effect=pages) as get:
            found = list(starkinfra.aiknowledgebase.query(name="Docs"))
        self.assertEqual(["6767676767676767", "6767676767676768"], [entity.id for entity in found])
        self.assertEqual(3, get.call_count)
        self.assertEqual("third-page", queryOf(get.call_args_list[2].kwargs["url"])["cursor"])
        self.assertEqual("Docs", queryOf(get.call_args_list[2].kwargs["url"])["name"])


if __name__ == '__main__':
    main()
