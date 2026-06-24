import starkinfra
from unittest import TestCase, main
from tests.utils.pixInternalTransactionReport import generateExamplePixInternalTransactionReportJson
from tests.utils.user import exampleProject

starkinfra.user = exampleProject


class TestPixInternalTransactionReportPost(TestCase):

    def test_success(self):
        reports = generateExamplePixInternalTransactionReportJson(n=3)
        reports = starkinfra.pixinternaltransactionreport.create(reports)
        for report in reports:
            self.assertIsNotNone(report.id)


class TestPixInternalTransactionReportQuery(TestCase):

    def test_success(self):
        reports = list(starkinfra.pixinternaltransactionreport.query(limit=10))
        for report in reports:
            self.assertIsNotNone(report.id)


class TestPixInternalTransactionReportPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            reports, cursor = starkinfra.pixinternaltransactionreport.page(limit=2, cursor=cursor)
            for report in reports:
                self.assertFalse(report.id in ids)
                ids.append(report.id)
            if cursor is None:
                break
        self.assertTrue(len(ids) == 4)


class TestPixInternalTransactionReportGet(TestCase):

    def test_success(self):
        reports = starkinfra.pixinternaltransactionreport.query(limit=10)
        for report in reports:
            report_id = report.id
            report = starkinfra.pixinternaltransactionreport.get(report_id)
            self.assertEqual(report.id, report_id)


if __name__ == '__main__':
    main()
