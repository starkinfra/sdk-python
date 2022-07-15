import starkinfra
from unittest import TestCase, main
from datetime import date, timedelta
from tests.utils.user import exampleProject
from tests.utils.holder import generateExampleHoldersJson

starkinfra.user = exampleProject


class TestIssuingHolderQuery(TestCase):

    def test_success(self):
        holders = starkinfra.issuingholder.query(
            limit=10,
            expand=["rules"],
            after=date.today() - timedelta(days=100),
            before=date.today(),
        )
        for holder in holders:
            self.assertEqual(holder.id, str(holder.id))


class TestIssuingHolderPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            holders, cursor = starkinfra.issuingholder.page(
                limit=2,
                after=date.today() - timedelta(days=100),
                before=date.today(),
                cursor=cursor
            )
            for holder in holders:
                self.assertFalse(holder.id in ids)
                ids.append(holder.id)
            if cursor is None:
                break


class TestIssuingHolderGet(TestCase):

    def test_success(self):
        holders = starkinfra.issuingholder.query(limit=1)
        holder = starkinfra.issuingholder.get(id=next(holders).id)
        self.assertEqual(holder.id, str(holder.id))


class TestIssuingHolderPostPatchAndDelete(TestCase):

    def test_success(self):
        holders = starkinfra.issuingholder.create(generateExampleHoldersJson(n=1), expand=["rules"])
        holder_id = holders[0].id
        holder = starkinfra.issuingholder.update(id=holder_id, name="Updated Name")
        self.assertEqual("Updated Name", holder.name)
        holder = starkinfra.issuingholder.cancel(id=holder_id)
        self.assertEqual("canceled", holder.status)


if __name__ == '__main__':
    main()
