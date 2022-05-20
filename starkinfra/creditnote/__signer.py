from starkcore.utils.subresource import SubResource


class Signer(SubResource):
    """# creditnote.Signer object
    CreditNote signer's information.
    ## Parameters (required):
    - name [string]: signer's name. ex: "Tony Stark"
    - contact [string]: signer's contact information. ex: "tony@starkindustries.com"
    - method [string]: delivery method for the contract. ex: "link"
    """

    def __init__(self, name, contact, method):
        self.name = name
        self.contact = contact
        self.method = method


_resource = {"class": Signer, "name": "Signer"}
