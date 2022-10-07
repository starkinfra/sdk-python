import starkinfra
from unittest import TestCase, main
from tests.utils.user import exampleProject

starkinfra.user = exampleProject


class TestMerchantCategoryQuery(TestCase):

    def test_success(self):
        categories = starkinfra.merchantcategory.query()
        for category in categories:
            print(category)
            self.assertIsNotNone(category.type)


if __name__ == '__main__':
    main()
