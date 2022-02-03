from ..utils import rest
from ..utils.resource import Resource
from ..utils.checks import check_datetime


class IndirectParticipant(Resource):
    """# IndirectParticipant object
    When you initialize a IndirectParticipant object, the entity will not be automatically
    created in the Stark Infra API. The 'create' function sends the objects
    to the Stark Infra API and returns the list of created objects.
    ## Parameters (Required):
    - request_url [string]: IndirectParticipant request url.
    - rsfn_url [string]: IndirectParticipant rsfn url.
    - tax_id [string]: IndirectParticipant tax ID (CPF or CNPJ). ex: "012.345.678-90" or "20.018.183/0001-80"
    - workspace_id [string]:  ID of the Workspace of the IndirectParticipant. ex: "4545454545454545"
    ## Parameters (Optional):
    - bank_code []: indirect participant's bank code. ex: "00000000"
    - direct_id []: direct participant id.
    - organization_id []: indirect participant's organization id.
    ## Attributes (return-only):
    - id [string, default None]: unique ID returned when the IndirectParticipant is created. ex: "5656565656565656"
    - status [string]: current IndirectParticipant status. ex:
    - created [datetime.datetime, default None]: creation datetime for the IndirectParticipant. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - updated [datetime.datetime, default None]: latest update datetime for the IndirectParticipant. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, request_url, rsfn_url, tax_id, workspace_id, id=None, bank_code=None,
                 status=None, direct_id=None, organization_id=None, created=None, updated=None):
        Resource.__init__(self, id=id)

        self.request_url = request_url
        self.rsfn_url = rsfn_url
        self.tax_id = tax_id
        self.workspace_id = workspace_id
        self.bank_code = bank_code
        self.status = status
        self.direct_id = direct_id
        self.organization_id = organization_id
        self.created = check_datetime(created)
        self.updated = check_datetime(updated)


_resource = {"class": IndirectParticipant, "name": "IndirectParticipant"}


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
