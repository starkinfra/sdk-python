import starkinfra
from unittest import TestCase, main
from datetime import timedelta, date
from tests.utils.user import exampleProject
from starkcore.error import InputErrors
from tests.utils.pixPullRequest import generateExamplePixPullRequestJson


starkinfra.user = exampleProject


class TestPixPullRequestPost(TestCase):
    def test_success(self):
        active_subs = list(starkinfra.pixpullsubscription.query(status=["active"], limit=1))
        if not active_subs:
            self.skipTest("no active subscriptions available to create pull requests against")
        subscription_id = active_subs[0].id
        requests = generateExamplePixPullRequestJson(subscription_id=subscription_id, n=2)
        requests = starkinfra.pixpullrequest.create(requests)
        for request in requests:
            check = starkinfra.pixpullrequest.get(request.id)
            self.assertEqual(check.id, request.id)


class TestPixPullRequestQuery(TestCase):

    def test_success(self):
        requests = list(starkinfra.pixpullrequest.query(limit=10))
        self.assertLessEqual(len(requests), 10)

    def test_success_with_params(self):
        requests = starkinfra.pixpullrequest.query(
            limit=10,
            after=date.today() - timedelta(days=100),
            before=date.today(),
            status=["created"],
            tags=["iron"],
            ids=["1", "2", "3"],
            subscription_ids=["1", "2"],
            flows=["out"],
        )
        self.assertEqual(len(list(requests)), 0)


class TestPixPullRequestPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            requests, cursor = starkinfra.pixpullrequest.page(limit=2, cursor=cursor)
            for request in requests:
                self.assertFalse(request.id in ids)
                ids.append(request.id)
            if cursor is None:
                break
        self.assertTrue(len(ids) <= 4)


class TestPixPullRequestInfoGet(TestCase):

    def test_success(self):
        requests = starkinfra.pixpullrequest.query(limit=1)
        request = next(requests, None)
        if request is None:
            self.skipTest("no requests available to fetch")
        result = starkinfra.pixpullrequest.get(id=request.id)
        self.assertEqual(result.id, request.id)


class TestPixPullRequestPatch(TestCase):

    def test_success(self):
        requests = starkinfra.pixpullrequest.query(status=["created"], limit=1)
        request = next(requests, None)
        if request is None:
            self.skipTest("no created requests available to patch")
        try:
            updated = starkinfra.pixpullrequest.update(
                id=request.id,
                status="denied",
                reason="senderAccountClosed",
            )
        except InputErrors as error:
            self.assertTrue(len(error.errors) > 0)
            return
        self.assertEqual(updated.id, request.id)


class TestPixPullRequestCancel(TestCase):

    def test_success(self):
        requests = starkinfra.pixpullrequest.query(status=["created"], limit=1)
        request = next(requests, None)
        if request is None:
            self.skipTest("no created requests available to cancel")
        try:
            canceled = starkinfra.pixpullrequest.cancel(
                id=request.id,
                reason="senderUserRequested",
            )
        except InputErrors as error:
            self.assertTrue(len(error.errors) > 0)
            return
        self.assertEqual(canceled.id, request.id)


if __name__ == '__main__':
    main()
