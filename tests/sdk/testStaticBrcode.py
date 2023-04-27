import starkinfra
from unittest import TestCase, main
from datetime import date, timedelta
from tests.utils.user import exampleProject
from tests.utils.staticBrcode import generateExampleStaticBrcodeJson

starkinfra.user = exampleProject


class TestStaticBrcodeQuery(TestCase):

    def test_success(self):
        static_brcodes = starkinfra.staticbrcode.query(
            after=date.today() - timedelta(days=100),
            before=date.today(),
            limit=2
        )
        for static_brcode in static_brcodes:
            print(static_brcode)
            self.assertEqual(static_brcode.uuid, str(static_brcode.uuid))


class TestStaticBrcodePage(TestCase):

    def test_success(self):
        cursor = None
        uuids = []
        for _ in range(2):
            brcodes, cursor = starkinfra.staticbrcode.page(limit=2, cursor=cursor)
            for brcode in brcodes:
                print(brcode)
                self.assertFalse(brcode.uuid in uuids)
                uuids.append(brcode.id)
            if cursor is None:
                break
        self.assertTrue(len(uuids) == 4)


class TestStaticBrcodeGet(TestCase):

    def test_success(self):
        static_brcodes = starkinfra.staticbrcode.query(limit=1)
        static_brcode = starkinfra.staticbrcode.get(uuid=next(static_brcodes).uuid)
        self.assertEqual(static_brcode.uuid, str(static_brcode.uuid))


class TestStaticBrcodePost(TestCase):

    def test_success(self):
        example_static_brcode = generateExampleStaticBrcodeJson()
        static_brcode = starkinfra.staticbrcode.create(
            brcodes=[example_static_brcode]
        )
        for brcode in static_brcode:
            self.assertIsNotNone(brcode.id)
            self.assertIsNotNone(brcode.cashier_bank_code)
            print(brcode)


if __name__ == '__main__':
    main()
