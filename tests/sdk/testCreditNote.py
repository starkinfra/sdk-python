import starkinfra
from unittest import TestCase, main
from tests.utils.user import exampleProject
from tests.utils.creditNote import generateExampleCreditNoteJson


starkinfra.user = exampleProject


class TestCreditNotePost(TestCase):

    def test_success(self):
        notes = generateExampleCreditNoteJson(n=1)
        notes = starkinfra.creditnote.create(notes)
        for note in notes:
            self.assertIsNotNone(note.id)


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
