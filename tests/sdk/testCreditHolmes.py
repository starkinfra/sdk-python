from datetime import datetime
from unittest import TestCase, main
import starkinfra
from tests.utils.creditHolmes import generateExampleCreditHolmesJson
from tests.utils.date import randomPastDatetime
from tests.utils.user import exampleProject

starkinfra.user = exampleProject


class TestCreditHolmesPost(TestCase):

    def test_success(self):
        holmes = generateExampleCreditHolmesJson(n=3)
        holmes = starkinfra.creditholmes.create(holmes)
        for holmes in holmes:
            self.assertIsNotNone(holmes.id)


class TestCreditHolmesQuery(TestCase):

    def test_success(self):
        after = randomPastDatetime(days=10)
        before = datetime.today()
        holmes = list(starkinfra.creditholmes.query(
            tags=["test"],
            after=after.date(),
            before=before.date(),
            limit=1,
        ))
        for holmes in holmes:
            print(holmes)
        print("Number of credit holmes:", len(holmes))


class TestCreditHolmesPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            holmes, cursor = starkinfra.creditholmes.page(limit=2, cursor=cursor)
            for holmes in holmes:
                print(holmes)
                self.assertFalse(holmes.id in ids)
                ids.append(holmes.id)
            if cursor is None:
                break
        self.assertTrue(len(ids) == 4)


class TestCreditHolmesInfoGet(TestCase):

    def test_success(self):
        holmes = starkinfra.creditholmes.query(limit=10)
        for holmes in holmes:
            holmes_id = holmes.id
            holmes = starkinfra.creditholmes.get(holmes_id)
            self.assertEqual(holmes.id, holmes_id)


if __name__ == '__main__':
    main()
