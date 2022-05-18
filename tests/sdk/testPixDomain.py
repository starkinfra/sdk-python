import starkinfra
from unittest import TestCase, main
from tests.utils.user import exampleProject


starkinfra.user = exampleProject


class TestPixDomainQuery(TestCase):

    def test_success(self):
        pixDomains = starkinfra.pixdomain.query()
        for domain in pixDomains:
            print(domain)
            self.assertIsNotNone(domain.name)


if __name__ == '__main__':
    main()
