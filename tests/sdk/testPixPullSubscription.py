import starkinfra
from unittest import TestCase, main
from datetime import timedelta, date
from tests.utils.user import exampleProject
from starkcore.error import InvalidSignatureError, InputErrors
from tests.utils.pixPullSubscription import generateExamplePixPullSubscriptionJson


starkinfra.user = exampleProject


class TestPixPullSubscriptionPost(TestCase):
    def test_success(self):
        subscriptions = generateExamplePixPullSubscriptionJson(n=2)
        subscriptions = starkinfra.pixpullsubscription.create(subscriptions)
        for subscription in subscriptions:
            check = starkinfra.pixpullsubscription.get(subscription.id)
            self.assertEqual(check.id, subscription.id)


class TestPixPullSubscriptionQuery(TestCase):

    def test_success(self):
        subscriptions = list(starkinfra.pixpullsubscription.query(limit=10))
        self.assertLessEqual(len(subscriptions), 10)

    def test_success_with_params(self):
        seeded = list(starkinfra.pixpullsubscription.query(limit=3))
        if not seeded:
            self.skipTest("no subscriptions available to round-trip ids filter")
        seeded_ids = [s.id for s in seeded]
        round_trip = list(starkinfra.pixpullsubscription.query(
            limit=10,
            after=date.today() - timedelta(days=100),
            before=date.today(),
            tags=["iron", "bank"],
            ids=seeded_ids,
        ))
        returned_ids = {s.id for s in round_trip}
        self.assertTrue(returned_ids.issubset(set(seeded_ids)))


class TestPixPullSubscriptionPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            subscriptions, cursor = starkinfra.pixpullsubscription.page(limit=2, cursor=cursor)
            for subscription in subscriptions:
                self.assertFalse(subscription.id in ids)
                ids.append(subscription.id)
            if cursor is None:
                break
        self.assertTrue(len(ids) <= 4)


class TestPixPullSubscriptionInfoGet(TestCase):

    def test_success(self):
        subscriptions = starkinfra.pixpullsubscription.query(limit=1)
        subscription = next(subscriptions, None)
        if subscription is None:
            self.skipTest("no subscriptions available to fetch")
        result = starkinfra.pixpullsubscription.get(id=subscription.id)
        self.assertIsNotNone(result.id)
        self.assertEqual(result.id, subscription.id)


class TestPixPullSubscriptionPatch(TestCase):

    def test_success(self):
        subscriptions = starkinfra.pixpullsubscription.query(status=["active"], limit=1)
        subscription = next(subscriptions, None)
        if subscription is None:
            self.skipTest("no active subscriptions available to patch")
        try:
            updated = starkinfra.pixpullsubscription.update(
                id=subscription.id,
                status="confirmed",
                sender_city_code="3550308",
                tags=["patched", "test"],
            )
        except InputErrors as error:
            self.assertTrue(len(error.errors) > 0)
            return
        self.assertEqual(updated.id, subscription.id)


class TestPixPullSubscriptionCancel(TestCase):

    def test_success(self):
        subscriptions = starkinfra.pixpullsubscription.query(status=["active"], limit=1)
        subscription = next(subscriptions, None)
        if subscription is None:
            self.skipTest("no active subscriptions available to cancel")
        try:
            canceled = starkinfra.pixpullsubscription.cancel(
                id=subscription.id,
                reason="accountClosed",
            )
        except InputErrors as error:
            self.assertTrue(len(error.errors) > 0)
            return
        self.assertEqual(canceled.id, subscription.id)


class TestPixPullSubscriptionParse(TestCase):
    content = '{"event": {"created": "2026-03-17T20:24:02.006080+00:00", "id": "5739991880695808", "log": {"created": "2026-03-17T20:23:58.050406+00:00", "errors": [], "id": "5340798381981696", "reason": "", "subscription": {"amount": 52064, "amountMinLimit": 0, "bacenId": "RR321606372026170317231564231", "created": "2026-03-17T20:23:57.255567+00:00", "description": "A Lannister always pays his debts", "due": "2026-04-17T02:59:59.999000+00:00", "externalId": "606512134", "flow": "out", "id": "5656970050666496", "installmentEnd": "", "installmentStart": "2026-03-18T02:59:59.999999+00:00", "interval": "month", "pullRetryLimit": 3, "receiverBankCode": "32160637", "receiverName": "Stark Bank", "receiverTaxId": "39.908.427/0001-28", "referenceCode": "36135971", "senderAccountNumber": "55213", "senderBankCode": null, "senderBranchCode": "356", "senderCityCode": "", "senderFinalName": "STARK SCD S.A.", "senderFinalTaxId": "39.908.427/0001-28", "senderTaxId": "99.999.919/9999-79", "status": "created", "tags": [], "type": "push", "updated": "2026-03-17T20:23:58.050421+00:00"}, "type": "delivering"}, "subscription": "pix-pull-subscription", "workspaceId": "4828094443552768"}}'
    valid_signature = "MEUCIQCCZWR4+JYoDNENLnRbSCGGZf+atOaG4q8jWB3ADgc+DQIgIZ1LuXLZ06pke2qzaMNTlDLwcriuH+S3ve1aTQeqNK0="
    invalid_signature = "MEUCIQCCZWR4+JYoDNENLnRbSCGGZf+atOaG4q8jWB3ADgc+DQIgIZ1LuXLZ06pke2qzaMNTlDLwcriuH+S3ve1aTQEqNK0="
    malformed_signature = "something is definitely wrong"

    def test_success(self):
        event = starkinfra.event.parse(
            content=self.content,
            signature=self.valid_signature,
        )
        self.assertIsNotNone(event.id)
        self.assertEqual(event.subscription, "pix-pull-subscription")
        self.assertIsNotNone(event.log.subscription.id)

    def test_invalid_signature(self):
        with self.assertRaises(InvalidSignatureError):
            starkinfra.event.parse(
                content=self.content,
                signature=self.invalid_signature,
            )

    def test_malformed_signature(self):
        with self.assertRaises(InvalidSignatureError):
            starkinfra.event.parse(
                content=self.content,
                signature=self.malformed_signature,
            )


class TestPixPullSubscriptionNormalization(TestCase):

    def test_empty_due_and_installment_end_become_none(self):
        sample = generateExamplePixPullSubscriptionJson(n=1)[0]
        sample.due = ""
        sample.installment_end = ""
        normalized = starkinfra.PixPullSubscription(
            bacen_id=sample.bacen_id,
            external_id=sample.external_id,
            installment_start=sample.installment_start,
            interval=sample.interval,
            receiver_name=sample.receiver_name,
            receiver_tax_id=sample.receiver_tax_id,
            receiver_bank_code=sample.receiver_bank_code,
            reference_code=sample.reference_code,
            sender_account_number=sample.sender_account_number,
            sender_bank_code=sample.sender_bank_code,
            sender_branch_code=sample.sender_branch_code,
            sender_city_code=sample.sender_city_code,
            sender_tax_id=sample.sender_tax_id,
            type=sample.type,
            amount=sample.amount,
            amount_min_limit=getattr(sample, "amount_min_limit", None),
            description=getattr(sample, "description", None),
            due="",
            installment_end="",
            pull_retry_limit=getattr(sample, "pull_retry_limit", None),
            sender_final_name=getattr(sample, "sender_final_name", None),
            sender_final_tax_id=getattr(sample, "sender_final_tax_id", None),
            tags=sample.tags,
        )
        self.assertIsNone(normalized.due)
        self.assertIsNone(normalized.installment_end)


if __name__ == '__main__':
    main()
