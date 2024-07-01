import starkinfra
from datetime import datetime
from unittest import TestCase, main
from tests.utils.date import randomPastDate
from tests.utils.user import exampleProject
from uuid import uuid4 as uuid


starkinfra.user = exampleProject


class TestJokerGet(TestCase):

    def test_get_page(self):
        example_id = starkinfra.request.get(
            path=f'/pix-request/',
            query={"limit": 1},
        ).json()["requests"][0]["id"]

        request = starkinfra.request.get(
            path=f'/pix-request/{example_id}',
            user=exampleProject
        ).json()
        self.assertEqual(request["request"]["id"], example_id)

    def test_get_pagination(self):
        after = randomPastDate(days=100)
        before = datetime.today().date()
        total_items = 0
        cursor = None
        i = 0
        ids = []
        while i <= 2:
            request = starkinfra.request.get(
                path=f'/pix-request/',
                query={
                    "after": after,
                    "before": before,
                    "cursor": cursor
                }
            ).json()
            cursor = request["cursor"]
            total_items += len(request["requests"])
            for item in request["requests"]:
                self.assertFalse(item["id"] in ids)
                ids.append(item["id"])
            if cursor is None:
                break
            i += 1
        self.assertTrue(len(ids) <= 200)


class TestJokerPostAndDelete(TestCase):

    def test_post(self):
        ext_id = str(uuid())
        data = {
            "holders": [
                {
                    "name": "Jaime Lannister",
                    "externalId": ext_id,
                    "taxId": "012.345.678-90"
                }
            ]
        }
        request = starkinfra.request.post(
            path="/issuing-holder",
            body=data,
        ).json()
        example_id = request["holders"][0]["id"]
        created_example = starkinfra.request.get(
            path=f'/issuing-holder/{example_id}'
        ).json()["holder"]["externalId"]
        self.assertEqual(created_example, str(ext_id))

        request = starkinfra.request.delete(
            path=f'/issuing-holder/{example_id}'
        ).json()
        self.assertEqual(request["holder"]["status"], "canceled")


class TestJokerPatch(TestCase):

    def test_patch(self):
        test_assertion = str(uuid())
        example_id = starkinfra.request.get(
            path=f'/issuing-holder/',
            query={"limit": 1, "status": "active"}
        ).json()["holders"][0]["id"]
        starkinfra.request.patch(
            path=f'/issuing-holder/{example_id}',
            body={
                "tags": [test_assertion]
            }
        ).json()
        final_state = starkinfra.request.get(
            path=f'/issuing-holder/{example_id}',
        ).json()
        self.assertEqual(final_state["holder"]["tags"],[test_assertion])


if __name__ == '__main__':
    main()
