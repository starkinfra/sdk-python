import starkinfra
from unittest import TestCase, main
from tests.utils.user import exampleProject


starkinfra.user = exampleProject


class TestAccountRequestAttachmentPost(TestCase):

    def test_success(self):
        requests = list(starkinfra.individualaccountrequest.query(limit=1))
        self.assertTrue(len(requests) > 0)
        attachments = starkinfra.accountrequestattachment.create([
            starkinfra.AccountRequestAttachment(
                account_request_id=requests[0].id,
                type="identity-front",
                content="iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==",
                content_type="image/png",
            )
        ])
        for attachment in attachments:
            self.assertIsNotNone(attachment.id)


class TestAccountRequestAttachmentQuery(TestCase):

    def test_success(self):
        attachments = list(starkinfra.accountrequestattachment.query(limit=1))
        for attachment in attachments:
            print(attachment)
        print("Number of attachments:", len(attachments))


class TestAccountRequestAttachmentPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            attachments, cursor = starkinfra.accountrequestattachment.page(limit=2, cursor=cursor)
            for attachment in attachments:
                print(attachment)
                self.assertFalse(attachment.id in ids)
                ids.append(attachment.id)
            if cursor is None:
                break
        self.assertEqual(len(ids), 4)


class TestAccountRequestAttachmentInfoGet(TestCase):

    def test_success(self):
        attachments = starkinfra.accountrequestattachment.query(limit=3)
        for attachment in attachments:
            attachment_id = attachment.id
            attachment_new = starkinfra.accountrequestattachment.get(attachment_id)
            self.assertEqual(attachment_new.id, attachment_id)


if __name__ == '__main__':
    main()
