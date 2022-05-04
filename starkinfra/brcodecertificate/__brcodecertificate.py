from ..utils import rest
from starkcore.utils.subresource import SubResource


class BrcodeCertificate(SubResource):
    """# BrcodeCertificate object
    The BrcodeCertificate object displays the certificate information of registered SPI participants able
    to issue dynamic QR Codes.
    They are used in the validation of the URLs contained in the dynamic QR Codes.
    ## Attributes (return-only):
    - content [string]: certificate of the SPI participant in PEM format.
    - domain [string]: current active domain (URL) of the SPI participant.
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
