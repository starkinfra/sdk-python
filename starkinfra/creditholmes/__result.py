from starkcore.utils.api import from_api_json
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime_or_date


class Result(Resource):
    """# creditholmes.Result object
    Result of the CreditHolmes investigation after the case is solved.
    ## Attributes (return-only):
    - risk [float]: vendor calculated risk
    - companyCount [integer]: number of financial institutions the target has relations with.
    - blockedCount [integer]: number of operations which are under legal block
    - blockedPercentage [float]: percentage of installment amount under legal block
    - disputedCount [integer]: number of operations which are under legal dispute
    - disputedPercentage [float]: percentage of installment amount under legal dispute
    - acquiredShare [float]: percentage of credit operations which have been acquired from other financial institutions
    - receivedShare [float]: percentage of credit operations which have been received from other financial institutions
    - operations [list of Operation objects]: list of credit operations listed within the current competence
    - created [datetime.datetime]: creation date of the user in SCR database. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, risk=None, companyCount=None, blockedCount=None, blockedPercentage=None,
                 disputedCount=None, disputedPercentage=None, acquiredShare=None, receivedShare=None,
                 created=None, operations=None):
        Resource.__init__(self, id=id)

        self.risk = risk
        self.companyCount = companyCount
        self.blockedCount = blockedCount
        self.blockedPercentage = blockedPercentage
        self.disputedCount = disputedCount
        self.disputedPercentage = disputedPercentage
        self.acquiredShare = acquiredShare
        self.receivedShare = receivedShare
        self.operations = operations
        self.created = check_datetime_or_date(created)


_resource = {"class": Result, "name": "Result"}


def parse_result(result):
    if not result:
        return result
    return from_api_json(_resource, result)
