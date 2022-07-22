from random import randint
from unittest import TestCase, main
from tests.utils.user import exampleProject
from tests.utils.creditNotePreview import getCreditNotePreviewExample
import starkinfra

starkinfra.user = exampleProject


class TestCreditNotePreviewSac(TestCase):

    def test_success(self):

        creditNoteSac = getCreditNotePreviewExample(type="sac")
        creditNotePrice = getCreditNotePreviewExample(type="price")
        creditNoteAmerican = getCreditNotePreviewExample(type="american")
        creditNoteBullet = getCreditNotePreviewExample(type="bullet")

        types = ["credit-note"]
        creditNoteTypes = ["sac", "price", "american", "bullet"]
        creditNotePreviews = [
            starkinfra.CreditPreview(type="credit-note", credit=creditNoteSac),
            starkinfra.CreditPreview(type="credit-note", credit=creditNotePrice),
            starkinfra.CreditPreview(type="credit-note", credit=creditNoteAmerican),
            starkinfra.CreditPreview(type="credit-note", credit=creditNoteBullet),
        ]

        previewedTypes = []
        creditNotePreviewedTypes = []
        for preview in starkinfra.creditpreview.create(previews=creditNotePreviews):
            print(preview)
            previewedTypes.append(preview.type)
            creditNotePreviewedTypes.append(preview.credit.type)
        self.assertEqual(creditNoteTypes, creditNotePreviewedTypes)
        self.assertEqual(previewedTypes, types)

if __name__ == '__main__':
    main()
