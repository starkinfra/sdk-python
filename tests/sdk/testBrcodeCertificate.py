import starkinfra
from unittest import TestCase, main
from tests.utils.user import exampleProject


starkinfra.user = exampleProject


class TestBrcodeCertificateQuery(TestCase):

    def test_success(self):
        brcodeCertificates = starkinfra.brcodecertificate.query()
        for certificate in brcodeCertificates:
            self.assertEqual(certificate.content, str(certificate.content))


if __name__ == '__main__':
    main()
