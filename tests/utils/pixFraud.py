#coding: utf-8
from copy import deepcopy
from random import randint
from starkinfra import PixFraud, pixfraud


example_pix_fraud = PixFraud(
    external_id= "my_external_id_" + str(randint(1, 1000)),
    type="scam",
    tax_id="01234567890"
)


def generateExamplePixFraudsJson():
    pix_frauds = []
    fraud = deepcopy(example_pix_fraud)
    fraud.reference_id = id
    pix_frauds.append(fraud)
    return pix_frauds

