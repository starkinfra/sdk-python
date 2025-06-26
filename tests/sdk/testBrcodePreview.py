import starkinfra
from unittest import TestCase, main
from tests.utils.user import exampleProject
from tests.utils.brcodePreview import create_brcode_preview_by_id
from tests.utils.dynamicBrcode import create_dynamic_brcode_by_type


starkinfra.user = exampleProject


class TestCreateBrcodePreview(TestCase):

    def test_query_and_create(self):
        static_brcodes = list(starkinfra.staticbrcode.query(limit=2))

        dynamic_brcodes = list(starkinfra.dynamicbrcode.query(limit=2))

        brcodes = static_brcodes + dynamic_brcodes

        previews = starkinfra.brcodepreview.create([
            starkinfra.BrcodePreview(
                id=brcodes[0].id,
                payer_id="20018183000180"
            ),
            starkinfra.BrcodePreview(
                id=brcodes[1].id,
                payer_id="20018183000180"
            ),
            starkinfra.BrcodePreview(
                id=brcodes[2].id,
                payer_id="20018183000180"
            ),
            starkinfra.BrcodePreview(
                id=brcodes[3].id,
                payer_id="20018183000180"
            )
        ])

        self.assertTrue(len(previews) == 4)

        index = 0
        for preview in previews:
            self.assertEqual(str(preview.id), str(brcodes[index].id))
            index = index + 1
    
    def test_create_type_instant(self):
        created_dynamic_brcode = create_dynamic_brcode_by_type("instant")
        preview = create_brcode_preview_by_id(created_dynamic_brcode.id)

        self.assertEqual(preview.id, created_dynamic_brcode.id)
        self.assertEqual(preview.due, None)
        self.assertEqual(preview.subscription, None)

    def test_create_type_due(self):
        created_dynamic_brcode = create_dynamic_brcode_by_type("due")
        preview = create_brcode_preview_by_id(created_dynamic_brcode.id)

        self.assertEqual(preview.id, created_dynamic_brcode.id)
        self.assertNotEqual(preview.due, None)
        self.assertEqual(preview.subscription, None)

    def test_create_type_subscription(self):
        created_dynamic_brcode = create_dynamic_brcode_by_type("subscription")
        preview = create_brcode_preview_by_id(created_dynamic_brcode.id)

        self.assertEqual(preview.id, created_dynamic_brcode.id)
        self.assertEqual(preview.payer_id, '')
        self.assertEqual(preview.subscription.type, "qrcode")

    def test_create_type_subscription_and_instant(self):
        created_dynamic_brcode = create_dynamic_brcode_by_type("subscriptionAndInstant")
        preview = create_brcode_preview_by_id(created_dynamic_brcode.id)

        self.assertEqual(preview.id, created_dynamic_brcode.id)
        self.assertNotEqual(preview.payer_id, None)
        self.assertEqual(preview.subscription.type, "qrcodeAndPayment")
    
    def test_create_type_due_and_or_subscription(self):
        created_dynamic_brcode = create_dynamic_brcode_by_type("dueAndOrSubscription")
        preview = create_brcode_preview_by_id(created_dynamic_brcode.id)

        self.assertEqual(preview.id, created_dynamic_brcode.id)
        self.assertNotEqual(preview.payer_id, None)
        self.assertEqual(preview.subscription.type, "paymentAndOrQrcode")


if __name__ == '__main__':
    main()
