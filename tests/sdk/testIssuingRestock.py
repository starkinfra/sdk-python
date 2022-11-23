import starkinfra
from unittest import TestCase, main
from datetime import date, timedelta
from tests.utils.user import exampleProject
from tests.utils.issuingRestock import generateExampleRestocksJson

starkinfra.user = exampleProject


class TestIssuingRestockQuery(TestCase):

    def test_success(self):
        restocks = starkinfra.issuingrestock.query(
            after=date.today() - timedelta(days=100),
            before=date.today(),
        )
        for restock in restocks:
            self.assertEqual(restock.id, str(restock.id))


class TestIssuingRestockPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            restocks, cursor = starkinfra.issuingrestock.page(
                limit=2,
                after=date.today() - timedelta(days=100),
                before=date.today(),
                cursor=cursor
            )
            for restock in restocks:
                self.assertFalse(restock.id in ids)
                ids.append(restock.id)
            if cursor is None:
                break


class TestIssuingRestockGet(TestCase):

    def test_success(self):
        restocks = starkinfra.issuingrestock.query(limit=1)
        restock = starkinfra.issuingrestock.get(id=next(restocks).id)
        self.assertEqual(restock.id, str(restock.id))


class TestIssuingRestockPost(TestCase):

    def test_success(self):
        example_restocks = generateExampleRestocksJson(n=5)
        restocks = starkinfra.issuingrestock.create(example_restocks)
        for restock in restocks:
            self.assertEqual(restock.id, str(restock.id))
            print(restock)


if __name__ == '__main__':
    main()
