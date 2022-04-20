import starkinfra
from random import choice
from datetime import datetime
from tests.utils.user import exampleProject


starkinfra.user = exampleProject


def get_end_to_end_id():
    cursor = None
    end_to_end_ids = []
    while len(end_to_end_ids) < 10:
        requests, cursor = starkinfra.pixrequest.page(cursor=cursor, limit=10)
        for request in requests:
            if request.flow == "in" and request.amount > 10:
                end_to_end_ids.append(str(request.end_to_end_id))
        if len(end_to_end_ids) < 1:
            print("Sorry, There are no PixRequests to be reversed in your workspace")
        if cursor is None:
            break
        return end_to_end_ids


class BacenId:

    _randomSource = [c for c in "abcdefghijklmnopqrstuvwxyz"]
    _randomSource += [c.upper() for c in _randomSource]
    _randomSource += [c for c in "0123456789"]

    @classmethod
    def newEndToEndId(cls, ispb):
        return "E{bacenId}".format(bacenId=cls._newBacenId(ispb))

    @classmethod
    def _newBacenId(cls, ispb):
        return "{ispb}{date}{randomString}".format(
            ispb=ispb,
            date=datetime.utcnow().strftime("%Y%m%d%H%M"),
            randomString=''.join(choice(cls._randomSource) for _ in range(11)),
        )
