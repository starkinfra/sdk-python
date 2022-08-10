import starkinfra
from unittest import TestCase, main
from tests.utils.user import exampleProject
from tests.utils.creditNotePreview import getCreditNotePreviewExample

starkinfra.user = exampleProject


class TestCreditNotePreviewSac(TestCase):

    def test_success(self):
        creditNoteSac = getCreditNotePreviewExample(type="sac")
        creditNotePrice = getCreditNotePreviewExample(type="price")
        creditNoteAmerican = getCreditNotePreviewExample(type="american")
        creditNoteBullet = getCreditNotePreviewExample(type="bullet")

        expectedTypes = ["credit-note", "credit-note", "credit-note", "credit-note"]
        expectedNoteTypes = ["sac", "price", "american", "bullet"]
        creditNotePreviews = [
            starkinfra.CreditPreview(type="credit-note", credit=creditNoteSac),
            starkinfra.CreditPreview(type="credit-note", credit=creditNotePrice),
            starkinfra.CreditPreview(type="credit-note", credit=creditNoteAmerican),
            starkinfra.CreditPreview(type="credit-note", credit=creditNoteBullet),
        ]

        previewedTypes = []
        creditNotePreviewedTypes = []
        for preview in starkinfra.creditpreview.create(previews=creditNotePreviews):
            previewedTypes.append(preview.type)
            creditNotePreviewedTypes.append(preview.credit.type)
        self.assertEqual(expectedNoteTypes, creditNotePreviewedTypes)
        self.assertEqual(previewedTypes, expectedTypes)

if __name__ == '__main__':
    main()
