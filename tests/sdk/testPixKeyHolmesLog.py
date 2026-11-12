import starkinfra
from unittest import TestCase, main

from tests.utils.user import exampleProject


starkinfra.user = exampleProject


class TestPixKeyHolmesLogQuery(TestCase):

    def test_success(self):
        logs = list(starkinfra.pixkeyholmes.log.query(limit=10))
        self.assertTrue(len(logs) > 0)
        for log in logs:
            self.assertIsNotNone(log.id)
            self.assertIsNotNone(log.type)
            self.assertIsNotNone(log.holmes.id)


class TestPixKeyHolmesLogPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            logs, cursor = starkinfra.pixkeyholmes.log.page(limit=2, cursor=cursor)
            for log in logs:
                self.assertFalse(log.id in ids)
                ids.append(log.id)
            if cursor is None:
                break
        self.assertTrue(len(ids) == 4)


class TestPixKeyHolmesLogGet(TestCase):

    def test_success(self):
        log_id = next(starkinfra.pixkeyholmes.log.query(limit=1)).id
        log = starkinfra.pixkeyholmes.log.get(id=log_id)
        self.assertEqual(log.id, log_id)
        self.assertIsNotNone(log.holmes.id)


if __name__ == '__main__':
    main()
