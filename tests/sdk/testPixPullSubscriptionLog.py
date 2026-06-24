import starkinfra
from unittest import TestCase, main
from tests.utils.user import exampleProject


starkinfra.user = exampleProject


class TestPixPullSubscriptionLogQuery(TestCase):

    def test_success(self):
        logs = list(starkinfra.pixpullsubscription.log.query(limit=10))
        self.assertLessEqual(len(logs), 10)


class TestPixPullSubscriptionLogPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            logs, cursor = starkinfra.pixpullsubscription.log.page(limit=2, cursor=cursor)
            for log in logs:
                self.assertFalse(log.id in ids)
                ids.append(log.id)
            if cursor is None:
                break
        self.assertTrue(len(ids) <= 4)


class TestPixPullSubscriptionLogInfoGet(TestCase):

    def test_success(self):
        logs = starkinfra.pixpullsubscription.log.query(limit=1)
        log = next(logs, None)
        if log is None:
            self.skipTest("no logs available to fetch")
        result = starkinfra.pixpullsubscription.log.get(id=log.id)
        self.assertEqual(log.id, result.id)


class TestPixPullSubscriptionLogFilter(TestCase):

    def test_query_by_subscription_ids(self):
        subscriptions = list(starkinfra.pixpullsubscription.query(limit=1))
        if not subscriptions:
            self.skipTest("no subscriptions available to filter logs by")
        target_id = subscriptions[0].id
        logs = list(starkinfra.pixpullsubscription.log.query(
            limit=5,
            subscription_ids=[target_id],
        ))
        for log in logs:
            self.assertEqual(log.subscription.id, target_id)


if __name__ == '__main__':
    main()
