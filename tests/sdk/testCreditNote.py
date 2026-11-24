import os
import starkinfra
from datetime import date
from unittest import TestCase, main
from tests.utils.user import exampleProject
from starkcore.utils.api import api_json, from_api_json
from starkinfra.creditnote.__creditnote import _resource as _creditNoteResource
from starkinfra.creditnote import TemplateReplacements
from tests.utils.creditNote import generateExampleCreditNoteIsoDatetimeJson, generateExampleCreditNoteJson, generateExampleCreditNoteStringDatesJson, generateExampleCreditNoteWithTemplateReplacementsJson


starkinfra.user = exampleProject


class TestCreditNotePost(TestCase):

    def test_success_template_replacements(self):
        request = generateExampleCreditNoteWithTemplateReplacementsJson(
            n=1,
            template_replacements=TemplateReplacements(**TestCreditNoteTemplateReplacements.templateReplacements)
        )
        response = starkinfra.creditnote.create(request)
        self.assertEqual(len(request), len(response))
        for note in response:
            self.assertIsNotNone(note.id)
            self.assertIsInstance(note.template_replacements, TemplateReplacements)
            self.assertEqual(
                TestCreditNoteTemplateReplacements.templateReplacements,
                api_json(note.template_replacements)
            )

    def test_success(self):
        request = generateExampleCreditNoteJson(n=1)
        response = starkinfra.creditnote.create(request)
        self.assertTrue(len(request) == len(response))
        for note in response:
            self.assertIsNotNone(note.id)

    def test_success_iso_datetime(self):
        request = generateExampleCreditNoteIsoDatetimeJson(n=1)
        response = starkinfra.creditnote.create(request)
        self.assertTrue(len(request) == len(response))
        for note in response:
            self.assertIsNotNone(note.id)

    def test_success_string_datetime(self):
        request = generateExampleCreditNoteStringDatesJson(n=1)
        response = starkinfra.creditnote.create(request)
        self.assertTrue(len(request) == len(response))
        for note in response:
            self.assertIsNotNone(note.id)
        

class TestCreditNoteTemplateReplacements(TestCase):

    templateReplacements = {
        "nomeAvalista": "Avalista Teste 2026",
        "cpfCnpjAvalista": "336.959.235-55",
        "enderecoAvalista": "Avenida das Nações Unidas, 2312 - Centro - Mogi das Cruzes, SP"
    }

    def test_serialization_keeps_keys(self):
        note = generateExampleCreditNoteWithTemplateReplacementsJson(n=1, template_replacements=self.templateReplacements)[0]
        self.assertEqual(self.templateReplacements, api_json(note)["templateReplacements"])

    def test_serialization_converts_snake_case_keys_and_drops_none(self):
        note = generateExampleCreditNoteWithTemplateReplacementsJson(
            n=1,
            template_replacements={"guarantor_name": "Jon Snow", "guarantor_taxId": "1", "emptyValue": None}
        )[0]
        self.assertEqual(
            {"guarantorName": "Jon Snow", "guarantorTaxid": "1"},
            api_json(note)["templateReplacements"]
        )

    def test_serialization_omits_when_absent(self):
        note = generateExampleCreditNoteWithTemplateReplacementsJson(n=1)[0]
        self.assertNotIn("templateReplacements", api_json(note))

    def test_serialization_omits_when_none(self):
        note = generateExampleCreditNoteWithTemplateReplacementsJson(n=1, template_replacements=None)[0]
        self.assertNotIn("templateReplacements", api_json(note))

    def test_object_and_dict_serialize_the_same(self):
        values = {"guarantor_name": "Jon Snow", "guarantorTaxId": "1", "emptyValue": None}
        fromDict = generateExampleCreditNoteWithTemplateReplacementsJson(n=1, template_replacements=values)[0]
        fromObject = generateExampleCreditNoteWithTemplateReplacementsJson(
            n=1,
            template_replacements=TemplateReplacements(**values)
        )[0]
        self.assertIsInstance(fromDict.template_replacements, TemplateReplacements)
        self.assertEqual(
            api_json(fromDict)["templateReplacements"],
            api_json(fromObject)["templateReplacements"]
        )
        self.assertEqual(
            {"guarantorName": "Jon Snow", "guarantorTaxId": "1"},
            api_json(fromObject)["templateReplacements"]
        )

    def test_v1_dict_payload_is_unchanged(self):
        note = generateExampleCreditNoteWithTemplateReplacementsJson(
            n=1,
            template_replacements=self.templateReplacements
        )[0]
        self.assertEqual(self.templateReplacements, api_json(note)["templateReplacements"])

    def test_response_keeps_every_key_as_attribute(self):
        note = _parseResponseNote({"guarantorName": "X", "someKeyNobodyDeclared": "Y"})
        self.assertIsInstance(note.template_replacements, TemplateReplacements)
        self.assertEqual("X", getattr(note.template_replacements, "guarantorName"))
        self.assertEqual("Y", getattr(note.template_replacements, "someKeyNobodyDeclared"))
        self.assertEqual(
            {"guarantorName": "X", "someKeyNobodyDeclared": "Y"},
            api_json(note)["templateReplacements"]
        )

    def test_snake_case_names_are_sent_in_camel_case(self):
        replacements = TemplateReplacements(
            guarantor_name="Jon Snow",
            guarantor_tax_id="012.345.678-90",
            guarantor_address="Av. Paulista, 200",
        )
        self.assertEqual(
            {"guarantorName": "Jon Snow", "guarantorTaxId": "012.345.678-90", "guarantorAddress": "Av. Paulista, 200"},
            api_json(replacements),
        )

    def test_instance_is_kept_as_is(self):
        replacements = TemplateReplacements(guarantor_name="Jon Snow")
        self.assertIs(replacements, _parseResponseNote(replacements).template_replacements)

    def test_none_stays_none(self):
        self.assertIsNone(_parseResponseNote(None).template_replacements)

    def test_key_named_self_is_accepted(self):
        replacements = TemplateReplacements(**{"self": "x"})
        self.assertEqual({"self": "x"}, api_json(replacements))

    def test_leading_underscore_key_raises_value_error(self):
        with self.assertRaises(ValueError):
            TemplateReplacements(_hidden="x")
        with self.assertRaises(ValueError):
            _parseResponseNote({"_hidden": "x"})

    def test_invalid_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            _parseResponseNote(["guarantorName"])

    def test_positional_dict_is_accepted_like_the_other_sdks(self):
        replacements = TemplateReplacements({"guarantorName": "Jon Snow", "guarantor_tax_id": "1"})
        self.assertEqual({"guarantorName": "Jon Snow", "guarantorTaxId": "1"}, api_json(replacements))

    def test_positional_dict_and_keywords_are_merged_with_keywords_winning(self):
        replacements = TemplateReplacements({"guarantorName": "Jon Snow", "city": "A"}, city="B")
        self.assertEqual({"guarantorName": "Jon Snow", "city": "B"}, api_json(replacements))

    def test_positional_value_that_is_not_a_dict_raises_type_error(self):
        with self.assertRaises(TypeError):
            TemplateReplacements(["guarantorName"])
        with self.assertRaises(TypeError):
            TemplateReplacements({"a": "1"}, {"b": "2"})

    def test_leading_underscore_key_in_positional_dict_raises_value_error(self):
        with self.assertRaises(ValueError):
            TemplateReplacements({"_hidden": "x"})

    def test_api_response_path_keeps_every_key(self):
        note = from_api_json(_creditNoteResource, {
            "templateId": "1",
            "name": "Jon Snow",
            "taxId": "012.345.678-90",
            "scheduled": "2030-01-01",
            "invoices": [],
            "payment": {"bankCode": "1", "branchCode": "1", "accountNumber": "1", "name": "Jon Snow", "taxId": "012.345.678-90"},
            "signers": [],
            "externalId": "x",
            "streetLine1": "a", "streetLine2": "b", "district": "c", "city": "d", "stateCode": "SP", "zipCode": "1",
            "templateReplacements": {"guarantorName": "X", "someKeyNobodyDeclared": "Y"},
        })
        self.assertIsInstance(note.template_replacements, TemplateReplacements)
        self.assertEqual("X", note.template_replacements.guarantorName)
        self.assertEqual("Y", note.template_replacements.someKeyNobodyDeclared)


