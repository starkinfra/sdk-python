import starkinfra
from datetime import date, timedelta
from unittest import TestCase, main
from tests.utils.user import exampleProject
from starkinfra import IndividualAccountAttachment


starkinfra.user = exampleProject


class TestIndividualAccountAttachmentLogQuery(TestCase):

    def test_success(self):
        logs = list(starkinfra.individualaccountattachment.log.query(limit=10))
        for log in logs:
            self.assertIsNotNone(log.id)

    def test_success_with_params(self):
        logs = starkinfra.individualaccountattachment.log.query(
            limit=10,
            after=date.today() - timedelta(days=100),
            before=date.today(),
            types=["created", "deleted"],
            attachment_ids=["1", "2", "3"],
        )
        self.assertEqual(len(list(logs)), 0)


class TestIndividualAccountAttachmentLogPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            logs, cursor = starkinfra.individualaccountattachment.log.page(limit=2, cursor=cursor)
            for log in logs:
                self.assertFalse(log.id in ids)
                ids.append(log.id)
            if cursor is None:
                break
        self.assertTrue(len(ids) == 4)

    def test_success_attachment_ids_filter(self):
        logs, cursor = starkinfra.individualaccountattachment.log.page(
            limit=2,
            attachment_ids=["1", "2", "3"],
        )
        self.assertEqual(len(logs), 0)


class TestIndividualAccountAttachmentLogGet(TestCase):

    def test_success(self):
        logs = starkinfra.individualaccountattachment.log.query(limit=1)
        log_id = next(logs).id
        log = starkinfra.individualaccountattachment.log.get(id=log_id)
        self.assertEqual(log.id, log_id)
        self.assertIsInstance(log.attachment, IndividualAccountAttachment)
        self.assertIn(log.type, ["created", "success", "failed", "deleted"])


if __name__ == '__main__':
    main()
