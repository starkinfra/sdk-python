import starkinfra
from unittest import TestCase, main
from tests.utils.user import exampleProject

starkinfra.user = exampleProject


class TestIssuingTokenDesignQuery(TestCase):

    def test_success(self):
        designs = starkinfra.issuingtokendesign.query(limit=5)
        for design in designs:
            self.assertEqual(design.id, str(design.id))


class TestIssuingTokenDesignPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            designs, cursor = starkinfra.issuingtokendesign.page(limit=2, cursor=cursor)
            for design in designs:
                self.assertEqual(design.id, str(design.id))
            if cursor is None:
                break


class TestIssuingTokenDesignGet(TestCase):

    def test_success(self):
        designs = starkinfra.issuingtokendesign.query(limit=1)
        for design in designs:
            design = starkinfra.issuingtokendesign.get(design.id)
            self.assertEqual(design.id, str(design.id))


class TestIssuingTokenDesignPdf(TestCase):

    def test_success(self):
        designs = starkinfra.issuingtokendesign.query(limit=1)
        for design in designs:
            design = starkinfra.issuingtokendesign.pdf(design.id)
            self.assertGreater(len(design), 1000)


if __name__ == '__main__':
    main()
