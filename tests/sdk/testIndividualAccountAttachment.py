import starkinfra
from datetime import datetime, date, timedelta
from unittest import TestCase, main
from tests.utils.user import exampleProject
from tests.utils.individualDocument import readImage, RgImages
from tests.utils.individualAccountRequest import generateExampleIndividualAccountRequestJson
from tests.utils.individualAccountAttachment import generateExampleIndividualAccountAttachmentJson


starkinfra.user = exampleProject


def _create_parent_request_id():
    requests = list(starkinfra.individualaccountrequest.query(limit=1))
    if requests:
        return requests[0].id
    requests = starkinfra.individualaccountrequest.create(
        generateExampleIndividualAccountRequestJson(n=1)
    )
    return requests[0].id


def _create_fresh_parent_request_id():
    requests = starkinfra.individualaccountrequest.create(
        generateExampleIndividualAccountRequestJson(n=1)
    )
    return requests[0].id


class TestIndividualAccountAttachmentPost(TestCase):

    def test_success(self):
        account_request_id = _create_parent_request_id()
        attachments = starkinfra.individualaccountattachment.create(
            generateExampleIndividualAccountAttachmentJson(account_request_id, n=1)
        )
        for attachment in attachments:
            self.assertIsNotNone(attachment.id)
            self.assertIsNotNone(attachment.status)


class TestIndividualAccountAttachmentContentEncoding(TestCase):

    def test_success_content_data_url(self):
        attachment = starkinfra.IndividualAccountAttachment(
            content=readImage(RgImages["front"]),
            content_type="image/png",
            type="identity-front",
            account_request_id="5189530608992256",
        )
        self.assertTrue(attachment.content.startswith("data:image/png;base64,"))

    def test_success_content_type_input_only(self):
        attachment = starkinfra.IndividualAccountAttachment(
            content=readImage(RgImages["front"]),
            content_type="image/png",
            type="identity-front",
            account_request_id="5189530608992256",
        )
        self.assertIsNone(attachment.content_type)


class TestIndividualAccountAttachmentExposure(TestCase):

    def test_exposed_under_new_name(self):
        self.assertTrue(hasattr(starkinfra, "individualaccountattachment"))
        self.assertTrue(hasattr(starkinfra, "IndividualAccountAttachment"))
        self.assertFalse(hasattr(starkinfra, "accountrequestattachment"))
        self.assertFalse(hasattr(starkinfra, "AccountRequestAttachment"))


class TestIndividualAccountAttachmentTypeEnum(TestCase):

    def test_type_enum(self):
        for type_value in [
            "drivers-license-front",
            "drivers-license-back",
            "identity-front",
            "identity-back",
        ]:
            attachment = starkinfra.IndividualAccountAttachment(
                content=readImage(RgImages["front"]),
                content_type="image/png",
                type=type_value,
                account_request_id="5189530608992256",
            )
            self.assertEqual(attachment.type, type_value)


class TestIndividualAccountAttachmentQuery(TestCase):

    def test_success(self):
        attachments = list(starkinfra.individualaccountattachment.query(limit=10))
        for attachment in attachments:
            self.assertIsNotNone(attachment.id)

    def test_success_with_params(self):
        attachments = starkinfra.individualaccountattachment.query(
            limit=10,
            after=date.today() - timedelta(days=100),
            before=date.today(),
            status="created",
            tags=["a", "b"],
            ids=["1", "2", "3"],
        )
        self.assertEqual(len(list(attachments)), 0)


class TestIndividualAccountAttachmentPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            attachments, cursor = starkinfra.individualaccountattachment.page(limit=2, cursor=cursor)
            for attachment in attachments:
                self.assertFalse(attachment.id in ids)
                ids.append(attachment.id)
            if cursor is None:
                break
        self.assertTrue(len(ids) == 4)


class TestIndividualAccountAttachmentGet(TestCase):

    def test_success(self):
        attachments = starkinfra.individualaccountattachment.query(limit=1)
        attachment_id = next(attachments).id
        attachment = starkinfra.individualaccountattachment.get(id=attachment_id)
        self.assertIsNotNone(attachment.id)
        self.assertEqual(attachment.id, attachment_id)

    def test_success_datetime_parsed(self):
        attachments = starkinfra.individualaccountattachment.query(limit=1)
        attachment = starkinfra.individualaccountattachment.get(id=next(attachments).id)
        self.assertIsInstance(attachment.created, datetime)


class TestIndividualAccountAttachmentPostAndCancel(TestCase):

    def test_success(self):
        account_request_id = _create_fresh_parent_request_id()
        attachments = starkinfra.individualaccountattachment.create(
            generateExampleIndividualAccountAttachmentJson(account_request_id, n=1)
        )
        attachment_id = attachments[0].id
        attachment = starkinfra.individualaccountattachment.cancel(id=attachment_id)
        self.assertEqual(attachment.id, attachment_id)
        self.assertEqual(attachment.status, "deleted")

    def test_success_idempotent_double_cancel(self):
        account_request_id = _create_fresh_parent_request_id()
        attachments = starkinfra.individualaccountattachment.create(
            generateExampleIndividualAccountAttachmentJson(account_request_id, n=1)
        )
        attachment_id = attachments[0].id
        first = starkinfra.individualaccountattachment.cancel(id=attachment_id)
        self.assertEqual(first.status, "deleted")
        second = starkinfra.individualaccountattachment.cancel(id=attachment_id)
        self.assertEqual(second.status, "deleted")


class TestIndividualAccountAttachmentInvalid(TestCase):

    def test_invalid_type(self):
        account_request_id = _create_fresh_parent_request_id()
        attachments = [starkinfra.IndividualAccountAttachment(
            content=readImage(RgImages["front"]),
            content_type="image/png",
            type="not-a-real-type",
            account_request_id=account_request_id,
        )]
        with self.assertRaises(starkinfra.error.InputErrors):
            starkinfra.individualaccountattachment.create(attachments)

    def test_invalid_content(self):
        account_request_id = _create_fresh_parent_request_id()
        attachments = [starkinfra.IndividualAccountAttachment(
            content="",
            content_type="image/png",
            type="identity-front",
            account_request_id=account_request_id,
        )]
        with self.assertRaises(starkinfra.error.InputErrors):
            starkinfra.individualaccountattachment.create(attachments)

    def test_invalid_file_type(self):
        account_request_id = _create_fresh_parent_request_id()
        attachments = [starkinfra.IndividualAccountAttachment(
            content=readImage(RgImages["front"]),
            content_type=None,
            type="identity-front",
            account_request_id=account_request_id,
        )]
        with self.assertRaises(starkinfra.error.InputErrors):
            starkinfra.individualaccountattachment.create(attachments)

    def test_invalid_account_request_id(self):
        attachments = [starkinfra.IndividualAccountAttachment(
            content=readImage(RgImages["front"]),
            content_type="image/png",
            type="identity-front",
            account_request_id="0",
        )]
        with self.assertRaises(starkinfra.error.InputErrors):
            starkinfra.individualaccountattachment.create(attachments)

    def test_unknown_id(self):
        with self.assertRaises(starkinfra.error.InputErrors):
            starkinfra.individualaccountattachment.get("0")


if __name__ == '__main__':
    main()
