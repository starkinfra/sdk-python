from random import randint
from unittest import TestCase, main
from tests.utils.user import exampleProject
from tests.utils.creditNotePreview import getPreviewExamples
import starkinfra

starkinfra.user = exampleProject


class TestCreditNotePreviewSac(TestCase):

    def test_success(self):
        previews = getPreviewExamples(n=randint(1, 12), type="sac")
        previews = starkinfra.creditnotepreview.create(previews)

        for preview in previews:
            self.assertTrue(len(preview.invoices) == preview.count)
            self.assertEqual("sac", preview.type)


class TestCreditNotePreviewPrice(TestCase):
    
    def test_success(self):
        previews = getPreviewExamples(n=randint(1, 12), type="price")
        previews = starkinfra.creditnotepreview.create(previews)

        for preview in previews:
            self.assertTrue(len(preview.invoices) == preview.count)
            self.assertEqual("price", preview.type)


class TestCreditNotePreviewAmerican(TestCase):

    def test_success(self):
        previews = getPreviewExamples(n=randint(1, 12), type="american")
        previews = starkinfra.creditnotepreview.create(previews)

        for preview in previews:
            self.assertTrue(len(preview.invoices) == preview.count)
            self.assertEqual("american", preview.type)


class TestCreditNotePreviewBullet(TestCase):

    def test_success(self):
        previews = getPreviewExamples(n=randint(1, 12), type="bullet")
        previews = starkinfra.creditnotepreview.create(previews)

        for preview in previews:
            self.assertTrue(len(preview.invoices) == preview.count)
            self.assertEqual("bullet", preview.type)


if __name__ == '__main__':
    main()
