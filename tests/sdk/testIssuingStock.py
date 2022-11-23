import starkinfra
from unittest import TestCase, main
from datetime import date, timedelta
from tests.utils.user import exampleProject

starkinfra.user = exampleProject


class TestIssuingStockQuery(TestCase):

    def test_success(self):
        stocks = starkinfra.issuingstock.query(
            after=date.today() - timedelta(days=100),
            before=date.today(),
        )
        for stock in stocks:
            self.assertEqual(stock.id, str(stock.id))


class TestIssuingStockPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            stocks, cursor = starkinfra.issuingstock.page(
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


class TestIssuingStockGet(TestCase):

    def test_success(self):
        stocks = starkinfra.issuingstock.query(limit=1)
        stock = starkinfra.issuingstock.get(id=next(stocks).id)
        self.assertEqual(stock.id, str(stock.id))


if __name__ == '__main__':
    main()
