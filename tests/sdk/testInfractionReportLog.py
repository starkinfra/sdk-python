import starkinfra
from unittest import TestCase, main
from datetime import timedelta, date
from tests.utils.user import exampleProject


starkinfra.user = exampleProject


class TestInfractionReportLogQuery(TestCase):

    def test_success(self):
        logs = list(starkinfra.infractionreport.log.query(limit=10))
        logs = list(starkinfra.infractionreport.log.query(
            limit=10,
            report_ids={log.report.id for log in logs},
            types={log.type for log in logs}
        ))
        self.assertEqual(10, len(logs))
        print("Number of logs:", len(logs))

    def test_success_with_params(self):
        infraction_reports = starkinfra.infractionreport.log.query(
            limit=10,
            after=date.today() - timedelta(days=100),
            before=date.today(),
            types="failed",
            report_ids=["1"],
            ids=["1", "2", "3"],

        )
        self.assertEqual(len(list(infraction_reports)), 0)


class TestInfractionReportLogPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            logs, cursor = starkinfra.infractionreport.log.page(limit=2, cursor=cursor)
            for log in logs:
                print(log)
                self.assertFalse(log.id in ids)
                ids.append(log.id)
            if cursor is None:
                break
        self.assertTrue(len(ids) == 4)

    def test_success_with_params(self):
        infraction_reports = starkinfra.infractionreport.log.page(
            limit=10,
            after=date.today() - timedelta(days=100),
            before=date.today(),
            types="failed",
            report_ids=["1"],
            ids=["1", "2", "3"],

        )
        self.assertEqual(len(list(infraction_reports)), 0)


class TestInfractionReportLogInfoGet(TestCase):
    def test_success(self):
        logs = starkinfra.infractionreport.log.query()
        log_id = next(logs).id
        log = starkinfra.infractionreport.log.get(id=log_id)
        self.assertEqual(log_id, log.id)


if __name__ == '__main__':
    main()
