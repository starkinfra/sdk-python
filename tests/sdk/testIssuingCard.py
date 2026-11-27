import inspect
import starkinfra
from json import dumps, loads
from unittest import TestCase, main
from unittest.mock import MagicMock, patch
from datetime import date, timedelta
from starkcore.error import InputErrors
from starkinfra import issuingholder
from tests.utils.holder import generateExampleHoldersJson
from tests.utils.user import exampleProject
from tests.utils.card import generateExampleCardsJson, generateExampleCardsWithoutHolderJson, \
    findExistingHolderForProduct

starkinfra.user = exampleProject


class TestIssuingCardQuery(TestCase):

    def test_success(self):
        cards = starkinfra.issuingcard.query(
            limit=10,
            after=date.today() - timedelta(days=100),
            before=date.today()
        )
        for card in cards:
            self.assertEqual(card.id, str(card.id))


class TestIssuingCardPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            cards, cursor = starkinfra.issuingcard.page(
                limit=2,
                after=date.today() - timedelta(days=100),
                before=date.today(),
                cursor=cursor
            )
            for card in cards:
                self.assertFalse(card.id in ids)
                ids.append(card.id)
            if cursor is None:
                break


class TestIssuingCardGet(TestCase):

    def test_success(self):
        cards = starkinfra.issuingcard.query(limit=1)
        card = starkinfra.issuingcard.get(id=next(cards).id)
        self.assertEqual(card.id, str(card.id))


class TestIssuingCardPostAndDelete(TestCase):

    def test_success(self):
        holder = issuingholder.create(generateExampleHoldersJson())[0]
        cards = starkinfra.issuingcard.create(cards=generateExampleCardsJson(n=1, holder=holder, product_id="52233227"), expand=["securityCode"])
        self.assertNotEqual(str(cards[0].security_code), "***")
        card_id = cards[0].id
        card = starkinfra.issuingcard.update(card_id, display_name="Updated Name")
        self.assertEqual("Updated Name", card.display_name)
        card = starkinfra.issuingcard.cancel(id=card_id)
        self.assertEqual("canceled", card.status)


class TestIssuingCardUpdate(TestCase):

    def test_success(self):
        holder = issuingholder.create(generateExampleHoldersJson())[0]
        cards = starkinfra.issuingcard.create(cards=generateExampleCardsJson(n=1, holder=holder, product_id="52233227"),
                                              expand=["securityCode"])
        for card in cards:
            self.assertIsNotNone(card.id)
            self.assertEqual(card.status, "active")
            update_card = starkinfra.issuingcard.update(card.id, status="blocked")
            self.assertEqual(update_card.status, "blocked")


def fakeCreatedCardResponse():
    response = MagicMock()
    response.status_code = 200
    response.content = dumps({"cards": [{
        "id": "5656565656565656", "status": "pending", "type": "physical", "holderId": "", "holderName": "",
    }]}).encode("utf-8")
    response.headers = {}
    return response


# Only the outgoing HTTP call is replaced here: payload building and signing run for real.
class TestIssuingCardWithoutHolderPayload(TestCase):

    def test_holder_fields_are_not_sent_when_omitted(self):
        with patch("starkcore.utils.rest.post", return_value=fakeCreatedCardResponse()) as sent:
            cards = starkinfra.issuingcard.create([starkinfra.IssuingCard(product_id="123", type="physical")])
        self.assertEqual(loads(sent.call_args.kwargs["data"]), {"cards": [{"productId": "123", "type": "physical"}]})
        self.assertEqual(cards[0].holder_id, "")
        self.assertEqual(cards[0].holder_name, "")

    def test_holder_fields_are_sent_when_informed(self):
        with patch("starkcore.utils.rest.post", return_value=fakeCreatedCardResponse()) as sent:
            starkinfra.issuingcard.create([starkinfra.IssuingCard(
                holder_name="Tony Stark",
                holder_tax_id="012.345.678-90",
                holder_external_id="my-entity/123",
                product_id="123",
            )])
        self.assertEqual(loads(sent.call_args.kwargs["data"]), {"cards": [{
            "holderName": "Tony Stark",
            "holderTaxId": "012.345.678-90",
            "holderExternalId": "my-entity/123",
            "productId": "123",
        }]})

    def test_holder_fields_keep_their_positions_in_the_constructor(self):
        card = starkinfra.IssuingCard("Tony Stark", "012.345.678-90", "my-entity/123", "ANTHONY STARK")
        self.assertEqual(card.holder_name, "Tony Stark")
        self.assertEqual(card.holder_tax_id, "012.345.678-90")
        self.assertEqual(card.holder_external_id, "my-entity/123")
        self.assertEqual(card.display_name, "ANTHONY STARK")


