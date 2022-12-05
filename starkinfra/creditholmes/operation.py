from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime_or_date


class Operation(Resource):
    """# creditholmes.Operation object
    Credit Operation initiated by the target of a CreditHolmes.
    ## Attributes (return-only):
    - risk [float]: vendor calculated risk
    - companyCount [integer]: number of financial institutions the target has relations with.
    - blockedCount [integer]: number of operations which are under legal block
    - blockedPercentage [float]: percentage of installment amount under legal block
    - disputedCount [integer]: number of operations which are under legal dispute
    - disputedPercentage [float]: percentage of installment amount under legal dispute
    - acquiredShare [float]:
    - receivedShare [float]:
    - operations [list of Operation objects]:
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


_resource = {"class": Operation, "name": "Operation"}
