import starkinfra
from datetime import datetime, date, timedelta
from unittest import TestCase, main
from tests.utils.user import exampleProject
from starkinfra.individualaccountrequest import Address
from tests.utils.individualAccountRequest import generateExampleIndividualAccountRequestJson


starkinfra.user = exampleProject


class TestIndividualAccountRequestPost(TestCase):

    def test_success(self):
        requests = generateExampleIndividualAccountRequestJson(n=1)
        requests = starkinfra.individualaccountrequest.create(requests)
        for request in requests:
            self.assertIsNotNone(request.id)
            self.assertIsNotNone(request.status)
            self.assertEqual(request.account_type, "individual")

    def test_success_output_only_ignored(self):
        requests = generateExampleIndividualAccountRequestJson(n=1)
        requests[0].status = "created"
        requests[0].account_type = "individual"
        requests[0].flags = []
        requests = starkinfra.individualaccountrequest.create(requests)
        for request in requests:
            self.assertIsNotNone(request.id)


class TestIndividualAccountRequestAddress(TestCase):

    def test_success_address_is_object(self):
        requests = generateExampleIndividualAccountRequestJson(n=1)
        address = requests[0].address
        self.assertIsInstance(address, Address)
        self.assertEqual(address.street, "Rua do Estilo Barroco")
        self.assertEqual(address.number, "648")
        self.assertEqual(address.neighborhood, "Santo Amaro")
        self.assertEqual(address.city, "Sao Paulo")
        self.assertEqual(address.state, "SP")
        self.assertEqual(address.zip_code, "05724005")

    def test_success_address_not_flattened(self):
        requests = generateExampleIndividualAccountRequestJson(n=1)
        request = requests[0]
        self.assertFalse(hasattr(request, "address_street"))
        self.assertFalse(hasattr(request, "address_city"))
        self.assertFalse(hasattr(request, "address_zip_code"))


class TestIndividualAccountRequestQuery(TestCase):

    def test_success(self):
        requests = list(starkinfra.individualaccountrequest.query(limit=10))
        for request in requests:
            self.assertIsNotNone(request.id)

    def test_success_with_params(self):
        requests = starkinfra.individualaccountrequest.query(
            limit=10,
            after=date.today() - timedelta(days=100),
            before=date.today(),
            status="created",
            tags=["a", "b"],
            ids=["1", "2", "3"],
        )
        self.assertEqual(len(list(requests)), 0)


class TestIndividualAccountRequestPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            requests, cursor = starkinfra.individualaccountrequest.page(limit=2, cursor=cursor)
            for request in requests:
                self.assertFalse(request.id in ids)
                ids.append(request.id)
            if cursor is None:
                break
        self.assertTrue(len(ids) == 4)


class TestIndividualAccountRequestGet(TestCase):

    def test_success(self):
        requests = starkinfra.individualaccountrequest.query(limit=1)
        request_id = next(requests).id
        request = starkinfra.individualaccountrequest.get(id=request_id)
        self.assertIsNotNone(request.id)
        self.assertEqual(request.id, request_id)

    def test_success_datetime_parsed(self):
        requests = starkinfra.individualaccountrequest.query(limit=1)
        request = starkinfra.individualaccountrequest.get(id=next(requests).id)
        self.assertIsInstance(request.created, datetime)
        self.assertIsInstance(request.updated, datetime)

    def test_success_status_enum(self):
        requests = list(starkinfra.individualaccountrequest.query(limit=5))
        for request in requests:
            self.assertIn(
                request.status,
                ["approved", "created", "denied", "processing", "updated"],
            )


class TestIndividualAccountRequestUpdate(TestCase):

    def test_success(self):
        requests = starkinfra.individualaccountrequest.query(limit=1)
        for request in requests:
            updated = starkinfra.individualaccountrequest.update(request.id, name=request.name)
            self.assertEqual(updated.id, request.id)

    def test_success_address_replaced(self):
        requests = starkinfra.individualaccountrequest.query(limit=1)
        new_address = Address(
            street="Avenida Paulista",
            number="1000",
            neighborhood="Bela Vista",
            city="Sao Paulo",
            state="SP",
            zip_code="01310100",
        )
        for request in requests:
            updated = starkinfra.individualaccountrequest.update(request.id, address=new_address)
            self.assertEqual(updated.id, request.id)


class TestIndividualAccountRequestInvalid(TestCase):

    def test_invalid_name(self):
        requests = generateExampleIndividualAccountRequestJson(n=1)
        requests[0].name = ""
        with self.assertRaises(starkinfra.error.InputErrors):
            starkinfra.individualaccountrequest.create(requests)

    def test_invalid_tax_id(self):
        requests = generateExampleIndividualAccountRequestJson(n=1)
        requests[0].tax_id = "000.000.000-00"
        with self.assertRaises(starkinfra.error.InputErrors):
            starkinfra.individualaccountrequest.create(requests)

    def test_invalid_address(self):
        requests = generateExampleIndividualAccountRequestJson(n=1)
        requests[0].address = Address(
            street="Rua do Estilo Barroco",
        )
        with self.assertRaises(starkinfra.error.InputErrors):
            starkinfra.individualaccountrequest.create(requests)

    def test_invalid_income(self):
        requests = generateExampleIndividualAccountRequestJson(n=1)
        requests[0].income = -1
        with self.assertRaises(starkinfra.error.InputErrors):
            starkinfra.individualaccountrequest.create(requests)

    def test_invalid_status_transition(self):
        with self.assertRaises(starkinfra.error.InputErrors):
            starkinfra.individualaccountrequest.update("0", status="not-a-real-status")

    def test_unknown_id(self):
        with self.assertRaises(starkinfra.error.InputErrors):
            starkinfra.individualaccountrequest.get("0")


if __name__ == '__main__':
    main()
