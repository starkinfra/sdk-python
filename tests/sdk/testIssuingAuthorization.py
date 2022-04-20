import starkinfra
from json import loads, dumps
from unittest import TestCase, main
from starkcore.error import InvalidSignatureError
from tests.utils.user import exampleProject

starkinfra.user = exampleProject


class TestIssuingAuthorizationParseRight(TestCase):
    content = '{"acquirerId": "236090", "amount": 100, "cardId": "5671893688385536", "cardTags": [], "endToEndId": "2fa7ef9f-b889-4bae-ac02-16749c04a3b6", "holderId": "5917814565109760", "holderTags": [], "isPartialAllowed": false, "issuerAmount": 100, "issuerCurrencyCode": "BRL", "merchantAmount": 100, "merchantCategoryCode": "bookStores", "merchantCountryCode": "BRA", "merchantCurrencyCode": "BRL", "merchantFee": 0, "merchantId": "204933612653639", "merchantName": "COMPANY 123", "methodCode": "token", "purpose": "purchase", "score": null, "tax": 0, "walletId": ""}'
    valid_signature = "MEUCIBxymWEpit50lDqFKFHYOgyyqvE5kiHERi0ZM6cJpcvmAiEA2wwIkxcsuexh9BjcyAbZxprpRUyjcZJ2vBAjdd7o28Q="
    invalid_signature = "MEUCIQDOpo1j+V40DNZK2URL2786UQK/8mDXon9ayEd8U0/l7AIgYXtIZJBTs8zCRR3vmted6Ehz/qfw1GRut/eYyvf1yOk="

    def test_success(self):
        event = starkinfra.issuingauthorization.parse(
            content=self.content,
            signature=self.valid_signature
        )
        print(event)

    def test_normalized_success(self):
        event = starkinfra.issuingauthorization.parse(
            content=dumps(loads(self.content), sort_keys=False, indent=4),
            signature=self.valid_signature
        )
        print(event)

    def test_invalid_signature(self):
        with self.assertRaises(InvalidSignatureError):
            starkinfra.issuingauthorization.parse(
                content=self.content,
                signature=self.invalid_signature,
            )


if __name__ == '__main__':
    main()
