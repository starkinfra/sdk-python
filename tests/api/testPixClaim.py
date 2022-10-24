import starkinfra
from time import sleep
from random import choice, shuffle
from unittest import TestCase, main
from tests.utils.pixKey import generateExamplePixKeyJson
from tests.utils.user import exampleProject, exampleReceiverProject
from tests.utils.poolingEntities import poolEntities, poolLogsByTypes
from tests.utils.pixClaim import generateExamplePixClaimJson, keyTypeFromType


starkinfra.user = exampleReceiverProject
name = "PixClaim"
debug = True


class TestPixClaimPost(TestCase):
    def test_success_part(self):
        claimCount = 3
        createNewKey = True

        claims = []
        keys = []

        for _ in range(claimCount):
            # createNewKey = False
            # if random.randint(0, 100) > 50:
            #     createNewKey = True

            starkinfra.user = exampleReceiverProject
            claimType = choice(["portability", "ownership"])
            keyType = keyTypeFromType(claimType)

            key = getKey(keyType)
            if createNewKey:
                key = createKey(keyType)

            starkinfra.user = exampleProject
            sleep(60)

            claim = generateExamplePixClaimJson(key=key, claimType=claimType)
            claim = starkinfra.pixclaim.create(claim)
            claims.append(claim)
            keys.append(key)

        if debug:
            keysAndClaims = [list(element) for element in zip(keys, claims)]
            for key, claim in keysAndClaims:
                print(key)
                print(claim)

        self.assertEqual(len(claims), claimCount)
        ids = [claim.id for claim in claims]

        poolLogsByTypes(
            name=name,
            ids=ids,
            newTypes=["created", "delivering"],
            debug=debug,
        )

        poolLogsByTypes(
            name=name,
            ids=ids,
            newTypes=["delivered"],
            debug=debug,
            poolRetries=16,
            sleepTime=15
        )

        poolEntities(
            name=name,
            ids=ids,
            newStatus="delivered",
            entityCount=claimCount,
            debug=debug,
        )

        starkinfra.user = exampleReceiverProject
        receiverClaims = []
        for claim in claims:
            receiverClaims.extend(list(
                starkinfra.pixclaim.query(
                    key_id=claim.key_id,
                    status="delivered",
                    after=claim.created
                )
            ))

        parametersToExclude = ["flow", "created", "updated", "id"]
        senderClaimIds = [claim.id for claim in claims]
        for receiverClaim in receiverClaims:
            index = senderClaimIds.index(receiverClaim.id)
            if not index:
                self.fail("Sender claim not found in receiver Claim workspace")
            senderClaim = claims[index]
            receiverClaimDict = receiverClaim.__dict__["_values"]
            for key, value in receiverClaimDict.items():
                if key in parametersToExclude and senderClaim.__dict__[key] != value:
                    self.fail("Divergence in claimer and claimed arguments")

        patchedClaims = []
        for claim in claims:
            patchedClaims.append(starkinfra.pixclaim.update(id=claim.id, status="confirmed"))

        poolEntities(
            name=name,
            ids=ids,
            newStatus="confirmed",
            entityCount=claimCount,
            debug=debug,
            poolRetries=8,
            sleepTime=30
        )

        poolLogsByTypes(
            name=name,
            ids=ids,
            newTypes=["confirming", "confirmed"],
            debug=debug,
            poolRetries=7,
            sleepTime=30
        )

        poolEntities(
            name=name,
            ids=ids,
            newStatus="success",
            entityCount=claimCount,
            debug=debug,
        )

        poolLogsByTypes(
            name=name,
            ids=ids,
            newTypes=["success"],
            debug=debug,
        )

        starkinfra.user = exampleProject

        poolLogsByTypes(
            name=name,
            ids=ids,
            newTypes=["confirming", "confirmed", "success"],
            debug=debug,
            poolRetries=7,
            sleepTime=30
        )

        poolLogsByTypes(
            name=name,
            ids=ids,
            newTypes=["success"],
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
            limit=limit
        ))
        self.assertNotEqual(len(claims), 0)
        cancelClaims(claims)


def cancelClaims(claims):
    for claim in claims:
        starkinfra.pixclaim.update(id=claim.id, status="canceled", reason="fraud")

    poolEntities(
        name=name,
        ids=[claim.id for claim in claims],
        newStatus="canceled",
        debug=debug,
    )
    poolLogsByTypes(
        name=name,
        ids=[claim.id for claim in claims],
        newTypes=["canceling", "canceled"],
        debug=debug,
    )


def createKey(keyType):
    key = generateExamplePixKeyJson(keyType)
    key = starkinfra.pixkey.create(key, user=exampleReceiverProject)

    poolEntities(
        name="PixKey",
        ids=[key.id],
        newStatus="registered",
    )
    poolLogsByTypes(
        name="PixKey",
        ids=[key.id],
        newTypes=["created", "registered"],
    )
    return key


def getKey(keyType):
    cursor = None

    while True:
        keys, cursor = starkinfra.pixkey.page(cursor=cursor, status="registered", type=keyType, limit=10)
        shuffle(keys)
        for key in keys:
            if key not in list(starkinfra.pixclaim.query(key_id=key.id, status=["created", "delivered", "confirmed"])):
                return key


if __name__ == '__main__':
    main()
