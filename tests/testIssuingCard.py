import starkinfra
from unittest import TestCase, main
from tests.utils.user import exampleProject
from tests.utils.card import generateExampleCardsJson

starkinfra.user = exampleProject


class TestIssuingCardQuery(TestCase):

    def test_success(self):
        cards = starkinfra.issuingcard.query()
        for card in cards:
            self.assertIsInstance(card.id, str)


class TestIssuingCardPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            cards, cursor = starkinfra.issuingcard.page(limit=2, cursor=cursor)
            for card in cards:
                self.assertFalse(card.id in ids)
                ids.append(card.id)
            if cursor is None:
                break


class TestIssuingCardGet(TestCase):

    def test_success(self):
        cards = starkinfra.issuingcard.query(limit=1)
        card = starkinfra.issuingcard.get(id=next(cards).id)
        self.assertIsInstance(card.id, str)


class TestIssuingCardPostAndDelete(TestCase):

    def test_success(self):
        holder = next(starkinfra.issuingholder.query(limit=1))
        cards = starkinfra.issuingcard.create(generateExampleCardsJson(n=1, holder=holder))
        card_id = cards[0].id
        card = starkinfra.issuingcard.delete(id=card_id)
        self.assertIsInstance(card.id, str)


if __name__ == '__main__':
    main()
