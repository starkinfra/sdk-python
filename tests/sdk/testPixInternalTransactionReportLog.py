import starkinfra
from unittest import TestCase, main
from tests.utils.user import exampleProject

starkinfra.user = exampleProject


class TestPixInternalTransactionReportLogQuery(TestCase):

    def test_success(self):
        logs = list(starkinfra.pixinternaltransactionreport.log.query(limit=10))
        for log in logs:
            self.assertIsNotNone(log.id)


class TestPixInternalTransactionReportLogPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            logs, cursor = starkinfra.pixinternaltransactionreport.log.page(limit=2, cursor=cursor)
            for log in logs:
                self.assertFalse(log.id in ids)
                ids.append(log.id)
            if cursor is None:
                break
        self.assertTrue(len(ids) == 4)


class TestPixInternalTransactionReportLogInfoGet(TestCase):

    def test_success(self):
        logs = starkinfra.pixinternaltransactionreport.log.query(limit=1)
        log_id = next(logs).id
        log = starkinfra.pixinternaltransactionreport.log.get(id=log_id)
        self.assertEqual(log.id, log_id)


if __name__ == '__main__':
    main()
