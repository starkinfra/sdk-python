import starkinfra
from unittest import TestCase, main
from tests.utils.user import exampleProject
from tests.utils.individualIdentity import generateExampleIndividualIdentityJson


starkinfra.user = exampleProject


class TestIndividualIdentityPost(TestCase):

    def test_success(self):
        identities = generateExampleIndividualIdentityJson(n=1)
        identities = starkinfra.individualidentity.create(identities)
        for individual in identities:
            self.assertIsNotNone(individual.id)


class TestIndividualIdentityQuery(TestCase):

    def test_success(self):
        identities = list(starkinfra.individualidentity.query(limit=1))
        for individual in identities:
            print(individual)
        print("Number of identities:", len(identities))


class TestIndividualIdentityPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            identities, cursor = starkinfra.individualidentity.page(limit=2, cursor=cursor)
            for individual in identities:
                print(individual)
                self.assertFalse(individual.id in ids)
                ids.append(individual.id)
            if cursor is None:
                break
        self.assertEqual(len(ids), 4)


class TestIndividualIdentityInfoGet(TestCase):

    def test_success(self):
        identities = starkinfra.individualidentity.query(limit=3)
        for individual in identities:
            individual_id = individual.id
            individual_new = starkinfra.individualidentity.get(individual_id)
            self.assertEqual(individual_new.id, individual_id)


class TestIndividualIdentityPostAndCancel(TestCase):
    
    def test_success(self):
        identities = generateExampleIndividualIdentityJson(n=1)
        identities = starkinfra.individualidentity.create(identities)
        individual_id = identities[0].id
        individual = starkinfra.individualidentity.cancel(id=individual_id)
        print(individual.id)


if __name__ == '__main__':
    main()
