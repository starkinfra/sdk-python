import starkinfra
from tests.utils.user import exampleProject


starkinfra.user = exampleProject


def get_end_to_end_id_to_reverse():
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


def get_end_to_end_id(n=1):
    end_to_end_ids = []
    requests = starkinfra.pixrequest.query(limit=n)
    for request in requests:
        end_to_end_ids.append(str(request.end_to_end_id))
    if len(end_to_end_ids) < 1:
        print("Sorry, There are no PixRequests in your workspace")
    return end_to_end_ids
