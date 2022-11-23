import starkinfra
from datetime import date, timedelta
from unittest import TestCase, main
from tests.utils.user import exampleProject

starkinfra.user = exampleProject


class TestIssuingRestockLogQuery(TestCase):

    def test_success(self):
        logs = starkinfra.issuingrestock.log.query(limit=10)
        for log in logs:
            self.assertEqual(log.id, str(log.id))


class TestIssuingRestockLogPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            restocks, cursor = starkinfra.issuingrestock.log.page(
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


class TestIssuingRestockLogGet(TestCase):

    def test_success(self):
        logs = starkinfra.issuingrestock.log.query(limit=1)
        log = starkinfra.issuingrestock.log.get(id=next(logs).id)
        self.assertEqual(log.id, str(log.id))


if __name__ == '__main__':
    main()
