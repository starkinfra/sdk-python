from ..utils import rest
from ..utils.resource import Resource


class BrcodeCertificate(Resource):
    """# BrcodeCertificate object
    The BrcodeCertificate object
    ## Attributes (return-only):
    """

    def __init__(self, id=None):
        Resource.__init__(self, id=id)


_resource = {"class": BrcodeCertificate, "name": "BrcodeCertificate"}


def get(user=None):
    """# Retrieve all the the BrcodeCertificate objects
    Receive all the the BrcodeCertificate objects linked to your workspace in the Stark Infra API
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - BrcodeCertificate objects
    """
    return next(rest.get_stream(resource=_resource, user=user))
