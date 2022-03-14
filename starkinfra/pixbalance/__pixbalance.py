from ..utils import rest
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime


class PixBalance(Resource):
    """# PixBalance object
    The PixBalance object displays the current balance of the workspace,
    which is the result of the sum of all transactions within this
    workspace. The balance is never generated by the user, but it
    can be retrieved to see the available information.
    ## Attributes (return-only):
    - id [string, default None]: unique id returned when Balance is created. ex: "5656565656565656"
    - amount [integer, default None]: current balance amount of the workspace in cents. ex: 200 (= R$ 2.00)
    - currency [string, default None]: currency of the current workspace. Expect others to be added eventually. ex: "BRL"
    - updated [datetime.datetime, default None]: latest update datetime for the balance. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, amount=None, currency=None, updated=None, id=None):
        Resource.__init__(self, id=id)

        self.amount = amount
        self.currency = currency
        self.updated = check_datetime(updated)


_resource = {"class": PixBalance, "name": "PixBalance"}


def get(user=None):
    """# Retrieve the PixBalance object
    Receive the Balance object linked to your workspace in the Stark Infra API
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call
    ## Return:
    - PixBalance object with updated attributes
    """
    return next(rest.get_stream(resource=_resource, user=user))
