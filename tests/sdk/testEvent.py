import starkinfra
from random import choice
from json import loads, dumps
from unittest import TestCase, main
from starkcore.error import InvalidSignatureError
from tests.utils.user import exampleProject

starkinfra.user = exampleProject


class TesteEventProcess(TestCase):
    content = '{"event": {"created": "2022-02-15T20:45:09.852878+00:00", "id": "5015597159022592", "log": {"created": "2022-02-15T20:45:09.436621+00:00", "errors": [{"code": "insufficientFunds", "message": "Amount of funds available is not sufficient to cover the specified transfer"}], "id": "5288053467774976", "request": {"amount": 1000, "bankCode": "34052649", "cashAmount": 0, "cashierBankCode": "", "cashierType": "", "created": "2022-02-15T20:45:08.210009+00:00", "description": "For saving my life", "endToEndId": "E34052649202201272111u34srod1a91", "externalId": "141322efdgber1ecd1s342341321", "fee": 0, "flow": "out", "id": "5137269514043392", "initiatorTaxId": "", "method": "manual", "receiverAccountNumber": "000001", "receiverAccountType": "checking", "receiverBankCode": "00000001", "receiverBranchCode": "0001", "receiverKeyId": "", "receiverName": "Jamie Lennister", "receiverTaxId": "45.987.245/0001-92", "reconciliationId": "", "senderAccountNumber": "000000", "senderAccountType": "checking", "senderBankCode": "34052649", "senderBranchCode": "0000", "senderName": "tyrion Lennister", "senderTaxId": "012.345.678-90", "status": "failed", "tags": [], "updated": "2022-02-15T20:45:09.436661+00:00"}, "type": "failed"}, "subscription": "pix-request.out", "workspaceId": "5692908409716736"}}'
    valid_signature = "MEYCIQD0oFxFQX0fI6B7oqjwLhkRhkDjrOiD86wguEKWdzkJbgIhAPNGUUdlNpYBe+npOaHa9WJopzy3WJYl8XJG6f4ek2R/"
    invalid_signature = "MEYCIQD0oFxFQX0fI6B7oqjwLhkRhkDjrOiD86wjjEKWdzkJbgIhAPNGUUdlNpYBe+npOaHa9WJopzy3WJYl8XJG6f4ek2R/"
    malformed_signature = "something is definitely wrong"

    def test_success(self):
        event = starkinfra.event.parse(
            content=self.content,
            signature=self.valid_signature
        )
        print(event)

    def test_normalized_success(self):
        event = starkinfra.event.parse(
            content=dumps(loads(self.content), sort_keys=False, indent=4),
            signature=self.valid_signature
        )
        print(event)

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


if __name__ == '__main__':
    main()
