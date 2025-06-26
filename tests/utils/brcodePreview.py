import starkinfra
from starkinfra import BrcodePreview

def create_brcode_preview_by_id(id):
    previews = starkinfra.brcodepreview.create([
        starkinfra.BrcodePreview(
            id=id,
            payer_id="20018183000180"
        )
    ])
    return previews[0]
