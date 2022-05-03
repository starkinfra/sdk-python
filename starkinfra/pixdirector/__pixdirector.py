from ..utils import rest
from starkcore.utils.resource import Resource


class PixDirector(Resource):
    """# PixDirector object
    Mandatory data that must be registered within the Central Bank for emergency contact purposes.
    When you initialize a PixDirector, the entity will not be automatically
    created in the Stark Infra API. The 'create' function sends the objects
    to the Stark Infra API and returns the list of created objects.
    ## Parameters (required):
    - name [string]: name of the PixDirector. ex: "Edward Stark".
    - tax_id [string]: tax ID (CPF/CNPJ) of the PixDirector. ex: "03.300.300/0001-00"
    - phone [string]: phone of the PixDirector. ex: "+55-1198989898"
    - email [string]: email of the PixDirector. ex: "ned.stark@starkbank.com"
    - password [string]: password of the PixDirector. ex: "12345678"
    - team_email [string]: team email. ex: "pix.team@company.com"
    - team_phones [list of strings]: list of phones of the team. ex: ["+55-11988889999", "+55-11988889998"]
    ## Attributes (return-only):
    - id [string, default None]: unique id returned when the PixDirector is created. ex: "5656565656565656"
    - status [string, default None]: current PixDirector status. ex: "success"
    """

    def __init__(self, name, tax_id, phone, email, password, team_email, team_phones, id=None, status=None):
        Resource.__init__(self, id=id)

        self.email = email
        self.name = name
        self.password = password
        self.phone = phone
        self.tax_id = tax_id
        self.team_email = team_email
        self.team_phones = team_phones
        self.status = status


_resource = {"class": PixDirector, "name": "PixDirector"}


def create(director, user=None):
    """# Create a PixDirector Object
    Send a PixDirector object for creation in the Stark Infra API
    ## Parameters (required):
    - director [list of PixDirector Object]: list of PixDirector objects to be created in the API
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - PixDirector objects with updated attributes
    """
    return rest.post_single(resource=_resource, entity=director, user=user)
