import starkinfra
from random import shuffle
from unittest import TestCase, main
from tests.utils.user import exampleProject


starkinfra.user = exampleProject


class TestBrcodePreview(TestCase):
    def test_success(self):
        static_brcodes = list(starkinfra.staticbrcode.query(limit=10))
        shuffle(static_brcodes)

        dynamic_brcodes = list(starkinfra.dynamicbrcode.query(limit=10))
        shuffle(dynamic_brcodes)

        brcodes = static_brcodes + dynamic_brcodes

        previews = starkinfra.brcodepreview.create([
            starkinfra.BrcodePreview(
                id=brcodes[0].id
            ),
            starkinfra.BrcodePreview(
                id=brcodes[1].id
            ),
        ])

        self.assertTrue(len(previews) == 2)

        index = 0
        for preview in previews:
            self.assertEqual(str(preview.id), str(brcodes[index].id))
            print(preview)
            index = index + 1


if __name__ == '__main__':
    main()
