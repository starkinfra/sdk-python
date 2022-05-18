from starkcore.utils.subresource import SubResource


class Certificate(SubResource):
    """# pixdomain.Certificate object
    The Certificate object displays the certificate information from a specific domain.
    ## Attributes (return-only):
    - content [string]: certificate of the Pix participant in PEM format.
    """

    def __init__(self, content=None):
        self.content = content


_resource = {"class": Certificate, "name": "Certificate"}
