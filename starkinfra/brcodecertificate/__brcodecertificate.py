from ..utils import rest
from starkcore.utils.subresource import SubResource


class BrcodeCertificate(SubResource):
    """# BrcodeCertificate object
    The BrcodeCertificate object displays the QR Code domain certificate information of Pix participants.
    All certificates must be registered with the Central Bank.
    ## Attributes (return-only):
    - content [string]: certificate of the Pix participant in PEM format.
    - domain [string]: current active domain (URL) of the Pix participant.
    """

    def __init__(self, content=None, domain=None):
        self.content = content
        self.domain = domain


_resource = {"class": BrcodeCertificate, "name": "BrcodeCertificate"}


def query(user=None):
    """# Retrieve BrcodeCertificates
    Receive a generator of BrcodeCertificate objects.
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - generator of BrcodeCertificate objects with updated attributes
    """
    return rest.get_stream(resource=_resource, user=user)
