import starkinfra
import starkbank
from unittest import TestCase, main
from tests.utils.user import exampleProject

starkbank.user = exampleProject


class TestIssuingHolderLogQuery(TestCase):

    def test_success(self):
        logs = starkinfra.issuingholder.log.query(user=exampleProject)
        for log in logs:
            self.assertIsInstance(log.id, str)


class TestIssuingHolderLogGet(TestCase):

    def test_success(self):
        logs = starkinfra.issuingholder.log.query(user=exampleProject, limit=1)
        log = starkinfra.issuingholder.log.get(user=exampleProject, id=next(logs).id)
        self.assertIsInstance(log.id, str)


if __name__ == '__main__':
    main()
