from datetime import datetime

import starkinfra
from unittest import TestCase, main

from tests.utils.date import randomPastDatetime
from tests.utils.user import exampleProject


starkinfra.user = exampleProject


class TestCreditHolmesLogQuery(TestCase):

    def test_success(self):
        logs = list(starkinfra.creditholmes.log.query(limit=100))
        after = randomPastDatetime(days=10)
        before = datetime.today()
        logs = list(starkinfra.creditholmes.log.query(
            limit=100,
            after=after.date(),
            before=before.date(),
            # holmes_ids={log.holmes.id for log in logs},
            types={log.type for log in logs}
        ))
        print("Number of logs:", len(logs))


class TestCreditHolmesLogPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            logs, cursor = starkinfra.creditholmes.log.page(limit=2, cursor=cursor)
            for log in logs:
                print(log)
                self.assertFalse(log.id in ids)
                ids.append(log.id)
            if cursor is None:
                break
        self.assertTrue(len(ids) == 4)


class TestCreditHolmesLogInfoGet(TestCase):
    def test_success(self):
        logs = starkinfra.creditholmes.log.query()
        log_id = next(logs).id
        log = starkinfra.creditholmes.log.get(id=log_id)
        self.assertEqual(log.id, log_id)


if __name__ == '__main__':
    main()
