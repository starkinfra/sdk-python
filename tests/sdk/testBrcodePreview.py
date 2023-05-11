import starkinfra
from unittest import TestCase, main
from tests.utils.user import exampleProject


starkinfra.user = exampleProject


class TestBrcodePreview(TestCase):

    def test_success(self):
        static_brcodes = list(starkinfra.staticbrcode.query(limit=2))

        dynamic_brcodes = list(starkinfra.dynamicbrcode.query(limit=2))

        brcodes = static_brcodes + dynamic_brcodes

        previews = starkinfra.brcodepreview.create([
            starkinfra.BrcodePreview(
                id=brcodes[0].id,
                payer_id="012.345.678-90"
            ),
            starkinfra.BrcodePreview(
                id=brcodes[1].id,
                payer_id="012.345.678-90"
            ),
            starkinfra.BrcodePreview(
                id=brcodes[2].id,
                payer_id="012.345.678-90"
            ),
            starkinfra.BrcodePreview(
                id=brcodes[3].id,
                payer_id="012.345.678-90"
            )
        ])

        self.assertTrue(len(previews) == 4)

        index = 0
        for preview in previews:
            self.assertEqual(str(preview.id), str(brcodes[index].id))
            print(preview)
            index = index + 1


if __name__ == '__main__':
    main()
