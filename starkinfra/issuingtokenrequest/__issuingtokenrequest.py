from starkcore.utils.subresource import SubResource
from starkinfra.utils import rest


class IssuingTokenRequest(SubResource):
    """# IssuingTokenRequest object
    The IssuingTokenRequest object displays the necessary information to proceed with the card tokenization.
    ## Parameters (required):
    - card_id [string]: card id to be tokenized. ex: "5734340247945216"
    - wallet_id [string]: desired wallet to be integrated. ex: "google"
    - method_code [string]: method code. ex: "app" or "manual"
    ## Attributes (return-only):
    - content [string]: token request content. ex: "eyJwdWJsaWNLZXlGaW5nZXJwcmludCI6ICJlNTNiZThjZTRhYWQxNWU2OWNmMjExOTA5Mjk4YzJkOTE0O..."
    - signature [string]: token request signature. ex: "eyJwdWJsaWNLZXlGaW5nZXJwcmludCI6ICJlNTNiZThjZTRhYWQxNWU2OWNmMjExOTA5Mjk4YzJkOTE0O..."
    - metadata [dictionary]: dictionary object used to store additional information about the IssuingTokenRequest object.
    """

    def __init__(self, card_id, wallet_id, method_code, content=None, signature=None, metadata=None):
        self.card_id = card_id
        self.wallet_id = wallet_id
        self.method_code = method_code
        self.content = content
        self.signature = signature
        self.metadata = metadata


_resource = {"class": IssuingTokenRequest, "name": "IssuingTokenRequest"}


def create(request, user=None):
    """# Create an IssuingTokenRequest object
    Send an IssuingTokenRequest object to Stark Infra API to create the payload to proceed with the card tokenization
    ## Parameters (required):
    - request [IssuingTokenRequest object]: IssuingTokenRequest object to the API to generate the payload
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - IssuingTokenRequest object with updated attributes
    """
    return rest.post_single(resource=_resource, entity=request, user=user)
