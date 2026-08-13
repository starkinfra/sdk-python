from starkcore.utils.subresource import SubResource


class Owner(SubResource):
    """# businessaccountrequest.Owner object
    The Owner object represents a company owner referenced by a BusinessAccountRequest. Each owner
    completes its own identity verification through an independent webview. It is embedded on the
    parent's `owners` field and has no endpoints of its own.
    ## Parameters (required):
    - tax_id [string]: owner's tax ID (CPF). ex: "012.345.678-90"
    - name [string]: owner's full name (minimum 5 characters). ex: "Jamie Lannister"
    - role [string]: owner's role in the company. Options: "partner", "representative"
    ## Attributes (return-only):
    - identity_id [string]: unique id of the identity verification linked to this owner. ex: "5709594221805568"
    - validator_link [string]: webview link to be delivered to the owner to complete biometrics and document capture.
    - status [string]: current status of the owner verification. Options: "created", "approved", "denied"
    """

    def __init__(self, tax_id=None, name=None, role=None, identity_id=None, validator_link=None, status=None):
        self.tax_id = tax_id
        self.name = name
        self.role = role
        self.identity_id = identity_id
        self.validator_link = validator_link
        self.status = status


resource = {"class": Owner, "name": "Owner"}
