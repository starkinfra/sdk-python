import starkinfra
from unittest import TestCase, main
from tests.utils.user import exampleProject

starkinfra.user = exampleProject


class TestIssuingCardLogQuery(TestCase):

    def test_success(self):
        logs = starkinfra.issuingcard.log.query()
        for log in logs:
            self.assertIsInstance(log.id, str)


class TestIssuingCardLogGet(TestCase):

    def test_success(self):
        logs = starkinfra.issuingcard.log.query(limit=1)
        log = starkinfra.issuingcard.log.get(id=next(logs).id)
        self.assertIsInstance(log.id, str)


if __name__ == '__main__':
    main()
