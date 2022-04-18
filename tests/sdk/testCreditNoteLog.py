import starkinfra
from unittest import TestCase, main
from tests.utils.user import exampleProject


starkinfra.user = exampleProject


class TestCreditNoteLogQuery(TestCase):

    def test_success(self):
        logs = list(starkinfra.creditnote.log.query(limit=100))
        logs = list(starkinfra.creditnote.log.query(limit=100, note_ids={log.note.id for log in logs}, types={log.type for log in logs}))
        print("Number of logs:", len(logs))


class TestCreditNoteLogPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            logs, cursor = starkinfra.creditnote.log.page(limit=2, cursor=cursor)
            for log in logs:
                print(log)
                self.assertFalse(log.id in ids)
                ids.append(log.id)
            if cursor is None:
                break
        self.assertTrue(len(ids) == 4)


class TestCreditNoteLogInfoGet(TestCase):
    def test_success(self):
        logs = starkinfra.creditnote.log.query()
        log_id = next(logs).id
        log = starkinfra.creditnote.log.get(id=log_id)
        self.assertEqual(log.id, log_id)


class TestCreditNoteLogFromCreditNoteId(TestCase):
    def test_success(self):
        note = starkinfra.creditnote.query(limit=1)
        note_id = next(note).id
        logs = starkinfra.creditnote.log.query(note_ids=note_id)
        for log in logs:
            print(log)


if __name__ == '__main__':
    main()
