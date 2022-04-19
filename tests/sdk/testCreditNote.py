import starkinfra
from datetime import datetime, timedelta
from unittest import TestCase, main
from tests.utils.creditNote import generateExampleCreditNoteJson
from tests.utils.date import randomPastDate
from tests.utils.user import exampleProject


starkinfra.user = exampleProject


class TestCreditNotePost(TestCase):

    def test_success(self):
        notes = generateExampleCreditNoteJson(n=1)
        notes = starkinfra.creditnote.create(notes)
        for note in notes:
            self.assertIsNotNone(note.id)
            print(note)


class TestCreditNoteQuery(TestCase):

    def test_success_after_before(self):
        after = randomPastDate(days=10)
        before = datetime.today()
        notes = starkinfra.creditnote.query(after=after, before=before)

        print("Number of credit notes:", sum(1 for _ in notes))


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


if __name__ == '__main__':
    main()
