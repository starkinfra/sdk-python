from ..utils import rest
from ..utils.resource import Resource


class PixDirector(Resource):
    """# PixDirector object
    When you initialize a PixDirector, the entity will not be automatically
    created in the Stark Infra API. The 'create' function sends the objects
    to the Stark Infra API and returns the list of created objects.
    ## Parameters (required):
    - email [string]:
    - name [string]:
    - password [string]:
    - phone [string]:
    - tax_id [string]:
    - team_email [list of strings]:
    - team_phones [list of strings]:
    ## Attributes (return-only):
    - id [string, default None]: unique id returned when the PixDirector is created. ex: "5656565656565656"
    """

    def __init__(self, email, name, password, phone, tax_id, team_email, team_phones, id=None):
        Resource.__init__(self, id=id)

        self.email = email
        self.name = name
        self.password = password
        self.phone = phone
        self.tax_id = tax_id
        self.team_email = team_email
        self.team_phones = team_phones


_resource = {"class": PixDirector, "name": "PixDirector"}


def create(director, user=None):
    """# Create a PixDirector Object
    Send a list of PixDirector objects for creation in the Stark Infra API
    ## Parameters (required):
    - director [list of PixDirector Object]: list of PixDirector objects to be created in the API
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - PixDirector object with updated attributes
    """
    return rest.post_single(resource=_resource, entity=director, user=user)
