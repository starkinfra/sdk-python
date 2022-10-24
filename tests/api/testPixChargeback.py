import starkinfra
from unittest import TestCase, main
from tests.utils.user import exampleProject
from tests.utils.pixChargeback import generateExamplePixChargebacksJson
from tests.utils.poolingEntities import poolEntities, poolLogs, poolLogsByTypes


starkinfra.user = exampleProject
name = "PixChargeback"
debug = True


class TestPixChargebackPost(TestCase):
    def test_success(self):
        reasons = ["flaw", "fraud", "reversalChargeback"]
        chargebackCount = len(reasons)

        allChargebacks = []
        for reason in reasons:
            chargebacks = generateExamplePixChargebacksJson(1, reason=reason)
            chargebacks = starkinfra.pixchargeback.create(chargebacks)
            allChargebacks.extend(chargebacks)

        if debug:
            for chargeback in allChargebacks:
                print(chargeback)

        self.assertEqual(len(allChargebacks), chargebackCount)
        self.assertNotEqual(len(allChargebacks), 0)
        ids = [chargeback.id for chargeback in allChargebacks]

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
            entityCount=chargebackCount,
            debug=debug,
        )
        chargebacks = list(starkinfra.pixchargeback.query(ids=ids))
        cancelChargebacks(chargebacks)


class CancelRegisteredChargebacks(TestCase):
    def test_cancel(self):
        limit = 2

        chargebacks = list(starkinfra.pixchargeback.query(
            status=["delivered", "created"],
            flow="out",
            limit=limit,
        ))
        self.assertNotEqual(len(chargebacks), 0)
        cancelChargebacks(chargebacks)


def cancelChargebacks(chargebacks):
    for chargeback in chargebacks:
        starkinfra.pixchargeback.cancel(id=chargeback.id)

    poolEntities(
        name=name,
        ids=[chargeback.id for chargeback in chargebacks],
        newStatus="canceled",
        debug=debug,
    )
    poolLogs(
        name=name,
        ids=[chargeback.id for chargeback in chargebacks],
        newType="canceled",
        debug=debug,
    )


if __name__ == '__main__':
    main()
