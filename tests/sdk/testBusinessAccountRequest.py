import starkinfra
from datetime import datetime, date, timedelta
from unittest import TestCase, main
from tests.utils.user import exampleProject
from starkcore.utils.api import api_json, from_api_json
from starkinfra import BusinessAccountRequest
from starkinfra.businessaccountrequest import Address, Owner
from starkinfra.businessaccountrequest.__address import resource as address_resource
from starkinfra.businessaccountrequest.__owner import resource as owner_resource
from tests.utils.businessAccountRequest import generateExampleBusinessAccountRequestJson
from tests.utils.businessAccountRequest import _generateExampleAddress


starkinfra.user = exampleProject


class TestBusinessAccountRequestAddress(TestCase):

    def test_success_serialized_as_camel_case(self):
        address = Address(
            street="Av. Faria Lima",
            number="2000",
            neighborhood="Itaim Bibi",
            city="Sao Paulo",
            state="SP",
            zip_code="04538-132",
            complement="Sala 42",
        )
        self.assertEqual(api_json(address), {
            "street": "Av. Faria Lima",
            "number": "2000",
            "neighborhood": "Itaim Bibi",
            "city": "Sao Paulo",
            "state": "SP",
            "zipCode": "04538-132",
            "complement": "Sala 42",
        })

    def test_success_complement_is_optional(self):
        address = Address(
            street="Av. Faria Lima",
            number="2000",
            neighborhood="Itaim Bibi",
            city="Sao Paulo",
            state="SP",
            zip_code="04538-132",
        )
        self.assertIsNone(address.complement)
        self.assertNotIn("complement", api_json(address))

    def test_success_parsed_from_api(self):
        address = from_api_json(address_resource, {
            "street": "Av. Faria Lima",
            "zipCode": "04538-132",
            "complement": "Sala 42",
        })
        self.assertIsInstance(address, Address)
        self.assertEqual(address.zip_code, "04538-132")
        self.assertEqual(address.complement, "Sala 42")
        self.assertIsNone(address.city)


class TestBusinessAccountRequestOwner(TestCase):

    def test_success_serialized_as_camel_case(self):
        owner = Owner(tax_id="012.345.678-90", name="Jamie Lannister", role="partner")
        self.assertEqual(api_json(owner), {
            "taxId": "012.345.678-90",
            "name": "Jamie Lannister",
            "role": "partner",
        })

    def test_success_return_only_attributes_omitted_on_create(self):
        owner = Owner(tax_id="012.345.678-90", name="Jamie Lannister", role="representative")
        self.assertIsNone(owner.identity_id)
        self.assertIsNone(owner.validator_link)
        self.assertIsNone(owner.status)
        payload = api_json(owner)
        self.assertNotIn("identityId", payload)
        self.assertNotIn("validatorLink", payload)
        self.assertNotIn("status", payload)

    def test_success_parsed_from_api(self):
        owner = from_api_json(owner_resource, {
            "taxId": "012.345.678-90",
            "name": "Jamie Lannister",
            "role": "partner",
            "identityId": "5709594221805568",
            "validatorLink": "https://example.invalid/webview/token",
            "status": "created",
        })
        self.assertIsInstance(owner, Owner)
        self.assertEqual(owner.identity_id, "5709594221805568")
        self.assertEqual(owner.validator_link, "https://example.invalid/webview/token")
        self.assertEqual(owner.status, "created")

    def test_success_owner_list_serialized(self):
        owners = [
            Owner(tax_id="012.345.678-90", name="Jamie Lannister", role="partner"),
            Owner(tax_id="812.531.960-36", name="Cersei Lannister", role="representative"),
        ]
        payload = api_json({"owners": owners})
        self.assertEqual(payload["owners"], [
            {"taxId": "012.345.678-90", "name": "Jamie Lannister", "role": "partner"},
            {"taxId": "812.531.960-36", "name": "Cersei Lannister", "role": "representative"},
        ])


