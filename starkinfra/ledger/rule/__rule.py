from starkcore.utils.api import from_api_json
from starkcore.utils.subresource import SubResource


class Rule(SubResource):
    """# Ledger.Rule object
    The Ledger.Rule object modifies the behavior of Ledger objects when passed as an argument upon their creation or update.
    ## Parameters (required):
    - key [string]: Rule to be customized, describes what Ledger behavior will be altered. ex: "minimumBalance", "maximumBalance"
    - value [integer]: Value of the rule. ex: 1000
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value


_sub_resource = {"class": Rule, "name": "Rule"}


def parse_rules(rules):
    if rules is None:
        return None
    parsed_rules = []
    for rule in rules:
        if isinstance(rule, Rule):
            parsed_rules.append(rule)
            continue
        parsed_rules.append(from_api_json(_sub_resource, rule))
    return parsed_rules
