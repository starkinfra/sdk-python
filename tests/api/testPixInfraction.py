import starkinfra
from random import choice
from unittest import TestCase, main
from tests.utils.user import exampleProject
from tests.utils.pixInfraction import generateExamplePixInfractionsJson
from tests.utils.poolingEntities import poolEntities, poolLogs, poolLogsByTypes


starkinfra.user = exampleProject
name = "PixInfraction"
debug = True


class TestPixInfractionPost(TestCase):
    def test_success(self):
        infractionCount = 4

        allInfractions = []
        for _ in range(infractionCount):
            infractionType = choice(["reversal", "reversalChargeback", "fraud"])
            infractions = generateExamplePixInfractionsJson(n=1, infractionType=infractionType)
            infractions = starkinfra.pixinfraction.create(infractions)
            allInfractions.extend(infractions)

        if debug:
            for infraction in allInfractions:
                print(infraction)

        self.assertEqual(len(allInfractions), infractionCount)
        self.assertNotEqual(len(allInfractions), 0)
        ids = [infraction.id for infraction in allInfractions]

        poolLogsByTypes(
            name=name,
            ids=ids,
            newTypes=["created", "delivering", "delivered"],
            debug=debug,
        )

        poolEntities(
            name=name,
            ids=ids,
            newStatus="delivered",
            entityCount=infractionCount,
            debug=debug,
        )
        infractions = list(starkinfra.pixinfraction.query(ids=ids))
        cancelInfractions(infractions)


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


if __name__ == '__main__':
    main()
