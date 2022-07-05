import starkinfra
from unittest import TestCase, main
from tests.utils.user import exampleProject

starkinfra.user = exampleProject


class TestMerchantCountryQuery(TestCase):

    def test_success(self):
        countries = starkinfra.merchantcountry.query(
            search="brazil"
        )
        for country in countries:
            self.assertIsNotNone(country.code)


if __name__ == '__main__':
    main()
