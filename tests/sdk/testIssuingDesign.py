import starkinfra
from unittest import TestCase, main
from tests.utils.user import exampleProject

starkinfra.user = exampleProject


class TestIssuingDesignQuery(TestCase):

    def test_success(self):
        designs = starkinfra.issuingdesign.query()
        for design in designs:
            self.assertEqual(design.id, str(design.id))


class TestIssuingDesignPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            designs, cursor = starkinfra.issuingdesign.page(
                limit=2,
                cursor=cursor
            )
            for design in designs:
                self.assertFalse(design.id in ids)
                ids.append(design.id)
            if cursor is None:
                break


class TestIssuingDesignGet(TestCase):

    def test_success(self):
        designs = starkinfra.issuingdesign.query(limit=1)
        design = starkinfra.issuingdesign.get(id=next(designs).id)
        self.assertEqual(design.id, str(design.id))


class TestDesignPdfGet(TestCase):

    def test_success(self):
        designs = starkinfra.issuingdesign.query()
        design_id = next(designs).id
        pdf = starkinfra.issuingdesign.pdf(design_id)
        self.assertGreater(len(pdf), 1000)


if __name__ == '__main__':
    main()
