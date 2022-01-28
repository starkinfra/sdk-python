from ..utils import rest
from ..utils.resource import Resource


class IndirectParticipant(Resource):
    """# IndirectParticipant object
    When you initialize a IndirectParticipant object, the entity will not be automatically
    created in the Stark Infra API. The 'create' function sends the objects
    to the Stark Infra API and returns the list of created objects.
    ## Attributes (return-only):
    - request_url [string]: indirect participant url used for reqeusts
    - rsfn_url [string]: indirect participant rsfn url
    - tax_id [string]: indirect participant tax ID (CPF or CNPJ). ex: "012.345.678-90" or "20.018.183/0001-80"
    - workspace_id [string]:  ID of the Workspace of the indirect participant. ex: "4545454545454545"
    """

    def __init__(self, request_url, rsfn_url, tax_id, workspace_id):
        Resource.__init__(self, id=id)

        self.request_url = request_url
        self.rsfn_url = rsfn_url
        self.tax_id = tax_id
        self.workspace_id = workspace_id


_resource = {"class": IndirectParticipant, "name": "IndirectParticipant"}


def get(id, user=None):
    """# Retrieve the IndirectParticipant object by its id
    Receive a IndirectParticipant object linked to your workspace in the Stark Infra API
    ## Parameters (optional):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - IndirectParticipant object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)


def create(participants, user=None):
    """# Create Indirect Participants at the StarkInfra API
     ## Parameters (required):
    - participants [list of IndirectParticipant objects]: list of IndirectParticipant objects to be created in the API
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - IndirectParticipant object with updated attributes
    """
    return rest.post_multi(resource=_resource, entities=participants,  user=user)
