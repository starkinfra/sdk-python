import starkinfra
from unittest import TestCase, main
from tests.utils.user import exampleProject

starkinfra.user = exampleProject


class TestCardMethodQuery(TestCase):

    def test_success(self):
        methods = starkinfra.cardmethod.query(
            search="token"
        )
        for method in methods:
            self.assertIsNotNone(method.code)


if __name__ == '__main__':
    main()
