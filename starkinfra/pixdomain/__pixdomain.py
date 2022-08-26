from ..utils import rest
from .__certificate import _resource as _certificate_resource
from starkcore.utils.api import from_api_json
from starkcore.utils.subresource import SubResource


class PixDomain(SubResource):
    """# PixDomain object
    The PixDomain object displays the domain name and the QR Code domain certificate of Pix participants.
    All certificates must be registered with the Central Bank.
    ## Attributes (return-only):
    - certificates [list of pixdomain.Certificate]: certificate information of the Pix participant.
    - name [string]: current active domain (URL) of the Pix participant.
    """

    def __init__(self, certificates=None, name=None):
        self.certificates = _parse_certificates(certificates)
        self.name = name


def _parse_certificates(certificates):
    return [from_api_json(_certificate_resource, certificate) for certificate in certificates]


_resource = {"class": PixDomain, "name": "PixDomain"}


def query(user=None):
    """# Retrieve PixDomains
    Receive a generator of PixDomain objects.
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - generator of PixDomain objects with updated attributes
    """
    return rest.get_stream(resource=_resource, user=user)