def _parseResponseNote(templateReplacements):
    return starkinfra.CreditNote(
        template_id="1",
        name="Jon Snow",
        tax_id="012.345.678-90",
        scheduled=date(2030, 1, 1),
        invoices=[],
        payment=starkinfra.creditnote.Transfer(
            bank_code="1", branch_code="1", account_number="1", name="Jon Snow", tax_id="012.345.678-90"
        ),
        signers=[],
        external_id="x",
        street_line_1="a", street_line_2="b", district="c", city="d", state_code="SP", zip_code="1",
        template_replacements=templateReplacements,
    )


class TestCreditNotePdf(TestCase):

    def test_success(self):
        pdf = starkinfra.creditnote.pdf(os.environ["SANDBOX_SIGNED_CREDIT_NOTE_ID"])
        stringified_pdf = pdf[:4].decode('utf-8')
        self.assertEqual(stringified_pdf, '%PDF')


class TestCreditNotePdfReceipt(TestCase):

    def test_success(self):
        pdf = starkinfra.creditnote.payment(os.environ["SANDBOX_SIGNED_CREDIT_NOTE_ID"])
        stringified_pdf = pdf[:4].decode('utf-8')
        self.assertEqual(stringified_pdf, '%PDF')


class TestCreditNoteQuery(TestCase):

    def test_success_after_before(self):
        notes = list(starkinfra.creditnote.query(limit=1))
        for note in notes:
            print(note)
        print("Number of credit notes:", len(notes))


class TestCreditNotePage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            notes, cursor = starkinfra.creditnote.page(limit=2, cursor=cursor)
            for note in notes:
                print(note)
                self.assertFalse(note.id in ids)
                ids.append(note.id)
            if cursor is None:
                break
        self.assertTrue(len(ids) == 4)


class TestCreditNoteInfoGet(TestCase):

    def test_success(self):
        notes = starkinfra.creditnote.query(limit=10)
        for note in notes:
            note_id = note.id
            note = starkinfra.creditnote.get(note_id)
            self.assertEqual(note.id, note_id)


class TestCreditNotePostAndCancel(TestCase):
    
    def test_success(self):
        notes = generateExampleCreditNoteJson(n=1)
        notes = starkinfra.creditnote.create(notes)
        note_id = notes[0].id
        note = starkinfra.creditnote.cancel(id=note_id)
        print(note.id)


if __name__ == '__main__':
    main()
