from random import choice
from datetime import datetime


_randomSource = [c for c in "abcdefghijklmnopqrstuvwxyz"]
_randomSource += [c.upper() for c in _randomSource]
_randomSource += [c for c in "0123456789"]


def create(bank_code):
    return "{bank_code}{date}{randomString}".format(
        bank_code=bank_code,
        date=datetime.utcnow().strftime("%Y%m%d%H%M"),
        randomString=''.join(choice(_randomSource) for _ in range(11)),
    )
