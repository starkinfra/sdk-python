from ..utils.resource import Resource


class IssuingRule(Resource):

    """# IssuingRule object
    The IssuingRule object displays the spending rules of Cards created to your Workspace.
    ## Parameters (required):
    - name [string, default None]: rule name. ex: "Travel" or "Food"
    - amount [string, default None]: amount to be used in informed interval. ex: 200000 (= R$ 2000.00)
    - interval [string, default None]: interval to reset the counters of the rule. ex: "instant", "day", "week", "month", "year" or "lifetime"
    ## Attributes (return-only):
    - id [string, default None]: unique id returned when Rule is created. ex: "5656565656565656"
    - currency_code [string, default None]: code of the currency used by the rule. ex: "BRL" or "USD"
    ## Attributes (expanded return-only):
    - counter_amount [integer, default None:
    - currency_name [string, default None: currency name. ex: "Brazilian Real"
    - currency_symbol [string, default None: currency symbol. ex: "R$"
    - categories [list of strings, default []]: merchant categories accepted by the rule. ex: ["eatingPlacesRestaurants", "travelAgenciesTourOperators"]
    - countries [list of strings, default []]: countries accepted by the rule. ex: ["BRA", "USA"]
    - methods [list of strings, default []]: methods accepted by the rule. ex: ["contactless", "token"]
    """

    def __init__(self, id=None, name=None, interval=None, amount=None, currency_code=None, counter_amount=None,
                 currency_name=None, currency_symbol=None, categories=None, countries=None, methods=None):
        super().__init__(id)
        self.name = name
        self.interval = interval
        self.amount = amount
        self.currency_code = currency_code
        self.counter_amount = counter_amount
        self.currency_name = currency_name
        self.currency_symbol = currency_symbol
        self.categories = categories
        self.countries = countries
        self.methods = methods
