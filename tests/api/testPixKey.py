import starkinfra
from time import sleep
from unittest import TestCase, main
from tests.utils.user import exampleProject, exampleReceiverProject
from tests.utils.names.names import get_full_name
from tests.utils.pixKey import generateExamplePixKeyJson
from tests.utils.poolingEntities import poolEntities, poolLogs, poolLogsByTypes

starkinfra.user = exampleProject
name = "PixKey"
debug = True


class TestPixKeyPost(TestCase):
    def test_success(self):
        keyTypes = ["phone", "email", "cpf", "cnpj", "evp"]
        keyCount = len(keyTypes)
        sleepEvpTime = 5

        keys = []
        for keyType in keyTypes:
            key = generateExamplePixKeyJson(keyType)
            key = starkinfra.pixkey.create(key)

            if keyType == "evp":
                key = getEvpKey(key, sleepEvpTime)
            keys.append(key)

        if debug:
            for key in keys:
                print(key)

        self.assertEqual(len(keys), keyCount)
        ids = [key.id for key in keys]

        poolEntities(
            name=name,
            ids=ids,
            newStatus="registered",
            entityCount=keyCount,
            debug=debug,
        )

        keyTypes = set([key.type for key in keys])
        if "evp" not in keyTypes:
            poolLogs(
                name=name,
                ids=[key.id for key in keys],
                newType="created",
                debug=debug,
            )
        poolLogs(
            name=name,
            ids=[key.id for key in keys],
            newType="registered",
            debug=debug,
        )

        for id in ids:
            key = starkinfra.pixkey.update(id=id, reason="reconciliation", name=get_full_name())
            assert key.id is not None

        poolLogs(
            name=name,
            ids=[key.id for key in keys],
            newType="updated",
            debug=debug,
        )

        keys = list(starkinfra.pixkey.query(ids=ids))
        cancelKeys(keys=keys, limit=keyCount)


class CancelRegisteredKeys(TestCase):
    def test_cancel(self):
        keyType = None
        searchLimit = 100
        limit = 30

        keys = list(starkinfra.pixkey.query(
            status="registered",
            type=keyType,
            limit=searchLimit,
        ))
        self.assertNotEqual(len(keys), 0)
        cancelKeys(keys=keys, limit=limit)


def getEvpKey(key, sleepEvpTime):
    sleep(sleepEvpTime)
    evpKey = list(starkinfra.pixkey.query(type="evp", limit=5))
    keys = [
        registeredKey
        for registeredKey in evpKey
        if registeredKey.tax_id == key.tax_id and registeredKey.account_number == key.account_number
    ]

    if not keys:
        raise Exception("No keys found!")

    key = keys[0]
    if key.status != "registered":
        raise Exception("Increase the waiting time for evp PixKeys")
    return key


def cancelKeys(keys, limit):
    unclaimedKeys = []
    for key in keys:
        claimedKeys = list(starkinfra.pixclaim.query(
            status=["created", "delivered", "confirmed"],
            key_id=key.id,
        ))
        if not claimedKeys:
            unclaimedKeys.append(key)
    keys = unclaimedKeys

    if not keys:
        raise Exception("No unclaimed keys of these type to cancel")

    if len(keys) > limit:
        keys = keys[0:limit]

    for key in keys:
        starkinfra.pixkey.cancel(id=key.id)

    poolEntities(
        name=name,
        ids=[key.id for key in keys],
        newStatus="canceled",
        debug=debug,
    )
    poolLogsByTypes(
        name=name,
        ids=[key.id for key in keys],
        newTypes=["canceling", "canceled"],
        debug=debug,
    )


if __name__ == '__main__':
    main()
