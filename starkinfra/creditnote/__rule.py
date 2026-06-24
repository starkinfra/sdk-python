from starkcore.utils.api import from_api_json
from starkcore.utils.subresource import SubResource


class Rule(SubResource):
    """# CreditNote.Rule object
    The CreditNote.Rule object modifies the behavior of CreditNote objects when passed
    as an argument upon their creation.
    ## Parameters (required):
    - key [string]: Rule to be customized, describes what CreditNote behavior will be altered. ex: "invoiceCreationMode"
    - value [string]: Value of the rule. ex: "scheduled", "instant", "never"
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
