import starkinfra
from unittest import TestCase, main
from tests.utils.user import exampleProject

starkinfra.user = exampleProject


class TestIssuingHolderLogQuery(TestCase):

    def test_success(self):
        logs = starkinfra.issuingholder.log.query(limit=10)
        for log in logs:
            self.assertEqual(log.id, str(log.id))


class TestIssuingHolderLogGet(TestCase):

    def test_success(self):
        logs = starkinfra.issuingholder.log.query(limit=1)
        log = starkinfra.issuingholder.log.get(id=next(logs).id)
        self.assertEqual(log.id, str(log.id))


if __name__ == '__main__':
    main()
