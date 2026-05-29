from starkcore.utils.subresource import SubResource


class Address(SubResource):
    """# individualaccountrequest.Address object
    The Address object is the structured residential address of the individual referenced by an
    IndividualAccountRequest. It is embedded on the parent's `address` field and has no endpoints of its own.
    ## Parameters (required):
    - street [string]: street name. ex: "Rua do Estilo Barroco"
    - number [string]: street number. ex: "648"
    - neighborhood [string]: neighborhood / district. ex: "Santo Amaro"
    - city [string]: city. ex: "Sao Paulo"
    - state [string]: state (BR 2-letter code). ex: "SP"
    - zip_code [string]: ZIP code (BR CEP), formatted or digit-only. ex: "05724005"
    """

    def __init__(self, street=None, number=None, neighborhood=None, city=None, state=None, zip_code=None):
        self.street = street
        self.number = number
        self.neighborhood = neighborhood
        self.city = city
        self.state = state
        self.zip_code = zip_code


resource = {"class": Address, "name": "Address"}
