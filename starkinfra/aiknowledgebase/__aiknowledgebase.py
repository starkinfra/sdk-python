from ..utils import rest
from starkcore.utils.api import from_api_json, api_json, endpoint
from starkcore.utils.case import camel_to_snake
from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime


class AiKnowledgeBase(Resource):
    """# AiKnowledgeBase object
    An AiKnowledgeBase turns a website into material an AiAgent can read. You give it a root URL; Stark Infra
    crawls the page, follows its links, converts everything to Markdown and indexes it for retrieval.
    When you initialize an AiKnowledgeBase, the entity will not be automatically
    created in the Stark Infra API. The 'create' function sends the object
    to the Stark Infra API and returns the created object.
    ## Parameters (required):
    - name [string]: name of the knowledge base. Between 1 and 100 characters. ex: "Product Documentation"
    - root_url [string]: absolute http or https URL the crawl starts from. ex: "https://docs.starkinfra.com"
    ## Parameters (optional):
    - is_recursive [bool, default None]: whether the crawl may follow links into other subdomains of the root URL's registered domain. The API defaults to True. ex: False
    - tags [list of strings, default None]: list of up to 100 strings for reference when searching for AiKnowledgeBases. ex: ["support", "public"]
    ## Attributes (return-only):
    - id [string]: unique id returned when the AiKnowledgeBase is created. ex: "5656565656565656"
    - status [string]: current status of the knowledge base. Options: "processing", "success", "failed". An agent retrieves from a base only once it reaches "success".
    - created [datetime.datetime]: creation datetime for the AiKnowledgeBase. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - updated [datetime.datetime]: latest update datetime for the AiKnowledgeBase. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, name, root_url, is_recursive=None, tags=None, id=None, status=None, created=None,
                 updated=None):
        Resource.__init__(self, id=id)

        self.name = name
        self.root_url = root_url
        self.is_recursive = is_recursive
        self.tags = tags
        self.status = status
        self.created = check_datetime(created)
        self.updated = check_datetime(updated)


_resource = {"class": AiKnowledgeBase, "name": "AiKnowledgeBase"}


def create(knowledge_base, user=None):
    """# Create an AiKnowledgeBase
    Send an AiKnowledgeBase object for creation at the Stark Infra API and start crawling it.
    The call returns immediately with the knowledge base in "processing" status.
    ## Parameters (required):
    - knowledge_base [AiKnowledgeBase object]: AiKnowledgeBase object to be created in the API.
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - AiKnowledgeBase object with updated attributes
    """
    response = rest.post_raw(path=endpoint(_resource), payload=api_json(knowledge_base), user=user)
    return from_api_json(_resource, response.json()["knowledgeBase"])


def get(id, user=None):
    """# Retrieve a specific AiKnowledgeBase
    Receive a single AiKnowledgeBase object previously created in the Stark Infra API by its id.
    This is the call to poll while the crawl runs.
    ## Parameters (required):
    - id [string]: object unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - AiKnowledgeBase object with updated attributes
    """
    response = rest.get_raw(path="{endpoint}/{id}".format(endpoint=endpoint(_resource), id=id), user=user)
    return from_api_json(_resource, response.json()["knowledgeBase"])


def query(limit=None, ids=None, name=None, status=None, user=None):
    """# Retrieve AiKnowledgeBases
    Receive a generator of AiKnowledgeBase objects previously created in the Stark Infra API
    ## Parameters (optional):
    - limit [integer, default None]: maximum number of objects to be retrieved. Unlimited if None. ex: 35
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - name [string, default None]: case-insensitive substring of the name to filter retrieved objects. ex: "docs"
    - status [string, default None]: filter for status of retrieved objects. Options: "processing", "success", "failed"
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - generator of AiKnowledgeBase objects with updated attributes
    """
    cursor = None
    remaining = limit
    while True:
        knowledge_bases, cursor = page(
            cursor=cursor,
            limit=min(remaining, 100) if remaining else None,
            ids=ids,
            name=name,
            status=status,
            user=user,
        )
        for knowledge_base in knowledge_bases:
            yield knowledge_base
        if remaining:
            remaining -= len(knowledge_bases)
        if not cursor or (limit and remaining <= 0):
            break


def page(cursor=None, limit=None, ids=None, name=None, status=None, user=None):
    """# Retrieve paged AiKnowledgeBases
    Receive a list of up to 100 AiKnowledgeBase objects previously created in the Stark Infra API and the cursor to the next page.
    Use this function instead of query if you want to manually page your requests.
    The name filter applies to each page, so a page can come back empty with a cursor: keep following it until the cursor is None.
    ## Parameters (optional):
    - cursor [string, default None]: cursor returned on the previous page function call
    - limit [integer, default 100]: maximum number of objects to be retrieved. Max = 100. ex: 35
    - ids [list of strings, default None]: list of ids to filter retrieved objects. ex: ["5656565656565656", "4545454545454545"]
    - name [string, default None]: case-insensitive substring of the name to filter retrieved objects. ex: "docs"
    - status [string, default None]: filter for status of retrieved objects. Options: "processing", "success", "failed"
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of AiKnowledgeBase objects with updated attributes
    - cursor to retrieve the next page of AiKnowledgeBase objects
    """
    response = rest.get_raw(
        path=endpoint(_resource),
        query={"ids": ids, "name": name, "status": status, "limit": limit, "cursor": cursor},
        user=user,
    )
    content = response.json()
    return [from_api_json(_resource, entity) for entity in content["knowledgeBases"]], content.get("cursor")


def update(id, name=None, is_recursive=None, tags=None, user=None):
    """# Update AiKnowledgeBase entity
    Rename a knowledge base, retag it or change whether its crawl is recursive. The root URL cannot be changed.
    ## Parameters (required):
    - id [string]: AiKnowledgeBase unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - name [string, default None]: new name of the knowledge base. Between 1 and 100 characters.
    - is_recursive [bool, default None]: whether the next crawl may follow links into other subdomains of the root URL's registered domain.
    - tags [list of strings, default None]: new list of up to 100 strings. Replaces the current list.
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - AiKnowledgeBase with updated attributes
    """
    payload = api_json({"name": name, "is_recursive": is_recursive, "tags": tags})
    response = rest.patch_raw(path="{endpoint}/{id}".format(endpoint=endpoint(_resource), id=id), payload=payload, user=user)
    return from_api_json(_resource, response.json()["knowledgeBase"])


def hosts(id, user=None):
    """# List the pages of an AiKnowledgeBase
    Receive every page the crawler has seen, grouped by host. While a crawl is running this is the live picture,
    merged with the last finished one.
    ## Parameters (required):
    - id [string]: AiKnowledgeBase unique id. ex: "5656565656565656"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - dict mapping each host to its list of pages. Each page is a dict with "original_url", "storage_url" and "status" ("pending", "success" or "failed")
    """
    response = rest.get_raw(path="{endpoint}/{id}/hosts".format(endpoint=endpoint(_resource), id=id), user=user)
    return {
        host: [{camel_to_snake(key): value for key, value in page.items()} for page in pages]
        for host, pages in response.json()["hosts"].items()
    }


def delete(ids, user=None):
    """# Delete AiKnowledgeBases
    Delete up to 100 AiKnowledgeBases at once. Agents still referencing a deleted base simply retrieve nothing from it.
    ## Parameters (required):
    - ids [list of strings]: ids of the AiKnowledgeBases to be deleted. Up to 100 ids. ex: ["5656565656565656", "4545454545454545"]
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starkinfra.user was set before function call.
    ## Return:
    - list of deleted AiKnowledgeBase objects
    """
    response = rest.delete_raw(path=endpoint(_resource), query={"ids": ids}, user=user)
    return [from_api_json(_resource, entity) for entity in response.json()["knowledgeBases"]]
