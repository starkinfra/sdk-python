import os
import starkinfra
from unittest import TestCase, main
from tests.utils.user import exampleProject
from tests.utils.creditNote import generateExampleCreditNoteIsoDatetimeJson, generateExampleCreditNoteJson, generateExampleCreditNoteStringDatesJson


starkinfra.user = exampleProject


class TestCreditNotePost(TestCase):

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
        

class TestCreditNotePdfReceipt(TestCase):

    def test_success(self):
        pdf = starkinfra.creditnote.pdf(os.environ["SANDBOX_SIGNED_CREDIT_NOTE_ID"])
        self.assertGreater(len(pdf), 1000)


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
