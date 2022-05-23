from starkcore.utils.subresource import SubResource


class Description(SubResource):
    """# creditnote.invoice.Discount object
    Invoice discount information.
    ## Parameters (required):
    - key [string]: Description for the value. ex: "Taxes"
    ## Parameters (optional):
    - value [string]: amount related to the described key. ex: "R$100,00"
    """

    def __init__(self, key, value=None):
        self.key = key
        self.value = value


resource = {"class": Description, "name": "Description"}
