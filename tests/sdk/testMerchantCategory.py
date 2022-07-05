import starkinfra
from unittest import TestCase, main
from datetime import date, timedelta
from starkinfra import IssuingWithdrawal
from tests.utils.user import exampleProject
from tests.utils.withdrawal import generateExampleWithdrawalJson

starkinfra.user = exampleProject


class TestMerchantCategoryQuery(TestCase):

    def test_success(self):
        categories = starkinfra.merchantcategory.query(
            search="food"
        )
        for category in categories:
            self.assertIsNotNone(category.type)


if __name__ == '__main__':
    main()
