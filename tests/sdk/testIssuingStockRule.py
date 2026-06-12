import starkinfra
from unittest import TestCase, main
from datetime import date, timedelta
from tests.utils.user import exampleProject
from tests.utils.issuingStockRule import generateExampleStockRulesJson

starkinfra.user = exampleProject


class TestIssuingStockRuleQuery(TestCase):

    def test_success(self):
        rules = starkinfra.issuingstockrule.query(
            limit=10,
            after=date.today() - timedelta(days=100),
            before=date.today(),
        )
        for rule in rules:
            self.assertEqual(rule.id, str(rule.id))


class TestIssuingStockRulePage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            rules, cursor = starkinfra.issuingstockrule.page(
                limit=2,
                after=date.today() - timedelta(days=100),
                before=date.today(),
                cursor=cursor
            )
            for rule in rules:
                self.assertFalse(rule.id in ids)
                ids.append(rule.id)
            if cursor is None:
                break


class TestIssuingStockRuleGet(TestCase):

    def test_success(self):
        rules = starkinfra.issuingstockrule.query(limit=1)
        rule = starkinfra.issuingstockrule.get(id=next(rules).id)
        self.assertEqual(rule.id, str(rule.id))


class TestIssuingStockRulePostPatchAndDelete(TestCase):

    def test_success(self):
        rules = starkinfra.issuingstockrule.create(generateExampleStockRulesJson(n=1))
        rule_id = rules[0].id
        rule = starkinfra.issuingstockrule.update(id=rule_id, minimum_balance=20000)
        self.assertEqual(20000, rule.minimum_balance)
        rule = starkinfra.issuingstockrule.cancel(id=rule_id)
        self.assertEqual("canceled", rule.status)


if __name__ == '__main__':
    main()
