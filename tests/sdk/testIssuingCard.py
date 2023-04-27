import starkinfra
from unittest import TestCase, main
from datetime import date, timedelta
from starkinfra import issuingholder
from tests.utils.holder import generateExampleHoldersJson
from tests.utils.user import exampleProject
from tests.utils.card import generateExampleCardsJson

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


if __name__ == '__main__':
    main()
