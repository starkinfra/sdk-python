from starkcore.utils.resource import Resource


class CreditSigner(Resource):
    """# CreditSigner object
    CreditNote signer's information.
    ## Parameters (required):
    - name [string]: signer's name. ex: "Tony Stark"
    - contact [string]: signer's contact information. ex: "tony@starkindustries.com"
    - method [string]: delivery method for the contract. ex: "link"
    Attributes (return-only):
    - id [string]: unique id returned when the CreditSigner is created. ex: "5656565656565656"
    """

    def __init__(self, name, contact, method, id=None):
        Resource.__init__(self, id=id)
        self.name = name
        self.contact = contact
        self.method = method


_resource = {"class": CreditSigner, "name": "CreditSigner"}
