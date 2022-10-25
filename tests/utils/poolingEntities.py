import starkinfra
from time import sleep


funcByName = {
    "PixKey": starkinfra.pixkey.query,
    "PixClaim": starkinfra.pixclaim.query,
    "PixInfraction": starkinfra.pixinfraction.query,
    "PixChargeback": starkinfra.pixchargeback.query,
}
logFuncByName = {
    "PixKey": starkinfra.pixkey.log.query,
    "PixClaim": starkinfra.pixclaim.log.query,
    "PixInfraction": starkinfra.pixinfraction.log.query,
    "PixChargeback": starkinfra.pixchargeback.log.query,
}
idsNameByName = {
    "PixKey": "key_ids",
    "PixClaim": "claim_ids",
    "PixInfraction": "infraction_ids",
    "PixChargeback": "chargeback_ids",
}


def poolEntitiesAndLogs(name, ids, entityStatuses, logTypes, poolRetries=10, sleepTime=1,
                        entityPoolRetries=None, entitySleepTime=None, debug=False):
    for newType in logTypes:
        poolLogs(
            name=name,
            ids=ids,
            newType=newType,
            poolRetries=poolRetries,
            sleepTime=sleepTime,
            debug=debug
        )
    for newStatus in entityStatuses:
        poolEntities(
            name=name,
            ids=ids,
            newStatus=newStatus,
            poolRetries=entityPoolRetries or entityPoolRetries,
            sleepTime=entitySleepTime or entitySleepTime,
            debug=debug
        )


def poolEntitiesByStatuses(name, ids, newStatuses, poolRetries=10, sleepTime=1, debug=False):
    for newStatus in newStatuses:
        poolEntities(name, ids, newStatus, poolRetries=poolRetries, sleepTime=sleepTime, debug=debug)


def poolEntities(name, ids, newStatus, poolRetries=10, sleepTime=2, entityCount=None, debug=False):
    poolFunc = funcByName[name]
    if not entityCount:
        entityCount = len(ids)

    if not ids:
        return

    time = 0
    entities = []
    foundEntities = False
    for _ in range(poolRetries):
        sleep(sleepTime)
        time += sleepTime

        entities = list(poolFunc(ids=ids, status=newStatus))
        foundEntities = len(entities) == entityCount
        statusSet = set([entity.status for entity in entities])
        if not foundEntities or len(statusSet) > 1 or newStatus not in statusSet:
            foundEntities = False
            continue
        break

    if debug:
        print("\nEntity status {}, pooling time = {}".format(newStatus.upper(), time))
        for entity in entities:
            print(entity.status.upper())

    if not foundEntities:
        raise Exception("No entities found with {} status".format(newStatus.upper()))


def poolLogsByTypes(name, ids, newTypes, poolRetries=10, sleepTime=1, debug=False):
    for newType in newTypes:
        poolLogs(name, ids, newType, poolRetries=poolRetries, sleepTime=sleepTime, debug=debug)


def poolLogs(name, ids, newType, poolRetries=10, sleepTime=1, debug=False):
    poolFunc = logFuncByName[name]
    idsName = idsNameByName[name]

    logCount = len(ids)
    if not ids:
        return

    time = 0
    logs = []
    foundLogs = False
    kwargs = {idsName: ids, "types": newType}
    for _ in range(poolRetries):
        sleep(sleepTime)
        time += sleepTime

        logs = list(poolFunc(**kwargs))
        foundLogs = len(logs) == logCount
        typeSet = set([log.type for log in logs])
        if not foundLogs or len(typeSet) > 1 or newType not in typeSet:
            foundLogs = False
            continue
        break

    if debug:
        print("\nLog type {}, pooling time = {}".format(newType.upper(), time))
        for log in logs:
            print(log.type.upper())

    if not foundLogs:
        raise Exception("No log with {} type found".format(newType))
