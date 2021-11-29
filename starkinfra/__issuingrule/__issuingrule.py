from ..utils.resource import Resource


class IssuingRule(Resource):

    """# IssuingRule object
    The IssuingRule object displays the informations of Cards created to your Workspace.
    ## Attributes (return-only):
    - id [string, default None]: unique id returned when Issuing Card is created. ex: "5656565656565656"
    - holder_id [string, default None]: card holder unique id.
    - type [string, default None]: card type. ex: "virtual"
    - status [string, default None]: current Issuing Card status. ex: "canceled" or "active"
    - number [string, default None]: card number. ex: "1234 5678 1234 5678"
    - security_code [string, default None]: card verification value (cvv). ex: "123"
    - expiration [string, default None]: [EXPANDABLE] expiration datetime for the Card. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - updated [datetime.datetime, default None]: latest update datetime for the bin. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - created [datetime.datetime, default None]: creation datetime for the bin. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    ## Attributes (expanded return-only):
    - merchantCountryName [string, default None]: expiration datetime for the Card. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, id=None, counter=None, name=None, amount=None, currency_code=None, interval=None,
                 categories=None, merchant_ids=None, countries=None, methods=None, allowed_amount=None,
                 allowed_amount_brl=None):
        super().__init__(id)
        self.counter = counter
        self.name = name
        self.amount = amount
        self.currency_code = currency_code
        self.interval = interval
        self.categories = categories
        self.merchant_ids = merchant_ids
        self.countries = countries
        self.methods = methods
        self.allowed_amount = allowed_amount
        self.allowed_amount_brl = allowed_amount_brl
