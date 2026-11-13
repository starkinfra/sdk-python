import starkinfra
from datetime import datetime
from unittest import TestCase, main
from unittest.mock import patch
from starkcore.utils.url import urlencode
from starkinfra import IndividualIdentity


_identity_json = {
    "id": "5155165527080961",
    "name": "Edward Stark",
    "taxId": "012.345.678-90",
    "email": "edward.stark@example.com",
    "phone": "(11) 98765-4321",
    "tags": ["employees"],
    "sourceId": "5656565656565656",
    "sourceType": "external",
    "status": "created",
    "proofs": ["identity", "biometric"],
    "validatorLink": "https://identity.starkinfra.com/validator-link?info=eyJpZGVudGl0eUlkIjoiNTE1NTE2NTUyNzA4MDk2MSJ9",
    "deliveryMethod": "manual",
    "workspaceId": "5656565656565656",
    "created": "2026-11-03T12:00:00+00:00",
    "updated": "2026-11-03T12:30:00+00:00",
}


class _Response:

    def __init__(self, body):
        self.body = body

    def json(self):
        return self.body


class _Fetch:

    def __init__(self, body):
        self.body = body
        self.calls = []

    def __call__(self, **kwargs):
        self.calls.append(kwargs)
        return _Response(self.body)


class TestIndividualIdentityContract(TestCase):
    """The requests and responses api-v2-ms-identity serves, checked offline at the wire."""

    def test_create_sends_the_keys_the_api_accepts(self):
        fetch = _Fetch({"identities": [_identity_json]})
        identity = IndividualIdentity(
            name="Edward Stark",
            delivery_method="manual",
            proofs=["identity", "biometric"],
            tax_id="012.345.678-90",
            email="edward.stark@example.com",
            phone="+5511987654321",
            tags=["employees"],
        )
        with patch("starkcore.utils.rest.fetch", fetch):
            identities = starkinfra.individualidentity.create([identity], user=object())
        self.assertEqual(fetch.calls[0]["payload"], {"identities": [{
            "name": "Edward Stark",
            "deliveryMethod": "manual",
            "proofs": ["identity", "biometric"],
            "taxId": "012.345.678-90",
            "email": "edward.stark@example.com",
            "phone": "+5511987654321",
            "tags": ["employees"],
        }]})
        self.assertEqual(identities[0].validator_link, _identity_json["validatorLink"])

    def test_create_without_optional_keys_sends_only_the_required_ones(self):
        fetch = _Fetch({"identities": [_identity_json]})
        identity = IndividualIdentity(name="Edward Stark", delivery_method="automatic", proofs=["identity"],
                                      email="edward.stark@example.com")
        with patch("starkcore.utils.rest.fetch", fetch):
            starkinfra.individualidentity.create([identity], user=object())
        self.assertEqual(fetch.calls[0]["payload"], {"identities": [{
            "name": "Edward Stark",
            "deliveryMethod": "automatic",
            "proofs": ["identity"],
            "email": "edward.stark@example.com",
        }]})

    def test_birth_date_is_no_longer_a_parameter(self):
        identity = IndividualIdentity(name="Edward Stark", delivery_method="manual", proofs=["identity"])
        self.assertFalse(hasattr(identity, "birth_date"))
        with self.assertRaises(TypeError):
            IndividualIdentity(name="Edward Stark", delivery_method="manual", proofs=["identity"],
                               birth_date="2012-03-06")

    def test_update_patches_tax_id_only(self):
        fetch = _Fetch({"identity": _identity_json})
        with patch("starkcore.utils.rest.fetch", fetch):
            identity = starkinfra.individualidentity.update("5155165527080961", tax_id="012.345.678-90",
                                                            user=object())
        self.assertEqual(fetch.calls[0]["path"], "individual-identity/5155165527080961")
        self.assertEqual(fetch.calls[0]["payload"], {"taxId": "012.345.678-90"})
        self.assertEqual(identity.tax_id, "012.345.678-90")

    def test_query_and_page_filter_by_tax_ids_and_email(self):
        fetch = _Fetch({"identities": [_identity_json], "cursor": None})
        with patch("starkcore.utils.rest.fetch", fetch):
            list(starkinfra.individualidentity.query(limit=1, tax_ids=["012.345.678-90"],
                                                     email="edward.stark@example.com", user=object()))
            starkinfra.individualidentity.page(tax_ids=["012.345.678-90"], email="edward.stark@example.com",
                                               user=object())
        self.assertEqual(len(fetch.calls), 2)
        for call in fetch.calls:
            query = urlencode(call["query"])
            self.assertIn("taxIds=012.345.678-90", query)
            self.assertIn("email=edward.stark%40example.com", query)

    def test_every_key_the_api_returns_is_read(self):
        fetch = _Fetch({"identity": _identity_json})
        with patch("starkcore.utils.rest.fetch", fetch):
            identity = starkinfra.individualidentity.get("5155165527080961", user=object())
        self.assertEqual(identity.delivery_method, "manual")
        self.assertEqual(identity.proofs, ["identity", "biometric"])
        self.assertEqual(identity.validator_link, _identity_json["validatorLink"])
        self.assertEqual(identity.source_id, "5656565656565656")
        self.assertEqual(identity.source_type, "external")
        self.assertEqual(identity.workspace_id, "5656565656565656")
        self.assertEqual(identity.email, "edward.stark@example.com")
        self.assertEqual(identity.phone, "(11) 98765-4321")
        self.assertEqual(identity.updated, datetime(2026, 11, 3, 12, 30))
        self.assertEqual(identity.created, datetime(2026, 11, 3, 12, 0))


if __name__ == "__main__":
    main()
