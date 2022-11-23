import starkinfra
from datetime import timedelta, date
from unittest import TestCase, main
from tests.utils.user import exampleProject

starkinfra.user = exampleProject


class TestIssuingStockLogQuery(TestCase):

    def test_success(self):
        logs = starkinfra.issuingstock.log.query(limit=10)
        for log in logs:
            self.assertEqual(log.id, str(log.id))


class TestIssuingStockLogPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            stocks, cursor = starkinfra.issuingstock.log.page(
                limit=2,
                after=date.today() - timedelta(days=100),
                before=date.today(),
                cursor=cursor
            )
            for stock in stocks:
                self.assertFalse(stock.id in ids)
                ids.append(stock.id)
            if cursor is None:
                break


class TestIssuingStockLogGet(TestCase):

    def test_success(self):
        logs = starkinfra.issuingstock.log.query(limit=1)
        log = starkinfra.issuingstock.log.get(id=next(logs).id)
        self.assertEqual(log.id, str(log.id))


if __name__ == '__main__':
    main()
