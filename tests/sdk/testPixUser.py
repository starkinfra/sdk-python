import starkinfra
from unittest import TestCase, main
from tests.utils.user import exampleProject


starkinfra.user = exampleProject


class TestPixUserGet(TestCase):

    def test_success(self):
        pix_user_id = "01234567890"
        pix_user = starkinfra.pixuser.get(id=pix_user_id)
        print(pix_user)
        self.assertIsNotNone(pix_user.id)

