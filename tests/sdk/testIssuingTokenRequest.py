import starkinfra
from unittest import TestCase, main
from tests.utils.user import exampleProject

starkinfra.user = exampleProject


class TestIssuingTokenRequestCreate(TestCase):

    def test_success(self):
        cards = starkinfra.issuingcard.query(status="active", limit=1)
        for card in cards:
            request = starkinfra.issuingtokenrequest.create(
                starkinfra.IssuingTokenRequest(
                    card_id=card.id,
                    wallet_id="google",
                    method_code="app"
                )
            )
            self.assertGreater(len(request.content), 1000)


if __name__ == '__main__':
    main()
