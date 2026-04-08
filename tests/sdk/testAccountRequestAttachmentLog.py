import starkinfra
from unittest import TestCase, main
from tests.utils.user import exampleProject

starkinfra.user = exampleProject


class TestAccountRequestAttachmentLogQuery(TestCase):

    def test_success(self):
        logs = starkinfra.accountrequestattachment.log.query(limit=10)
        for log in logs:
            self.assertEqual(log.id, str(log.id))


class TestAccountRequestAttachmentLogGet(TestCase):

    def test_success(self):
        logs = starkinfra.accountrequestattachment.log.query(limit=1)
        log = starkinfra.accountrequestattachment.log.get(id=next(logs).id)
        self.assertEqual(log.id, str(log.id))


if __name__ == '__main__':
    main()
