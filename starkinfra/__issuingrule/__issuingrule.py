from starkcore.utils.resource import Resource


class IssuingRule(Resource):

    """# IssuingRule object
    The IssuingRule object displays the spending rules of IssuingCards and IssuingHolders created in your Workspace.
    ## Parameters (required):
    - name [string]: rule name. ex: "Travel" or "Food"
    - amount [integer]: maximum amount that can be spent in the informed interval. ex: 200000 (= R$ 2000.00)
    - interval [string]: interval after which the rule amount counter will be reset to 0. ex: "instant", "day", "week", "month", "year" or "lifetime"
    ## Parameters (optional):
    - currency_code [string, default "BRL"]: code of the currency that the rule amount refers to. ex: "BRL" or "USD"
    - categories [list of strings, default []]: merchant categories accepted by the rule. ex: ["eatingPlacesRestaurants", "travelAgenciesTourOperators"]
    - countries [list of strings, default []]: countries accepted by the rule. ex: ["BRA", "USA"]
    - methods [list of strings, default []]: card purchase methods accepted by the rule. ex: ["contactless", "manual"]
    ## Attributes (expanded return-only):
    - counter_amount [integer]: current rule spent amount. ex: 1000
    - currency_symbol [string]: currency symbol. ex: "R$"
    - currency_name [string]: currency name. ex: "Brazilian Real"
    ## Attributes (return-only):
    - id [string]: unique id returned when Rule is created. ex: "5656565656565656"
    """

    def __init__(self, id=None, name=None, interval=None, amount=None, currency_code=None, counter_amount=None,
                 currency_name=None, currency_symbol=None, categories=None, countries=None, methods=None):
        Resource.__init__(self, id=id)
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
