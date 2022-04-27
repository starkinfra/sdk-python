import starkinfra
from unittest import TestCase, main
from datetime import timedelta, date
from tests.utils.user import exampleProject
from tests.utils.infractionReport import generateExampleInfractionReportJson, getInfractionReportToPatch


starkinfra.user = exampleProject


class TestInfractionReportPostAndDelete(TestCase):
    def test_success(self):
        infraction_reports = []
        for _ in range(2):
            infraction_report = generateExampleInfractionReportJson()
            infraction_report = starkinfra.infractionreport.create(infraction_report)
            print(infraction_report)
            infraction_reports.append(infraction_report)
        self.assertEqual(len(infraction_reports), 2)
        for infraction_report in infraction_reports:
            deleted_infraction_report = starkinfra.infractionreport.delete(infraction_report.id)
            self.assertEqual(deleted_infraction_report.status, "canceled")
            print(infraction_report.id)


class TestInfractionReportQuery(TestCase):

    def test_success(self):
        infraction_reports = list(starkinfra.infractionreport.query(limit=3))
        assert len(infraction_reports) == 3

    def test_success_with_params(self):
        infraction_reports = starkinfra.infractionreport.query(
            limit=10,
            after=date.today() - timedelta(days=100),
            before=date.today(),
            status="failed",
            ids=["1", "2"],
            type="fraud",
        )
        self.assertEqual(len(list(infraction_reports)), 0)


class TestInfractionReportPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            infraction_reports, cursor = starkinfra.infractionreport.page(limit=2, cursor=cursor)
            for infraction_report in infraction_reports:
                print(infraction_report)
                self.assertFalse(infraction_report.id in ids)
                ids.append(infraction_report.id)
            if cursor is None:
                break
        self.assertTrue(len(ids) == 4)


class TestInfractionReportInfoGet(TestCase):

    def test_success(self):
        infraction_reports = starkinfra.infractionreport.query()
        infraction_report_id = next(infraction_reports).id
        infraction_report = starkinfra.infractionreport.get(id=infraction_report_id)
        self.assertIsNotNone(infraction_report.id)
        self.assertEqual(infraction_report.id, infraction_report_id)
        print(infraction_report)
    
    def test_success_ids(self):
        infraction_reports = starkinfra.infractionreport.query(limit=5)
        infraction_reports_ids_expected = [t.id for t in infraction_reports]
        infraction_reports_ids_result = [t.id for t in starkinfra.infractionreport.query(ids=infraction_reports_ids_expected)]
        infraction_reports_ids_expected.sort()
        infraction_reports_ids_result.sort()
        self.assertTrue(infraction_reports_ids_result)
        self.assertEqual(infraction_reports_ids_expected, infraction_reports_ids_result)


class TestInfractionReportInfoDelete(TestCase):

    def test_success(self):
        infraction_report = starkinfra.infractionreport.create(generateExampleInfractionReportJson())
        deleted_infraction_report = starkinfra.infractionreport.delete(infraction_report.id)
        self.assertIsNotNone(deleted_infraction_report.id)
        self.assertEqual(deleted_infraction_report.id, infraction_report.id)
        self.assertEqual(deleted_infraction_report.status, "canceled")


class TestInfractionReportInfoPatch(TestCase):

    def test_success_cancel(self):
        infraction_report = getInfractionReportToPatch()
        self.assertIsNotNone(infraction_report.id)
        self.assertEqual(infraction_report.status, "created")
        print(infraction_report)
        updated_infraction_report = starkinfra.infractionreport.update(
            id=infraction_report.id,
            result="agreed",
        )
        self.assertEqual(updated_infraction_report.result, "agreed")


if __name__ == '__main__':
    main()
