from copy import deepcopy
from starkinfra import PixStatement
from random import choice
from ..utils.date import randomPastDate


example_pix_statement = PixStatement(
    after="2022-01-01",
    before="2022-01-01",
    type=choice(["interchange", "interchangeTotal", "transaction"]),
)


def generateExamplePixStatementJson():
    pix_statement = deepcopy(example_pix_statement)
    pix_statement.type = choice(["interchange", "interchangeTotal", "transaction"])
    if pix_statement.type == "transaction":
        pix_statement.after = randomPastDate(days=360)
        pix_statement.before = pix_statement.after
    else:
        pix_statement.after = choice(["2021-10-01", "2021-11-01", "2021-12-01", "2022-01-01"])
        pix_statement.before = pix_statement.after
    return pix_statement
