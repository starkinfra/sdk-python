from starkcore.utils.api import from_api_json
from starkcore.utils.subresource import SubResource
from ..utils import rest
from .__creditnotepreview import _sub_resource as _credit_note_preview_sub_resource, CreditNotePreview


class CreditPreview(SubResource):
    """# CreditPreview object
    A CreditPreview is used to get information from a credit before taking it.
    This resource can be used to preview credit notes
    ## Parameters (required):
    - credit [CreditNotePreview]: Information preview of the informed credit.
    - type [string]: Credit type. ex: "credit-note"
    """

    def __init__(self, type=None, credit=None):
        self.credit, self.type = _parse_credit(credit=credit, type=type)


_sub_resource = {"class": CreditPreview, "name": "CreditPreview"}


def create(previews, user=None):
    """# Create CreditPreviews
    Send a list of CreditPreview objects for processing in the Stark Infra API
    ## Parameters (required):
    - previews [list of CreditPreview objects]: list of CreditPreview objects to be created in the API
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - list of CreditPreview objects with updated attributes
    """
    return rest.post_multi(resource=_sub_resource, entities=previews, user=user)


def _parse_credit(credit, type):
    if isinstance(credit, dict):
        try:
            return from_api_json(*({
                "credit-note": _credit_note_preview_sub_resource,
            }[type], credit)), type
        except KeyError:
            return credit, type

    if type:
        return credit, type

    if isinstance(credit, CreditNotePreview):
        return credit, "credit-note"

    raise Exception(
        "credit must be either "
        "a dictionary"
        ", a starkinfra.creditpreview.CreditNotePreview"
        ", but not a {}".format(type(credit))
    )
