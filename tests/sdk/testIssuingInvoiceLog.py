import starkinfra
from unittest import TestCase, main
from tests.utils.user import exampleProject

starkinfra.user = exampleProject


class TestIssuingInvoiceLogQuery(TestCase):

    def test_success(self):
        logs = starkinfra.issuinginvoice.log.query(limit=10)
        for log in logs:
            self.assertEqual(log.id, str(log.id))


class TestIssuingInvoiceLogPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            cards, cursor = starkinfra.issuinginvoice.log.page(limit=2, cursor=cursor)
            for card in cards:
                self.assertFalse(card.id in ids)
                ids.append(card.id)
            if cursor is None:
                break


if __name__ == '__main__':
    main()
