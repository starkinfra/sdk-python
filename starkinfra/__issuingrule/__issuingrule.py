from starkcore.utils.api import from_api_json
from starkcore.utils.resource import Resource


class IssuingRule(Resource):

    """# IssuingRule object
    The IssuingRule object displays the spending rules of IssuingCards and IssuingHolders created in your Workspace.
    ## Parameters (required):
    - name [string]: rule name. ex: "Travel" or "Food"
    - amount [integer]: maximum amount that can be spent in the informed interval. ex: 200000 (= R$ 2000.00)
    ## Parameters (optional):
    - id [string, default None]: unique id returned when an IssuingRule is created, used to update a specific IssuingRule. ex: "5656565656565656"
    - interval [string, default "lifetime"]: interval after which the rule amount counter will be reset to 0. ex: "instant", "day", "week", "month", "year" or "lifetime"
    - currency_code [string, default "BRL"]: code of the currency that the rule amount refers to. ex: "BRL" or "USD"
    - categories [list of strings, default []]: merchant categories accepted by the rule. ex: ["eatingPlacesRestaurants", "travelAgenciesTourOperators"]
    - countries [list of strings, default []]: countries accepted by the rule. ex: ["BRA", "USA"]
    - methods [list of strings, default []]: card purchase methods accepted by the rule. ex: ["chip", "token", "server", "manual", "magstripe", "contactless"]
    ## Attributes (expanded return-only):
    - counter_amount [integer]: current rule spent amount. ex: 1000
    - currency_symbol [string]: currency symbol. ex: "R$"
    - currency_name [string]: currency name. ex: "Brazilian Real"
    """

    def __init__(self, name, amount, id=None, interval=None, currency_code=None, categories=None, countries=None,
                 methods=None, counter_amount=None, currency_name=None, currency_symbol=None):
        Resource.__init__(self, id=id)

        self.name = name
        self.amount = amount
        self.interval = interval
        self.counter_amount = counter_amount
        self.categories = categories
        self.countries = countries
        self.methods = methods
        self.currency_code = currency_code
        self.currency_symbol = currency_symbol
        self.currency_name = currency_name

_resource = {"class": IssuingRule, "name": "IssuingRule"}


def parse_rules(rules):
    parsed_rules = []
    if rules is None:
        return rules
    for rule in rules:
        if isinstance(rule, IssuingRule):
            parsed_rules.append(rule)
            continue
        parsed_rules.append(from_api_json(_resource, rule))
    return parsed_rules

