from starkcore.utils.subresource import SubResource


class Signer(SubResource):
    """# creditnote.Signer object
    CreditNote signer's information.
    ## Parameters (required):
    - name [string]: signer name. ex: "Tony Stark"
    - contact [string]: contact for the contract signature request. ex: "tony@starkindustries.com"
    - method [string]: delivery method for the contract. ex: "link"
    """

    def __init__(self, name, contact, method):
        self.name = name
        self.contact = contact
        self.method = method


_resource = {"class": Signer, "name": "Signer"}