class TestIssuingCardWithoutHolder(TestCase):

    def test_physical_card_without_holder_is_created_pending(self):
        cards = starkinfra.issuingcard.create(cards=generateExampleCardsWithoutHolderJson(type="physical"))
        try:
            self.assertEqual(len(cards), 1)
            self.assertEqual(cards[0].status, "pending")
            self.assertEqual(cards[0].type, "physical")
            self.assertEqual(cards[0].holder_id, "")
            self.assertEqual(cards[0].holder_name, "")
        finally:
            for card in cards:
                starkinfra.issuingcard.cancel(id=card.id)

    def test_api_rejects_virtual_card_without_holder(self):
        created = []
        try:
            with self.assertRaises(InputErrors):
                created = starkinfra.issuingcard.create(cards=generateExampleCardsWithoutHolderJson(type="virtual"))
        finally:
            for card in created:
                starkinfra.issuingcard.cancel(id=card.id)

    def test_api_rejects_incomplete_holder_fields(self):
        cards = generateExampleCardsWithoutHolderJson(type="physical")
        cards[0].holder_name = "Tony Stark"
        created = []
        try:
            with self.assertRaises(InputErrors):
                created = starkinfra.issuingcard.create(cards=cards)
        finally:
            for card in created:
                starkinfra.issuingcard.cancel(id=card.id)


def fakeUpdatedCardResponse():
    response = MagicMock()
    response.status_code = 200
    response.content = dumps({"card": {"id": "5656565656565656", "status": "pending"}}).encode("utf-8")
    response.headers = {}
    return response


# Only the outgoing HTTP call is replaced here: payload building and signing run for real.
class TestIssuingCardUpdatePayload(TestCase):

    def test_user_keeps_its_position_after_the_existing_parameters(self):
        names = list(inspect.signature(starkinfra.issuingcard.update).parameters)
        self.assertEqual(names[:7], ["id", "status", "pin", "display_name", "rules", "tags", "user"])

    def test_holder_fields_are_not_sent_when_omitted(self):
        with patch("starkcore.utils.rest.patch", return_value=fakeUpdatedCardResponse()) as sent:
            starkinfra.issuingcard.update("5656565656565656", display_name="ANTHONY STARK")
        self.assertEqual(loads(sent.call_args.kwargs["data"]), {"displayName": "ANTHONY STARK"})

    def test_holder_fields_are_sent_alone(self):
        with patch("starkcore.utils.rest.patch", return_value=fakeUpdatedCardResponse()) as sent:
            starkinfra.issuingcard.update(
                "5656565656565656",
                holder_name="Tony Stark",
                holder_tax_id="012.345.678-90",
                holder_external_id="my-entity/123",
            )
        self.assertEqual(loads(sent.call_args.kwargs["data"]), {
            "holderName": "Tony Stark",
            "holderTaxId": "012.345.678-90",
            "holderExternalId": "my-entity/123",
        })

    def test_holder_fields_are_sent_with_status_and_pin(self):
        with patch("starkcore.utils.rest.patch", return_value=fakeUpdatedCardResponse()) as sent:
            starkinfra.issuingcard.update(
                "5656565656565656",
                holder_name="Tony Stark",
                holder_tax_id="012.345.678-90",
                holder_external_id="my-entity/123",
                status="active",
                pin="1234",
            )
        self.assertEqual(loads(sent.call_args.kwargs["data"]), {
            "status": "active",
            "pin": "1234",
            "holderName": "Tony Stark",
            "holderTaxId": "012.345.678-90",
            "holderExternalId": "my-entity/123",
        })


