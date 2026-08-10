from starkcore.utils.subresource import SubResource


class Address(SubResource):
    """# businessaccountrequest.Address object
    The Address object is the structured address of the company referenced by a
    BusinessAccountRequest. It is embedded on the parent's `address` field and has no endpoints of its own.
    ## Parameters (required):
    - street [string]: street name. ex: "Av. Faria Lima"
    - number [string]: street number. ex: "2000"
    - neighborhood [string]: neighborhood / district. ex: "Itaim Bibi"
    - city [string]: city. ex: "Sao Paulo"
    - state [string]: state (BR 2-letter code). ex: "SP"
    - zip_code [string]: ZIP code (BR CEP), formatted or digit-only. ex: "04538-132"
    ## Parameters (optional):
    - complement [string, default None]: address complement. ex: "Sala 42"
    """

    def __init__(self, street=None, number=None, neighborhood=None, city=None, state=None, zip_code=None,
                 complement=None):
        self.street = street
        self.number = number
        self.neighborhood = neighborhood
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.complement = complement


resource = {"class": Address, "name": "Address"}
