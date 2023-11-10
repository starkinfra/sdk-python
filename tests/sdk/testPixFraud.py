import starkinfra
from time import sleep
from unittest import TestCase, main
from datetime import timedelta, date
from tests.utils.user import exampleProject
from tests.utils.pixFraud import generateExamplePixFraudsJson


starkinfra.user = exampleProject


class TestPixFraudPost(TestCase):

    def test_success(self):
        fraud = generateExamplePixFraudsJson()
        fraud = starkinfra.pixfraud.create(fraud)
        self.assertEqual(len(fraud), 1)


class TestPixFraudQuery(TestCase):

    def test_success(self):
        fraud = list(starkinfra.pixfraud.query(limit=3))
        assert len(fraud) == 3

    def test_success_with_params(self):
        fraud = starkinfra.pixfraud.query(
            limit=10,
            after=date.today() - timedelta(days=100),
            before=date.today(),
            status="created",
            ids=["1", "2"],
            type="mule"
        )
        self.assertEqual(len(list(fraud)), 0)


class TestPixFraudPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            frauds, cursor = starkinfra.pixfraud.page(limit=2, cursor=cursor)
            for fraud in frauds:
                print(fraud)
                self.assertFalse(fraud.id in ids)
                ids.append(fraud.id)
            if cursor is None:
                break
        self.assertTrue(len(ids) == 4)


class TestPixFraudInfoDelete(TestCase):

    def test_success(self):
        fraud_report = starkinfra.pixfraud.create(generateExamplePixFraudsJson())[0]
        sleep(5)
        deleted_fraud_report = starkinfra.pixfraud.cancel(fraud_report.id)
        query_fraud_report = starkinfra.pixfraud.get(fraud_report.id)
        self.assertIsNotNone(deleted_fraud_report.id)
        self.assertEqual(deleted_fraud_report.id, fraud_report.id)
        self.assertEqual(query_fraud_report.status, "canceled")


if __name__ == '__main__':
    main()
