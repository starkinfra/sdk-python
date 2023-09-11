import starkinfra
from json import dumps, loads
from unittest import TestCase, main
from datetime import timedelta, date
from tests.utils.user import exampleProject
from starkcore.error import InvalidSignatureError


starkinfra.user = exampleProject


class TestIssuingTokenQuery(TestCase):

    def test_success(self):
        tokens = starkinfra.issuingtoken.query(limit=5)
        for token in tokens:
            self.assertEqual(token.id, str(token.id))


class TestIssuingTokenPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            tokens, cursor = starkinfra.issuingtoken.page(limit=2, cursor=cursor)
            for token in tokens:
                self.assertEqual(token.id, str(token.id))
            if cursor is None:
                break


class TestIssuingTokenGet(TestCase):

    def test_success(self):
        tokens = starkinfra.issuingtoken.query(limit=1)
        for token in tokens:
            token = starkinfra.issuingtoken.get(token.id)
            self.assertEqual(token.id, str(token.id))
            print(token)


class TestIssuingTokenUpdateAndDelete(TestCase):

    def test_success(self):
        tokens = starkinfra.issuingtoken.query(limit=1)
        for token in tokens:
            updated_token = starkinfra.issuingtoken.update(id=token.id, status="blocked")
            canceled_token = starkinfra.issuingtoken.cancel(id=updated_token.id)
            self.assertEqual(canceled_token.id, str(canceled_token.id))


class TestIssuingTokenParseRight(TestCase):
    content = "{\"deviceName\": \"My phone\", \"methodCode\": \"manual\", \"walletName\": \"Google Pay\", \"activationCode\": \"\", \"deviceSerialNumber\": \"2F6D63\", \"deviceImei\": \"352099001761481\", \"deviceType\": \"Phone\", \"walletInstanceId\": \"1b24f24a24ba98e27d43e345b532a245e4723d7a9c4f624e\", \"deviceOsVersion\": \"4.4.4\", \"cardId\": \"5189831499972623\", \"deviceOsName\": \"Android\", \"merchantId\": \"12345678901\", \"walletId\": \"google\"}"
    valid_signature = "MEYCIQC4XbhjxEp9VhowLeg9JbSOo94FCRWE9GI7l7OuHh0bUwIhAJBuLDl5DAT9L4iMI0qYQ+PVmBIG5scxxvkWSsoWmwi4"
    invalid_signature = "MEUCIQDOpo1j+V40DNZK2URL2786UQK/8mDXon9ayEd8U0/l7AIgYXtIZJBTs8zCRR3vmted6Ehz/qfw1GRut/eYyvf1yOk="

    def test_success(self):
        event = starkinfra.issuingtoken.parse(
            content=self.content,
            signature=self.valid_signature
        )
        print(event)

    def test_normalized_success(self):
        event = starkinfra.issuingtoken.parse(
            content=dumps(loads(self.content), sort_keys=False, indent=4),
            signature=self.valid_signature
        )
        print(event)

    def test_invalid_signature(self):
        with self.assertRaises(InvalidSignatureError):
            starkinfra.issuingtoken.parse(
                content=self.content,
                signature=self.invalid_signature,
            )


class TestIssuingTokenResponseAuthorization(TestCase):

    def test_approved(self):
        response = starkinfra.issuingtoken.response_authorization(
            status="approved",
            activation_methods=[
                {
                    "type": "app",
                    "value": "com.subissuer.android"
                },
                {
                    "type": "text",
                    "value": "** *****-5678"
                }
            ],
            design_id="4584031664472031",
            tags=["tony", "stark"]
        )
        print(response)

    def test_denied(self):
        response = starkinfra.issuingtoken.response_authorization(
            status="denied",
            reason="other",
            tags=["tony", "stark"]
        )
        print(response)


class TestIssuingTokenResponseActivation(TestCase):

    def test_approved(self):
        response = starkinfra.issuingtoken.response_activation(
            status="approved",
            tags=["tony", "stark"]
        )
        print(response)

    def test_denied(self):
        response = starkinfra.issuingtoken.response_activation(
            status="denied",
            reason="other",
            tags=["tony", "stark"]
        )
        print(response)


if __name__ == '__main__':
    main()
