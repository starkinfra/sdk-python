import starkinfra
from unittest import TestCase, main
from tests.utils.pixKeyHolmes import generateExamplePixKeyHolmesJson
from tests.utils.user import exampleProject

starkinfra.user = exampleProject


class TestPixKeyHolmesPost(TestCase):

    def test_success(self):
        holmes = generateExamplePixKeyHolmesJson(n=3)
        holmes = starkinfra.pixkeyholmes.create(holmes)
        for sherlock in holmes:
            self.assertIsNotNone(sherlock.id)


class TestPixKeyHolmesQuery(TestCase):

    def test_success(self):
        holmes = list(starkinfra.pixkeyholmes.query(limit=10))
        for sherlock in holmes:
            self.assertIsNotNone(sherlock.id)


class TestPixKeyHolmesPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            holmes, cursor = starkinfra.pixkeyholmes.page(limit=2, cursor=cursor)
            for sherlock in holmes:
                self.assertFalse(sherlock.id in ids)
                ids.append(sherlock.id)
            if cursor is None:
                break
        self.assertTrue(len(ids) == 4)


if __name__ == '__main__':
    main()
