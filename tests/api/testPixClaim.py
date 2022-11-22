import starkinfra
from time import sleep
from unittest import TestCase, main
from random import choice, shuffle, randint
from tests.utils.pixKey import generateExamplePixKeyJson
from tests.utils.poolingEntities import poolEntitiesAndLogs, poolEntities
from tests.utils.user import exampleProject, exampleReceiverProject
from tests.utils.pixClaim import generateExamplePixClaimJson, keyTypeFromType


starkinfra.user = exampleReceiverProject
name = "PixClaim"
debug = True


class TestPixClaimPost(TestCase):
    def test_success_part(self):
        claimCount = 2

        claims = []
        keys = []
        for _ in range(claimCount):
            starkinfra.user = exampleReceiverProject  # set user to receiver
            claimType = choice(["portability", "ownership"])
            keyType = keyTypeFromType(claimType)

            key = getKey(keyType)
            if not key or randint(0, 100) > 50:
                key = createKey(keyType)

            starkinfra.user = exampleProject  # set user to sender
            sleep(20)

            claim = generateExamplePixClaimJson(key=key, claimType=claimType)
            claim = starkinfra.pixclaim.create(claim)
            claims.append(claim)
            keys.append(key)

        if debug:
            print("keys: {}".format(keys))
            print("senderClaims: {}".format(keys))

        self.assertEqual(len(claims), claimCount)
        claimIds = [claim.id for claim in claims]

        poolEntities(
            name=name,
            ids=claimIds,
            newStatus="created",
            poolRetries=100,
            sleepTime=4,
            debug=debug,
        )

        poolEntitiesAndLogs(
            name=name,
            ids=claimIds,
            entityStatuses=["delivered"],
            logTypes=["created", "delivering", "delivered"],
            entityPoolRetries=20,
            entitySleepTime=1,
            poolRetries=100,
            sleepTime=4,
            debug=debug,
        )

        starkinfra.user = exampleReceiverProject  # set user to receiver
        receiverClaims = []
        for claim in claims:
            while True:
                claimsByKeyId = list(starkinfra.pixclaim.query(
                    key_id=claim.key_id,
                    status="delivered",
                    flow="in",
                ))
                if not claimsByKeyId:
                    sleep(4)
                    continue
                receiverClaims.append(claimsByKeyId[0])
                break

        if len(claims) != len(receiverClaims):
            self.fail("claims not found on receiver workspace")

        if debug:
            print("\nAll entities found in the receiver workspace")

        parametersToExclude = ["flow", "created", "updated", "id", "tags", "status"]
        senderClaimKeyIds = [claim.key_id for claim in claims]
        for receiverClaim in receiverClaims:
            index = senderClaimKeyIds.index(receiverClaim.key_id)
            senderClaim = claims[index]
            receiverClaimDict = receiverClaim.__dict__
            for key, value in receiverClaimDict.items():
                if key not in parametersToExclude and senderClaim.__dict__[key] != value:
                    print("key: {}".format(key))
                    self.fail("Divergence in claimer and claimed arguments")

        patchedClaims = []
        for receiverClaim in receiverClaims:
            patchedClaim = starkinfra.pixclaim.update(id=receiverClaim.id, status="confirmed")
            patchedClaims.append(patchedClaim)

        receiverClaimIds = [receiverClaim.id for receiverClaim in receiverClaims]

        if debug:
            print("\nreceiver claims:\n")

        poolEntitiesAndLogs(
            name=name,
            ids=receiverClaimIds,
            entityStatuses=["confirmed", "success"],
            logTypes=["created", "delivering", "delivered", "confirming", "confirmed"],
            entityPoolRetries=200,
            entitySleepTime=3,
            poolRetries=20,
            sleepTime=3,
            debug=debug,
        )

        starkinfra.user = exampleProject
        if debug:
            print("\nSender entities:\n")

        poolEntitiesAndLogs(
            name=name,
            ids=claimIds,
            entityStatuses=["success"],
            logTypes=["confirming", "confirmed", "success"],
            debug=debug,
            poolRetries=200,
            sleepTime=5,
        )

        starkinfra.user = exampleReceiverProject
        if debug:
            print("\nReceiver entities:\n")

        poolEntitiesAndLogs(
            name=name,
            ids=receiverClaimIds,
            entityStatuses=["success"],
            logTypes=["success"],
            entityPoolRetries=20,
            entitySleepTime=1,
            poolRetries=50,
            sleepTime=2,
            debug=debug,
        )


class CancelRegisteredClaims(TestCase):
    def test_cancel(self):
        claimType = "ownership"
        limit = 100

        claims = list(starkinfra.pixclaim.query(
            status="delivered",
            flow="out",
            type=claimType,
            limit=limit,
        ))
        self.assertNotEqual(len(claims), 0)
        cancelClaims(claims)


def cancelClaims(claims):
    for claim in claims:
        starkinfra.pixclaim.update(id=claim.id, status="canceled", reason="fraud")

    poolEntitiesAndLogs(
        name=name,
        ids=[claim.id for claim in claims],
        entityStatuses=["canceled"],
        logTypes=["canceling", "canceled"],
    )


def createKey(keyType):
    key = generateExamplePixKeyJson(keyType)
    key = starkinfra.pixkey.create(key, user=exampleReceiverProject)
    poolEntitiesAndLogs(
        name="PixKey",
        ids=[key.id],
        entityStatuses=["registered"],
        logTypes=["created", "registered"],
    )

    return key


def getKey(keyType):
    cursor = None
    for _ in range(2):
        keys, cursor = starkinfra.pixkey.page(cursor=cursor, status="registered", type=keyType, limit=5)
        shuffle(keys)
        for key in keys:
            keyClaims, _ = starkinfra.pixclaim.page(key_id=key.id, status=["created", "delivered", "confirmed"])
            if not keyClaims:
                return key


if __name__ == '__main__':
    main()
