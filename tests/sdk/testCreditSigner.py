from unittest import TestCase, main
import starkinfra
from starkinfra.creditsigner.__creditsigner import CreditSigner
from tests.utils.creditNote import generateExampleCreditNoteJson
from tests.utils.user import exampleProject


starkinfra.user = exampleProject


class TestCreditSignerResendToken(TestCase):

    def test_success(self):

        request = generateExampleCreditNoteJson(n=1)
        notes = starkinfra.creditnote.create(request)
        for note in notes:
            self.assertGreater(len(note.signers), 0)
            signer = next(
                (s for s in note.signers if not s.name.lower().strip().startswith("stark")),
                None
            )
            if not signer:
                self.fail("No signer found")

            res = starkinfra.creditsigner.resend_token(signer.id)
            self.assertIsInstance(res, CreditSigner)
    
    def test_signer_not_found(self):
        with self.assertRaises(starkinfra.error.InputErrors):
            starkinfra.creditsigner.resend_token("000")

if __name__ == '__main__':
    main()
