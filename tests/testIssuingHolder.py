import starkinfra
import starkbank
from unittest import TestCase, main
from tests.utils.user import exampleProject
from tests.utils.holder import generateExampleHoldersJson

starkbank.user = exampleProject


class TestIssuingHolderQuery(TestCase):

    def test_success(self):
        holders = starkinfra.issuingholder.query(user=exampleProject)
        for holder in holders:
            self.assertIsInstance(holder.id, str)


class TestIssuingHolderPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            holders, cursor = starkinfra.issuingholder.page(limit=2, cursor=cursor)
            for holder in holders:
                self.assertFalse(holder.id in ids)
                ids.append(holder.id)
            if cursor is None:
                break


class TestIssuingHolderGet(TestCase):

    def test_success(self):
        holders = starkinfra.issuingholder.query(user=exampleProject, limit=1)
        holder = starkinfra.issuingholder.get(user=exampleProject, id=next(holders).id)
        self.assertIsInstance(holder.id, str)


class TestIssuingHolderPostAndDelete(TestCase):

    def test_success(self):
        holders = starkinfra.issuingholder.create(generateExampleHoldersJson(n=1))
        holder_id = holders[0].id
        holder = starkinfra.issuingholder.delete(id=holder_id)
        print(holder)


if __name__ == '__main__':
    main()
