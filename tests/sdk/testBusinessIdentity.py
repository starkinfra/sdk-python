import starkinfra
from unittest import TestCase, main
from tests.utils.user import exampleProject
from tests.utils.businessIdentity import generateExampleBusinessIdentityJson


starkinfra.user = exampleProject


class TestBusinessIdentityPost(TestCase):

    def test_success(self):
        identities = generateExampleBusinessIdentityJson(n=1)
        identities = starkinfra.businessidentity.create(identities)
        for identity in identities:
            self.assertIsNotNone(identity.id)


class TestBusinessIdentityQuery(TestCase):

    def test_success(self):
        identities = list(starkinfra.businessidentity.query(limit=1))
        for identity in identities:
            self.assertIsNotNone(identity.id)


class TestBusinessIdentityPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            identities, cursor = starkinfra.businessidentity.page(limit=2, cursor=cursor)
            for identity in identities:
                self.assertFalse(identity.id in ids)
                ids.append(identity.id)
            if cursor is None:
                break
        self.assertEqual(len(ids), 4)


class TestBusinessIdentityInfoGet(TestCase):

    def test_success(self):
        identities = starkinfra.businessidentity.query(limit=3)
        for identity in identities:
            identity_id = identity.id
            identity_new = starkinfra.businessidentity.get(identity_id)
            self.assertEqual(identity_new.id, identity_id)


class TestBusinessIdentityUpdate(TestCase):

    def test_success(self):
        identities = starkinfra.businessidentity.query(limit=1)
        for identity in identities:
            identity = starkinfra.businessidentity.update(id=identity.id, tags=identity.tags)
            self.assertIsNotNone(identity.id)


class TestBusinessIdentityCancel(TestCase):

    def test_success(self):
        identities = generateExampleBusinessIdentityJson(n=1)
        identities = starkinfra.businessidentity.create(identities)
        identity_id = identities[0].id
        identity = starkinfra.businessidentity.cancel(id=identity_id)
        self.assertEqual(identity.id, identity_id)


if __name__ == '__main__':
    main()
