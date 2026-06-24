import starkinfra
from unittest import TestCase, main
from tests.utils.user import exampleProject

starkinfra.user = exampleProject


class TestBusinessAttachmentLogQuery(TestCase):

    def test_success(self):
        logs = starkinfra.businessattachment.log.query(limit=10)
        for log in logs:
            self.assertEqual(log.id, str(log.id))


class TestBusinessAttachmentLogGet(TestCase):

    def test_success(self):
        logs = starkinfra.businessattachment.log.query(limit=1)
        log = starkinfra.businessattachment.log.get(id=next(logs).id)
        self.assertEqual(log.id, str(log.id))


if __name__ == '__main__':
    main()