class TestIssuingCardAssignHolder(TestCase):

    def setUp(self):
        product = next(starkinfra.issuingproduct.query(limit=1))
        self.holder = findExistingHolderForProduct(product)
        if self.holder is None:
            self.skipTest("no existing holder compatible with the sandbox product")
        self.cards = starkinfra.issuingcard.create(
            cards=generateExampleCardsWithoutHolderJson(type="physical", product_id=product.id)
        )

    def tearDown(self):
        for card in getattr(self, "cards", []):
            starkinfra.issuingcard.cancel(id=card.id)

    def test_holder_is_assigned_to_a_pending_card(self):
        card = starkinfra.issuingcard.update(
            self.cards[0].id,
            holder_name=self.holder.name,
            holder_tax_id=self.holder.tax_id,
            holder_external_id=self.holder.external_id,
        )
        self.assertEqual(card.status, "pending")
        self.assertEqual(card.holder_id, self.holder.id)
        self.assertEqual(card.holder_name, self.holder.name)

    def test_holder_is_assigned_and_card_activated_in_the_same_call(self):
        card = starkinfra.issuingcard.update(
            self.cards[0].id,
            holder_name=self.holder.name,
            holder_tax_id=self.holder.tax_id,
            holder_external_id=self.holder.external_id,
            status="active",
            pin="1234",
        )
        self.assertEqual(card.status, "active")
        self.assertEqual(card.holder_id, self.holder.id)

    def test_api_rejects_incomplete_holder_fields(self):
        with self.assertRaises(InputErrors):
            starkinfra.issuingcard.update(self.cards[0].id, holder_name=self.holder.name)

    def test_api_rejects_activation_without_holder(self):
        with self.assertRaises(InputErrors):
            starkinfra.issuingcard.update(self.cards[0].id, status="active", pin="1234")


class TestIssuingCardUpdateMultiPayload(TestCase):

    def test_items_are_sent_in_the_cards_list_with_only_informed_fields(self):
        response = MagicMock()
        response.status_code = 200
        response.content = dumps({"cards": [{"id": "1", "status": "pending"}, {"id": "2", "status": "pending"}]}).encode("utf-8")
        response.headers = {}
        with patch("starkcore.utils.rest.patch", return_value=response) as sent:
            cards = starkinfra.issuingcard.update_multi([
                starkinfra.IssuingCard(
                    id="1",
                    holder_name="Tony Stark",
                    holder_tax_id="012.345.678-90",
                    holder_external_id="my-entity/123",
                ),
                {"id": "2", "tags": ["batch"]},
            ])
        call = sent.call_args.kwargs
        self.assertTrue(call["url"].endswith("/v2/issuing-card"))
        self.assertEqual(loads(call["data"]), {"cards": [
            {"id": "1", "holderName": "Tony Stark", "holderTaxId": "012.345.678-90", "holderExternalId": "my-entity/123"},
            {"id": "2", "tags": ["batch"]},
        ]})
        self.assertEqual([card.id for card in cards], ["1", "2"])
        self.assertTrue(all(isinstance(card, starkinfra.IssuingCard) for card in cards))


class TestIssuingCardUpdateMulti(TestCase):

    def setUp(self):
        product = next(starkinfra.issuingproduct.query(limit=1))
        self.holder = findExistingHolderForProduct(product)
        if self.holder is None:
            self.skipTest("no existing holder compatible with the sandbox product")
        self.cards = starkinfra.issuingcard.create(
            cards=generateExampleCardsWithoutHolderJson(n=2, type="physical", product_id=product.id)
        )

    def tearDown(self):
        for card in getattr(self, "cards", []):
            starkinfra.issuingcard.cancel(id=card.id)

    def holderFields(self):
        return {
            "holder_name": self.holder.name,
            "holder_tax_id": self.holder.tax_id,
            "holder_external_id": self.holder.external_id,
        }

    def test_holder_is_assigned_to_several_cards(self):
        updated = starkinfra.issuingcard.update_multi([dict(id=card.id, **self.holderFields()) for card in self.cards])
        self.assertEqual(sorted(card.id for card in updated), sorted(card.id for card in self.cards))
        for card in updated:
            self.assertEqual(card.holder_id, self.holder.id)

    def test_api_rejects_the_whole_list_when_one_item_is_invalid(self):
        items = [dict(id=self.cards[0].id, **self.holderFields()), dict(id="0000000000000001", **self.holderFields())]
        with self.assertRaises(InputErrors):
            starkinfra.issuingcard.update_multi(items)
        card = starkinfra.issuingcard.get(self.cards[0].id)
        self.assertEqual(card.holder_id, "")

    def test_api_rejects_incomplete_holder_fields(self):
        with self.assertRaises(InputErrors):
            starkinfra.issuingcard.update_multi([{"id": self.cards[0].id, "holder_name": self.holder.name}])

    def test_api_rejects_pin_in_the_batch(self):
        with self.assertRaises(InputErrors) as context:
            starkinfra.issuingcard.update_multi([{"id": self.cards[0].id, "pin": "1234"}])
        self.assertEqual(context.exception.errors[0].code, "invalidJson")

    def test_api_rejects_display_name_in_the_batch(self):
        with self.assertRaises(InputErrors) as context:
            starkinfra.issuingcard.update_multi([{"id": self.cards[0].id, "display_name": "Name"}])
        self.assertEqual(context.exception.errors[0].code, "invalidJson")


if __name__ == '__main__':
    main()
