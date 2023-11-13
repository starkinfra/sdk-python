import starkinfra
from unittest import TestCase, main
from datetime import timedelta, date
from tests.utils.user import exampleProject
from tests.utils.pixInfraction import generateExamplePixInfractionsJson, getPixInfractionToPatch


starkinfra.user = exampleProject


class TestPixInfractionPostAndDelete(TestCase):
    def test_success(self):
        infraction_reports = generateExamplePixInfractionsJson(n=2)
        infraction_reports = starkinfra.pixinfraction.create(infraction_reports)
        self.assertEqual(len(infraction_reports), 2)
        for infraction_report in infraction_reports:
            deleted_infraction_report = starkinfra.pixinfraction.cancel(infraction_report.id)
            self.assertEqual(deleted_infraction_report.status, "canceled")


class TestPixInfractionQuery(TestCase):

    def test_success(self):
        infraction_reports = list(starkinfra.pixinfraction.query(limit=3))
        assert len(infraction_reports) == 3

    def test_success_with_params(self):
        infraction_reports = starkinfra.pixinfraction.query(
            limit=10,
            after=date.today() - timedelta(days=100),
            before=date.today(),
            status="failed",
            ids=["1", "2"],
            type="reversal",
            flow="in",
            bacen_id="ccf9bd9c-e99d-999e-bab9-b999ca999f99"
        )
        self.assertEqual(len(list(infraction_reports)), 0)


class TestPixInfractionPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            infraction_reports, cursor = starkinfra.pixinfraction.page(limit=2, cursor=cursor, flow="out")
            for infraction_report in infraction_reports:
                print(infraction_report)
                self.assertFalse(infraction_report.id in ids)
                ids.append(infraction_report.id)
            if cursor is None:
                break
        self.assertTrue(len(ids) == 4)


class TestPixInfractionInfoGet(TestCase):

    def test_success(self):
        infraction_reports = starkinfra.pixinfraction.query()
        infraction_report_id = next(infraction_reports).id
        infraction_report = starkinfra.pixinfraction.get(id=infraction_report_id)
        self.assertIsNotNone(infraction_report.id)
        self.assertEqual(infraction_report.id, infraction_report_id)
        print(infraction_report)
    
    def test_success_ids(self):
        infraction_reports = starkinfra.pixinfraction.query(limit=5)
        infraction_reports_ids_expected = [t.id for t in infraction_reports]
        infraction_reports_ids_result = [t.id for t in starkinfra.pixinfraction.query(ids=infraction_reports_ids_expected)]
        infraction_reports_ids_expected.sort()
        infraction_reports_ids_result.sort()
        self.assertTrue(infraction_reports_ids_result)
        self.assertEqual(infraction_reports_ids_expected, infraction_reports_ids_result)


class TestPixInfractionInfoDelete(TestCase):

    def test_success(self):
        infraction_report = starkinfra.pixinfraction.create(generateExamplePixInfractionsJson())[0]
        deleted_infraction_report = starkinfra.pixinfraction.cancel(infraction_report.id)
        self.assertIsNotNone(deleted_infraction_report.id)
        self.assertEqual(deleted_infraction_report.id, infraction_report.id)
        self.assertEqual(deleted_infraction_report.status, "canceled")


class TestPixInfractionInfoPatch(TestCase):

    def test_success_cancel(self):
        infraction_report = getPixInfractionToPatch()
        self.assertIsNotNone(infraction_report.id)
        self.assertEqual(infraction_report.status, "delivered")
        print(infraction_report)
        updated_infraction_report = starkinfra.pixinfraction.update(
            id=infraction_report.id,
            fraud_type="scam",
            result="agreed",
        )
        self.assertEqual(updated_infraction_report.result, "agreed")


if __name__ == '__main__':
    main()
