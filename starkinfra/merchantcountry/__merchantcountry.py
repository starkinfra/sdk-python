from starkcore.utils.subresource import SubResource
from starkinfra.utils import rest


class MerchantCountry(SubResource):
    """# MerchantCountry object
    MerchantCountry's codes are used to define countries filters in IssuingRules.
    ## Parameters (required):
    - code [string]: country's code. ex: "BRA"
    ## Attributes (return-only):
    - name [string]: country's name. ex: "Brazil"
    - number [string]: country's number. ex: "076"
    - short_code [string]: country's short code. ex: "BR"
    """

    def __init__(self, code, name=None, number=None, short_code=None):
        self.code = code
        self.name = name
        self.number = number
        self.short_code = short_code


_resource = {"class": MerchantCountry, "name": "MerchantCountry"}


def query(search=None, user=None):
    """# Retrieve MerchantCountries
    Receive a generator of MerchantCountry objects previously created in the Stark Infra API
    ## Parameters (optional):
    - search [string, default None]: keyword to search for code, name, number or short_code
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - generator of MerchantCountry objects with updated attributes
    """
    return rest.get_stream(
        resource=_resource,
        search=search,
        user=user,
    )
