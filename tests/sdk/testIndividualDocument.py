import starkinfra
from unittest import TestCase, main
from tests.utils.individualDocument import readImage, RgImages
from tests.utils.user import exampleProject
from tests.utils.individualIdentity import generateExampleIndividualIdentityJson


starkinfra.user = exampleProject


class TestIndividualDocumentPost(TestCase):

    def test_success_and_patch_individual(self):
        identities = generateExampleIndividualIdentityJson(n=1)
        identities = starkinfra.individualidentity.create(identities=identities)
        self.assertEqual(len(identities), 1)
        self.assertIsNotNone(identities[0].id)
        
        image = readImage(RgImages["front"])
        documents = starkinfra.individualdocument.create([starkinfra.IndividualDocument(
            content=image,
            content_type="image/png",
            type="identity-front",
            identity_id=identities[0].id,
        )])
        
        self.assertIsNotNone(documents[0].id)

        image = readImage(RgImages["back"])
        documents = starkinfra.individualdocument.create([starkinfra.IndividualDocument(
            content=image,
            content_type="image/png",
            type="identity-back",
            identity_id=identities[0].id
        )])
        
        self.assertIsNotNone(documents[0].id)

        image = readImage(RgImages["selfie"])
        documents = starkinfra.individualdocument.create([starkinfra.IndividualDocument(
            content=image,
            content_type="image/png",
            type="selfie",
            identity_id=identities[0].id
        )])
        
        self.assertIsNotNone(documents[0].id)
        
        individual = starkinfra.individualidentity.update(
            id=identities[0].id,
            status="processing"
        )
        
        self.assertTrue(individual.status == "processing")


class TestIndividualDocumentQuery(TestCase):

    def test_success(self):
        identities = list(starkinfra.individualdocument.query(limit=1))
        for individual in identities:
            print(individual)
        print("Number of identities:", len(identities))


class TestIndividualDocumentPage(TestCase):

    def test_success(self):
        cursor = None
        ids = []
        for _ in range(2):
            identities, cursor = starkinfra.individualdocument.page(limit=2, cursor=cursor)
            for individual in identities:
                print(individual)
                self.assertFalse(individual.id in ids)
                ids.append(individual.id)
            if cursor is None:
                break
        self.assertEqual(len(ids), 4)


class TestIndividualDocumentInfoGet(TestCase):

    def test_success(self):
        identities = starkinfra.individualdocument.query(limit=3)
        for individual in identities:
            individual_id = individual.id
            individual_new = starkinfra.individualdocument.get(individual_id)
            self.assertEqual(individual_new.id, individual_id)


if __name__ == '__main__':
    main()
