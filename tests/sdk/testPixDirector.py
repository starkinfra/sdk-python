import starkinfra
from random import randint
from starkinfra import PixDirector
from unittest import TestCase, main
from tests.utils.user import exampleProject
from tests.utils.names.names import get_full_name
from tests.utils.taxIdGenerator import TaxIdGenerator


starkinfra.user = exampleProject


class TestPixDirectorPost(TestCase):

    def test_success(self):
        pix_director = PixDirector(
            name=get_full_name(),
            tax_id=TaxIdGenerator.taxId(),
            phone="+5511"+str(randint(100000000, 999999999)),
            email=(get_full_name()+"@gmail.com").replace(" ", ""),
            password=str(randint(10000000, 99999999)),
            team_email=(get_full_name()+"@gmail.com").replace(" ", ""),
            team_phones=["+5511"+str(randint(100000000, 999999999)), "+5511"+str(randint(100000000, 999999999))],
        )
        print(pix_director)
        created_pix_director = starkinfra.pixdirector.create(pix_director)
        print(pix_director)
        self.assertEqual(created_pix_director.name, pix_director.name)
        self.assertEqual(created_pix_director.phone, pix_director.phone)
        self.assertEqual(created_pix_director.tax_id, pix_director.tax_id)


if __name__ == '__main__':
    main()
