import starkinfra
from unittest import TestCase, main
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

            res = starkinfra.creditsigner.resend_token_one_signer(signer.id)
            self.assertIsInstance(res, CreditSigner)


if __name__ == '__main__':
    main()
