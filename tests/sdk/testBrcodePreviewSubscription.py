from datetime import datetime
from unittest import TestCase, main
from starkcore.utils.api import from_api_json
from starkinfra.brcodepreview.__brcodepreview import _resource as brcode_preview_resource


class TestSubscriptionParsing(TestCase):

    def test_parse_subscription_with_empty_installment_end(self):
        preview = from_api_json(brcode_preview_resource, {
            "id": "00020126180014br.gov.bcb.pix5204000053039865802BR5913Fulano de Tal63046078",
            "payerId": "",
            "subscription": {
                "amount": 44448,
                "created": "2026-09-18T00:00:00+00:00",
                "installmentEnd": "",
                "installmentStart": "2026-09-19T02:59:59.999999+00:00",
                "interval": "month",
                "type": "qrcode",
                "updated": "2026-09-18T00:00:00+00:00",
            },
        })

        self.assertIsNone(preview.subscription.installment_end)
        self.assertEqual(preview.subscription.installment_start, datetime(2026, 9, 19, 2, 59, 59, 999999))
        self.assertEqual(preview.subscription.created, datetime(2026, 9, 18))
        self.assertEqual(preview.subscription.interval, "month")

    def test_parse_subscription_with_empty_installment_start_and_end(self):
        preview = from_api_json(brcode_preview_resource, {
            "id": "00020126180014br.gov.bcb.pix5204000053039865802BR5913Fulano de Tal63046078",
            "payerId": "",
            "subscription": {
                "amount": 44448,
                "created": "2026-09-18T00:00:00+00:00",
                "installmentEnd": "",
                "installmentStart": "",
                "interval": "month",
                "type": "qrcode",
                "updated": "2026-09-18T00:00:00+00:00",
            },
        })

        self.assertIsNone(preview.subscription.installment_start)
        self.assertIsNone(preview.subscription.installment_end)
        self.assertEqual(preview.subscription.created, datetime(2026, 9, 18))
        self.assertEqual(preview.subscription.updated, datetime(2026, 9, 18))


if __name__ == '__main__':
    main()
