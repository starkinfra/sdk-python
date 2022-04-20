import starkinfra
from unittest import TestCase, main
from tests.utils.pixStatement import generateExamplePixStatementJson
from tests.utils.user import exampleProject


starkinfra.user = exampleProject


class TestPixStatementPost(TestCase):
    def test_success(self):
        pix_statements = []
        for _ in range(5):
            pix_statement = generateExamplePixStatementJson()
            pix_statement = starkinfra.pixstatement.create(pix_statement)
            pix_statements.append(pix_statement)
        self.assertEqual(len(pix_statements), 5)
        for pix_statement in pix_statements:
            print(pix_statement.id)


class TestPixStatementQuery(TestCase):

    def test_success(self):
        pix_statements = list(starkinfra.pixstatement.query(limit=5))
        assert len(pix_statements) == 5

    def test_success_with_params(self):
        pix_statements = starkinfra.pixstatement.query(
            limit=10,
            ids=["1", "2", "3"],
        )
        self.assertEqual(len(list(pix_statements)), 0)


class TestPixStatementPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            pix_statements, cursor = starkinfra.pixstatement.page(limit=2, cursor=cursor)
            for pix_statement in pix_statements:
                print(pix_statement)
                self.assertFalse(pix_statement.id in ids)
                ids.append(pix_statement.id)
            if cursor is None:
                break
        self.assertTrue(len(ids) == 4)


class TestPixStatementInfoGet(TestCase):

    def test_success(self):
        pix_statements = starkinfra.pixstatement.query()
        pix_statement_id = next(pix_statements).id
        pix_statement = starkinfra.pixstatement.get(id=pix_statement_id)
        self.assertIsNotNone(pix_statement.id)
        self.assertEqual(pix_statement.id, pix_statement_id)
    
    def test_success_ids(self):
        pix_statements = starkinfra.pixstatement.query(limit=5)
        pix_statements_ids_expected = [t.id for t in pix_statements]
        pix_statements_ids_result = [t.id for t in starkinfra.pixstatement.query(ids=pix_statements_ids_expected)]
        pix_statements_ids_expected.sort()
        pix_statements_ids_result.sort()
        self.assertTrue(pix_statements_ids_result)
        self.assertEqual(pix_statements_ids_expected, pix_statements_ids_result)


if __name__ == '__main__':
    main()
