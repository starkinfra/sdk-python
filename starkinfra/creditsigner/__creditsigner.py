from starkcore.utils.resource import Resource

from starkinfra.utils import rest


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

    def __init__(self, name, contact, method, id=None, status=None):
        Resource.__init__(self, id=id)
        self.name = name
        self.contact = contact
        self.method = method


_resource = {"class": CreditSigner, "name": "CreditSigner"}


def resend_token_one_signer(signerId: str, user=None):
    """# Resend token to signer 
    Resend token to a specific signer.
    ## Parameters (required):
    - signerId [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. 
    Not necessary if starkinfra.user was set before function call.
    ## Return:
    
    """
    return rest.patch_id(
        resource=_resource,
        id=signerId,
        user=user,
        payload={"isSent": False},
    )
