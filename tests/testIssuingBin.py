import starkinfra
from unittest import TestCase, main
from tests.utils.user import exampleProject


starkinfra.user = exampleProject


class TestIssuingBinQuery(TestCase):

    def test_success(self):
        bins = starkinfra.issuingbin.query()
        for bin in bins:
            self.assertIsInstance(bin.id, str)


class TestIssuingBinPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            bins, cursor = starkinfra.issuingbin.page(limit=2, cursor=cursor)
            for bin in bins:
                self.assertFalse(bin.id in ids)
                ids.append(bin.id)
            if cursor is None:
                break


if __name__ == '__main__':
    main()
