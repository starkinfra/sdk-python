import time
import starkinfra
from random import choice
from copy import deepcopy
from unittest import TestCase, main
from tests.utils.pixInfraction import example_pix_infraction
from tests.utils.user import exampleProject, exampleReceiverProject
from tests.utils.poolingEntities import poolEntities, poolLogs, poolEntitiesAndLogs

starkinfra.user = exampleProject
name = "PixInfraction"
debug = True


class TestPixInfractionPost(TestCase):
    def test_success(self):
        infractionCount = 2

        allInfractions = []
        for _ in range(infractionCount):
            infractionType = choice(["reversal", "reversalChargeback", "fraud"])
            infractions = generateReceiverPixInfractionsJson(
                limit=1,
                receiverBankCode="34052649",
                infractionType=infractionType,
            )
            infractions = starkinfra.pixinfraction.create(infractions)
            allInfractions.extend(infractions)

        if debug:
            for infraction in allInfractions:
                print(infraction)

        self.assertEqual(len(allInfractions), infractionCount)
        self.assertNotEqual(len(allInfractions), 0)
        infractionIds = [infraction.id for infraction in allInfractions]

        time.sleep(5*60)

        if debug:
            print("\nSender infractions:\n")

        poolEntitiesAndLogs(
            name=name,
            ids=infractionIds,
            logTypes=["created", "delivering", "delivered"],
            entityStatuses=["delivered"],
            poolRetries=50,
            sleepTime=6,
            debug=debug,
        )
        infractions = list(starkinfra.pixinfraction.query(ids=infractionIds))

        after = infractions[0].created.date()
        senderReferenceIds = [infraction.reference_id for infraction in infractions]

        starkinfra.user = exampleReceiverProject  # change to receiver's workspace
        while True:
            time.sleep(5)
            receiverInfractionIds = []
            receiverInfractions = list(starkinfra.pixinfraction.query(
                after=after,
                flow="in",
                status="delivered"
            ))
            receiverReferenceIds = [infraction.reference_id for infraction in receiverInfractions]
            infractionsByReferenceIds = {infraction.reference_id: infraction for infraction in receiverInfractions}
            for senderReferenceId in senderReferenceIds:
                if senderReferenceId not in receiverReferenceIds:
                    continue
                receiverInfractionIds.append(infractionsByReferenceIds[senderReferenceId].id)
            break

        if debug:
            print("\nReceiver infractions:\n")

        print("receiverInfractionIds: {}".format(receiverInfractionIds))

        poolEntitiesAndLogs(
            name=name,
            ids=receiverInfractionIds,
            logTypes=["created", "delivering", "delivered"],
            entityStatuses=["delivered"],
            poolRetries=100,
            sleepTime=2,
            debug=debug,
        )

        for id in receiverInfractionIds:
            starkinfra.pixinfraction.update(
                id=id,
                result="agreed",
                user=exampleReceiverProject,
            )

        poolEntitiesAndLogs(
            name=name,
            ids=receiverInfractionIds,
            logTypes=["closed"],
            entityStatuses=["closed"],
            poolRetries=100,
            sleepTime=2,
            debug=debug,
        )

        if debug:
            print("\nSender infractions:\n")

        time.sleep(5 * 60)
        starkinfra.user = exampleProject  # change to sender's workspace
        poolEntitiesAndLogs(
            name=name,
            ids=infractionIds,
            logTypes=["closed"],
            entityStatuses=["closed"],
            poolRetries=50,
            sleepTime=6,
            debug=debug,
        )


class CancelRegisteredInfractions(TestCase):
    def test_cancel(self):
        limit = 3

        infractions = list(starkinfra.pixinfraction.query(
            status=["delivered", "created"],
            flow="out",
            limit=limit,
        ))
        self.assertNotEqual(len(infractions), 0)
        cancelInfractions(infractions)


def cancelInfractions(infractions):
    for infraction in infractions:
        starkinfra.pixinfraction.cancel(id=infraction.id)

    poolEntities(
        name=name,
        ids=[infraction.id for infraction in infractions],
        newStatus="canceled",
        debug=debug,
    )
    poolLogs(
        name=name,
        ids=[infraction.id for infraction in infractions],
        newType="canceled",
        debug=debug,
    )


def generateReceiverPixInfractionsJson(receiverBankCode, limit=1, infractionType="fraud"):
    infractions = []
    receiverRequests = getTransactions(
        limit=limit,
        receiverBankCode=receiverBankCode,
        queryFunction=starkinfra.pixrequest.page,
    )
    referenceIds = [request.end_to_end_id for request in receiverRequests]

    if infractionType == "reversalChargeback":
        receiverReversals = getTransactions(
            limit=limit,
            receiverBankCode=receiverBankCode,
            queryFunction=starkinfra.pixrequest.page,
        )
        referenceIds = [reversal.return_id for reversal in receiverReversals]

    for referenceId in referenceIds:
        infraction = deepcopy(example_pix_infraction)
        infraction.reference_id = referenceId
        infraction.type = infractionType
        infractions.append(infraction)
    return infractions


def getTransactions(receiverBankCode, limit, queryFunction):
    receiverRequests = []
    cursor = None
    while True:
        requests, cursor = queryFunction(limit=100, status="success", cursor=cursor)
        receiverRequest = [
            request for request in requests
            if request.receiver_bank_code == receiverBankCode
               or request.sender_bank_code == receiverBankCode
        ]
        receiverRequests.extend(receiverRequest)
        if len(receiverRequests) >= limit:
            break
        if not cursor:
            print("Less Pix transactions than the limit were found")
            break
    return receiverRequests[:limit]


if __name__ == '__main__':
    main()
