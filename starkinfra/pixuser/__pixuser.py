from ..utils import rest
from starkcore.utils.resource import Resource


class PixUser(Resource):
    """# PixUser object
    Pix Users are used to get fraud statistics of a user.
    ## Parameters (required):
    - id [string]: user tax ID (CPF or CNPJ) with or without formatting. ex: "01234567890" or "20.018.183/0001-80"
    ## Attributes (return-only):
    - statistics [list of PixUser.Statistics, default []]: list of PixUser.Statistics objects. ex: [PixUser.Statistics(after="2023-11-06T18:57:08.325090+00:00", source="pix-key")]
    """

    def __init__(self, id, statistics=None):
        Resource.__init__(self, id=id)

        self.statistics = statistics


_resource = {"class": PixUser, "name": "PixUser"}


def get(id, key_id=None, user=None):
    """# Retrieve a PixUser object
    Receive a single PixUser object information by passing its taxId
    ## Parameters (required):
    - id [string]: user tax ID (CPF or CNPJ) with or without formatting. ex: "01234567890" or "20.018.183/0001-80"
    ## Parameters (optional):
    - key_id [string]: marked PixKey id. ex: "+5511989898989"
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - PixUser object that corresponds to the given id.
    """
    return rest.get_id(id=id, resource=_resource, key_id=key_id, user=user)
