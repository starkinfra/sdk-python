import starkinfra
from unittest import TestCase, main
from tests.utils.user import exampleProject


starkinfra.user = exampleProject


class TestBusinessAttachmentPost(TestCase):

    def test_success(self):
        identities = list(starkinfra.businessidentity.query(status="pending", limit=1))
        self.assertTrue(len(identities) > 0)
        attachments = starkinfra.businessattachment.create([
            starkinfra.BusinessAttachment(
                business_identity_id=identities[0].id,
                name="articles-of-incorporation.png",
                content="iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==",
                content_type="image/png",
            )
        ])
        for attachment in attachments:
            self.assertIsNotNone(attachment.id)


class TestBusinessAttachmentQuery(TestCase):

    def test_success(self):
        attachments = list(starkinfra.businessattachment.query(limit=1))
        for attachment in attachments:
            self.assertIsNotNone(attachment.id)


class TestBusinessAttachmentPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            attachments, cursor = starkinfra.businessattachment.page(limit=2, cursor=cursor)
            for attachment in attachments:
                self.assertFalse(attachment.id in ids)
                ids.append(attachment.id)
            if cursor is None:
                break
        self.assertEqual(len(ids), 4)


class TestBusinessAttachmentInfoGet(TestCase):

    def test_success(self):
        attachments = starkinfra.businessattachment.query(limit=3)
        for attachment in attachments:
            attachment_id = attachment.id
            attachment_new = starkinfra.businessattachment.get(attachment_id, expand=["content"])
            self.assertEqual(attachment_new.id, attachment_id)


class TestBusinessAttachmentCancel(TestCase):

    def test_success(self):
        identities = list(starkinfra.businessidentity.query(status="pending", limit=1))
        self.assertTrue(len(identities) > 0)
        attachments = starkinfra.businessattachment.create([
            starkinfra.BusinessAttachment(
                business_identity_id=identities[0].id,
                name="cancel-test.png",
                content="iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==",
                content_type="image/png",
            )
        ])
        attachment_id = attachments[0].id
        attachment = starkinfra.businessattachment.cancel(id=attachment_id)
        self.assertEqual(attachment.id, attachment_id)


if __name__ == '__main__':
    main()
