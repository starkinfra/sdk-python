import starkinfra
from unittest import TestCase, main
from tests.utils.user import exampleProject

starkinfra.user = exampleProject


class TestIssuingTokenLogQuery(TestCase):

    def test_success(self):
        logs = starkinfra.issuingtoken.log.query(limit=5)
        for log in logs:
            self.assertEqual(log.id, str(log.id))


class TestIssuingTokenLogPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            logs, cursor = starkinfra.issuingtoken.log.page(limit=2, cursor=cursor)
            for log in logs:
                self.assertEqual(log.id, str(log.id))
            if cursor is None:
                break


class TestIssuingTokenLogGet(TestCase):

    def test_success(self):
        logs = starkinfra.issuingtoken.log.query(limit=1)
        for log in logs:
            log = starkinfra.issuingtoken.log.get(log.id)
            self.assertEqual(log.id, str(log.id))


if __name__ == '__main__':
    main()
