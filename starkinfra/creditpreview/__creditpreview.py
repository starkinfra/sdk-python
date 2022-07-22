from starkcore.utils.api import from_api_json
from starkcore.utils.subresource import SubResource
from ..utils import rest
from .__creditnotepreview import _sub_resource as _credit_note_preview_sub_resource

_sub_resource_by_type = {
    "credit-note": _credit_note_preview_sub_resource,
}


class CreditPreview(SubResource):

    """# CreditPreview object
    A CreditPreview is used to get information from a credit before taking it.
    This resource can be used to preview credit notes
    ## Parameters (required):
    - type [string]: Credit type. ex: "credit-note"
    - credit [CreditNotePreview]: Information preview of the informed Credit.
    """

    def __init__(self, type=None, credit=None):
        SubResource.__init__(self)

        self.type = type
        self.credit = credit
        if type in _sub_resource_by_type:
            self.credit = from_api_json(resource=_sub_resource_by_type[type], json=credit)

_resource = {"class": CreditPreview, "name": "CreditPreview"}


def create(previews, user=None):
    """# Create CreditPreviews
    Send a list of CreditPreviews objects for processing in the Stark Bank API
    ## Parameters (required):
    - previews [list of CreditPreviews objects]: list of CreditPreviews objects to be created in the API
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkbank.user was set before function call
    ## Return:
    - list of CreditPreviews objects with updated attributes
    """
    return rest.post_multi(resource=_resource, entities=previews, user=user)
