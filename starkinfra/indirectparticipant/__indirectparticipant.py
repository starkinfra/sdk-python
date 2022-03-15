from ..utils import rest
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime


class IndirectParticipant(Resource):
    """# IndirectParticipant object
    When you initialize an IndirectParticipant object, the entity will not be automatically
    created in the Stark Infra API. The 'create' function sends the objects
    to the Stark Infra API and returns the list of created objects.
    ## Parameters (Required):
    - tax_id [string]: indirectParticipant's tax ID (CPF or CNPJ) with or without formatting. ex: "01234567890" or "20.018.183/0001-80"
    - workspace_id [string]: indirectParticipant's workspace ID. ex: "4545454545454545"
    - request_url [string]: indirectParticipant's url to send PixRequest authorizations. ex: "https://requesthadler656565.com"
    ## Parameters (Optional):
    - reversal_url [string, default None]: indirectParticipant's url to send PixReversal authorizations. ex: "https://reversalhadler656565.com"
    ## Attributes (return-only):
    - id [string, default None]: unique ID returned when the IndirectParticipant is created. ex: "5656565656565656"
    - status [string, default None]: current IndirectParticipant status. ex: "processing", "processing"
    - created [datetime.datetime, default None]: creation datetime for the IndirectParticipant. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - updated [datetime.datetime, default None]: latest update datetime for the IndirectParticipant. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """
    def __init__(self, tax_id, workspace_id, request_url, reversal_url=None, id=None, status=None,
                 created=None, updated=None):
        Resource.__init__(self, id=id)

        self.tax_id = tax_id
        self.workspace_id = workspace_id
        self.request_url = request_url
        self.reversal_url = reversal_url
        self.status = status
        self.created = check_datetime(created)
        self.updated = check_datetime(updated)


_resource = {"class": IndirectParticipant, "name": "IndirectParticipant"}


def create(participants, user=None):
    """# Create IndirectParticipant at the StarkInfra API
     ## Parameters (required):
    - participants [list of IndirectParticipant objects]: list of IndirectParticipant objects to be created in the API
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - IndirectParticipant object with updated attributes
    """
    return rest.post_multi(resource=_resource, entities=participants,  user=user)


def get(id, user=None):
    """# Retrieve the IndirectParticipant object by its id
    Receive a IndirectParticipant object linked to your workspace in the Stark Infra API
    ## Parameters (optional):
    - id [string]: IndirectParticipant object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - IndirectParticipant object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id, user=user)
