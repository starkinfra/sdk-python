import starkinfra
from unittest import TestCase, main
from tests.utils.user import exampleProject


starkinfra.user = exampleProject


class TestPixInfractionLogQuery(TestCase):

    def test_success(self):
        logs = list(starkinfra.pixinfraction.log.query(limit=10))
        logs = list(starkinfra.pixinfraction.log.query(
            limit=10,
            infraction_ids={log.infraction.id for log in logs},
            types={log.type for log in logs}
        ))
        self.assertEqual(10, len(logs))
        print("Number of logs:", len(logs))

    def test_success_with_params(self):
        infraction_reports = starkinfra.pixinfraction.log.query(
            limit=2,
        )
        self.assertEqual(len(list(infraction_reports)), 2)


class TestPixInfractionLogPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            logs, cursor = starkinfra.pixinfraction.log.page(limit=2, cursor=cursor)
            for log in logs:
                print(log)
                self.assertFalse(log.id in ids)
                ids.append(log.id)
            if cursor is None:
                break
        self.assertTrue(len(ids) == 4)

    def test_success_with_params(self):
        infraction_reports = starkinfra.pixinfraction.log.page(
            limit=2,
        )
        self.assertEqual(len(list(infraction_reports)), 2)


class TestPixInfractionLogInfoGet(TestCase):
    def test_success(self):
        logs = starkinfra.pixinfraction.log.query(limit=10)
        log_id = next(logs).id
        log = starkinfra.pixinfraction.log.get(id=log_id)
        self.assertEqual(log_id, log.id)


if __name__ == '__main__':
    main()
