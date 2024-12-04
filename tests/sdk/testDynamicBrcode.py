import starkinfra
from random import random, uniform
from unittest import TestCase, main
from datetime import date, timedelta, datetime
from tests.utils.user import exampleProject
from starkcore.error import InvalidSignatureError
from tests.utils.dynamicBrcode import generateExampleDynamicBrcodeJson

starkinfra.user = exampleProject


class TestDynamicBrcodeQuery(TestCase):

    def test_success(self):
        dynamic_brcodes = starkinfra.dynamicbrcode.query(
            after=date.today() - timedelta(days=100),
            before=date.today(),
            uuids=[
                "68a6af231c594a40bd11a80cb980c400",
                "ba989316ffeb4500a60c3636eca90d7e"
            ],
            limit=8
        )
        for dynamic_brcode in dynamic_brcodes:
            print(dynamic_brcode)
            self.assertEqual(dynamic_brcode.id, str(dynamic_brcode.id))


class TestDynamicBrcodePage(TestCase):

    def test_success(self):
        cursor = None
        uuids = []
        for _ in range(2):
            brcodes, cursor = starkinfra.dynamicbrcode.page(limit=2, cursor=cursor)
            for brcode in brcodes:
                print(brcode)
                self.assertFalse(brcode.uuid in uuids)
                uuids.append(brcode.id)
            if cursor is None:
                break
        self.assertTrue(len(uuids) == 4)


class TestDynamicBrcodeGet(TestCase):

    def test_success(self):
        dynamic_brcodes = starkinfra.dynamicbrcode.query(limit=1)
        dynamic_brcode = starkinfra.dynamicbrcode.get(uuid=next(dynamic_brcodes).uuid)
        self.assertEqual(dynamic_brcode.uuid, str(dynamic_brcode.uuid))


class TestDynamicBrcodePost(TestCase):

    def test_success(self):
        example_dynamic_brcode = generateExampleDynamicBrcodeJson()
        dynamic_brcode = starkinfra.dynamicbrcode.create(
            brcodes=[example_dynamic_brcode]
        )
        for brcode in dynamic_brcode:
            print(brcode)


class TestDynamicBrcodeParseRight(TestCase):
    uuid = '21f174ab942843eb90837a5c3135dfd6'
    valid_signature = "MEYCIQC+Ks0M54DPLEbHIi0JrMiWbBFMRETe/U2vy3gTiid3rAIhANMmOaxT03nx2bsdo+vg6EMhWGzdphh90uBH9PY2gJdd"
    invalid_signature = "MEUCIQDOpo1j+V40DNZK2URL2786UQK/8mDXon9ayEd8U0/l7AIgYXtIZJBTs8zCRR3vmted6Ehz/qfw1GRut/eYyvf1yOk="

    def test_success(self):
        uuid = starkinfra.dynamicbrcode.verify(
            uuid=self.uuid,
            signature=self.valid_signature
        )
        print(uuid)

    def test_invalid_signature(self):
        with self.assertRaises(InvalidSignatureError):
            starkinfra.dynamicbrcode.verify(
                uuid=self.uuid,
                signature=self.invalid_signature,
            )


class TestDynamicBrcodeResponse(TestCase):

    def test_due(self):
        response = starkinfra.dynamicbrcode.response_due(
            version=1,
            created=datetime(2022, 3, 10, 10, 30, 0, 0),
            due="2022-07-15",
            expiration=timedelta(seconds=100000),
            key_id="+5511989898989",
            status="paid",
            reconciliation_id="b77f5236-7ab9-4487-9f95-66ee6eaf1781",
            nominal_amount=100,
            sender_name="Anthony Edward Stark",
            sender_tax_id="012.345.678-90",
            receiver_name="Jamie Lannister",
            receiver_tax_id="20.018.183/0001-8",
            receiver_street_line="Av. Paulista, 200",
            receiver_city="Sao Paulo",
            receiver_state_code="SP",
            receiver_zip_code="01234-567",
            fine=uniform(0, 100),
            interest=uniform(0, 1),
            discounts=[
                {
                    "percentage": 5,
                    "due": datetime(2022, 3, 10, 10, 30, 0, 0),
                },{
                    "percentage": 1,
                    "due": datetime(2022, 3, 10, 10, 30, 0, 0),
                }
            ],
            description="teste Python",
            data= [
                {
                    "key": "desconto para pagamento antecipado",
                    "value": "3.80",
                }
            ]
        )
        print(response)

    def test_instant(self):
        response = starkinfra.dynamicbrcode.response_instant(
            version=1,
            created="2022-07-01",
            key_id="+5511989898989",
            status="paid",
            reconciliation_id="b77f5236-7ab9-4487-9f95-66ee6eaf1781",
            amount=100,
            data=[
                {
                    "key": "desconto para pagamento antecipado",
                    "value": "3.80",
                }
            ]
        )
        print(response)
        

if __name__ == '__main__':
    main()