class TestBusinessAccountRequestParse(TestCase):

    def test_success_owners_from_dicts(self):
        request = BusinessAccountRequest(
            address={"street": "Av. Faria Lima", "zipCode": "04538-132"},
            revenue=100000000,
            name="Stark Bank S.A.",
            tax_id="20.018.183/0001-80",
            owners=[{"taxId": "012.345.678-90", "name": "Jamie Lannister", "role": "partner"}],
        )
        self.assertIsInstance(request.address, Address)
        self.assertEqual(request.address.zip_code, "04538-132")
        self.assertIsInstance(request.owners[0], Owner)
        self.assertEqual(request.owners[0].tax_id, "012.345.678-90")

    def test_success_owners_already_objects(self):
        owners = [Owner(tax_id="012.345.678-90", name="Jamie Lannister", role="partner")]
        request = BusinessAccountRequest(
            address=_generateExampleAddress(),
            revenue=100000000,
            name="Stark Bank S.A.",
            tax_id="20.018.183/0001-80",
            owners=owners,
        )
        self.assertIs(request.owners[0], owners[0])

    def test_success_owners_none_is_not_empty_list(self):
        request = BusinessAccountRequest(
            address=None,
            revenue=100000000,
            name="Stark Bank S.A.",
            tax_id="20.018.183/0001-80",
            owners=None,
        )
        self.assertIsNone(request.owners)
        self.assertIsNone(request.address)
        payload = api_json(request)
        self.assertNotIn("owners", payload)
        self.assertNotIn("address", payload)

    def test_success_full_payload_is_camel_case(self):
        request = generateExampleBusinessAccountRequestJson(n=1)[0]
        payload = api_json(request)
        self.assertIn("taxId", payload)
        self.assertIn("revenue", payload)
        self.assertEqual(payload["address"]["zipCode"], "04538-132")
        self.assertEqual(payload["address"]["complement"], "Sala 42")
        for owner in payload["owners"]:
            self.assertIn("taxId", owner)
            self.assertIn("role", owner)
            self.assertNotIn("validatorLink", owner)


class TestBusinessAccountRequestPost(TestCase):

    def test_success(self):
        requests = generateExampleBusinessAccountRequestJson(n=1)
        requests = starkinfra.businessaccountrequest.create(requests)
        for request in requests:
            self.assertIsNotNone(request.id)
            self.assertIsNotNone(request.status)
            self.assertEqual(request.account_type, "business")
            self.assertIsInstance(request.address, Address)
            for owner in request.owners:
                self.assertIsInstance(owner, Owner)


class TestBusinessAccountRequestQuery(TestCase):

    def test_success(self):
        requests = list(starkinfra.businessaccountrequest.query(limit=10))
        for request in requests:
            self.assertIsNotNone(request.id)

    def test_success_with_params(self):
        requests = starkinfra.businessaccountrequest.query(
            limit=10,
            after=date.today() - timedelta(days=100),
            before=date.today(),
            status="created",
            tags=["a", "b"],
            ids=["1", "2", "3"],
        )
        self.assertEqual(len(list(requests)), 0)


class TestBusinessAccountRequestPage(TestCase):

    def test_success(self):
        starkinfra.businessaccountrequest.create(generateExampleBusinessAccountRequestJson(n=3))

        cursor = None
        ids = []
        for _ in range(2):
            requests, cursor = starkinfra.businessaccountrequest.page(limit=2, cursor=cursor)
            for request in requests:
                self.assertNotIn(request.id, ids)
                ids.append(request.id)
            if cursor is None:
                break
        self.assertGreaterEqual(len(ids), 2)


class TestBusinessAccountRequestGet(TestCase):

    def test_success(self):
        created = starkinfra.businessaccountrequest.create(generateExampleBusinessAccountRequestJson(n=1))[0]
        request = starkinfra.businessaccountrequest.get(id=created.id)
        self.assertEqual(request.id, created.id)
        self.assertIsInstance(request.created, datetime)

    def test_success_status_enum(self):
        created = starkinfra.businessaccountrequest.create(generateExampleBusinessAccountRequestJson(n=1))[0]
        request = starkinfra.businessaccountrequest.get(id=created.id)
        self.assertIn(request.status, ["created", "processing", "approved", "denied"])

    def test_unknown_id(self):
        with self.assertRaises(starkinfra.error.InputErrors):
            starkinfra.businessaccountrequest.get("0")


if __name__ == '__main__':
    main()
