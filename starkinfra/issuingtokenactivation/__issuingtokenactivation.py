from ..utils.parse import parse_and_verify
from starkcore.utils.subresource import SubResource


class IssuingTokenActivation(SubResource):
    """# IssuingTokenActivation object
    The IssuingTokenActivation object displays the necessary information to proceed with the card tokenization.
    You will receive this object at your registered URL to notify you which method your user want to receive the activation code.
    The POST request must be answered with no content, within 2 seconds, and with an HTTP status code 200.
    After that, you may generate the activation code and send it to the cardholder.
    ## Attributes (return-only):
    - card_id [string]: card ID which the token is bounded to. ex: "5656565656565656"
    - token_id [string]: token unique id. ex: "5656565656565656" 
    - tags [list of strings]: tags to filter retrieved object. ex: ["tony", "stark"]
    - activation_method [dictionary]: dictionary object with "type":string and "value":string pairs
    """

    def __init__(self, card_id=None, token_id=None, tags=None, activation_method=None):
        self.card_id = card_id
        self.token_id = token_id
        self.tags = tags
        self.activation_method = activation_method


_resource = {"class": IssuingTokenActivation, "name": "IssuingTokenActivation"}


def parse(content, signature, user=None):
    """# Create a single verified IssuingTokenActivation request from a content string
    Use this method to parse and verify the authenticity of the request received at the informed endpoint.
    Activation requests are posted to your registered endpoint whenever IssuingTokenActivations are received.
    If the provided digital signature does not check out with the StarkInfra public key, a stark.exception.InvalidSignatureException will be raised.
    ## Parameters (required):
    - content [string]: response content from request received at user endpoint (not parsed)
    - signature [string]: base-64 digital signature received at response header "Digital-Signature"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - Parsed IssuingTokenActivation object
    """
    return parse_and_verify(
        content=content,
        signature=signature,
        user=user,
        resource=_resource,
        key="",
    )
