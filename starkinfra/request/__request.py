from ..utils import rest
from starkinfra import request_methods_prefix


def get(path, query=None, user=None):
    """# Retrieve any StarkInfra resource
    Receive a json of resources previously created in StarkInfra's API
    ## Parameters (required):
    - path [string]: StarkInfra resource's route. ex: "/pix-request/"
    - query [dict, default None]: Query parameters. ex: {"limit": 1, "status": paid}
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if StarkInfra.user
        was set before function call
    ## Return:
    - dict of StarkInfra objects with updated attributes
    """
    return rest.get_raw(
        path=path,
        query=query,
        user=user,
        prefix=request_methods_prefix,
        raiseException=False
    )


def post(path, body=None, query=None, user=None):
    """# Create any StarkInfra resource
    Send a list of jsons and create any StarkInfra resource objects
    ## Parameters (required):
    - path [string]: StarkInfra resource's route. ex: "/pix-request/"
    - body [dict]: request parameters. ex: {"requests": [{"amount": 100, "name": "Iron Bank S.A.", "taxId": "20.018.183/0001-80"}]}
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if StarkInfra.user
        was set before function call
    - query [dict, default None]: Query parameters. ex: {"limit": 1, "status": paid}
    ## Return:
    - list of resources jsons with updated attributes
    """
    return rest.post_raw(
        path=path,
        payload=body,
        query=query,
        user=user,
        prefix=request_methods_prefix,
        raiseException=False
    )


def patch(path, body=None, user=None):
    """# Update any StarkInfra resource
    Send a json with parameters of a single StarkInfra resource object and update it
    ## Parameters (required):
    - path [string]: StarkInfra resource's route. ex: "/pix-request/5699165527090460"
    - body [dict]: request parameters. ex: {"amount": 100}
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if StarkInfra.user
        was set before function call
    ## Return:
    - json of the resource with updated attributes
    """
    return rest.patch_raw(
        path=path,
        payload=body,
        user=user,
        prefix=request_methods_prefix,
        raiseException=False
    )


def put(path, body=None, user=None):
    """# Put any StarkInfra resource
        Send a json with parameters of a single StarkInfra resource object and create it, if the resource alredy exists,
        you will update it.
        ## Parameters (required):
        - path [string]: StarkInfra resource's route. ex: "/pix-request"
        - body [dict]: request parameters. ex: {"amount": 100}
        ## Parameters (optional):
        - user [Organization/Project object, default None]: Organization or Project object. Not necessary if StarkInfra.user
            was set before function call
        ## Return:
        - json of the resource with updated attributes
        """
    return rest.put_raw(
        path=path,
        payload=body,
        user=user,
        prefix=request_methods_prefix,
        raiseException=False
    )


def delete(path, body=None, user=None):
    """# Delete any StarkInfra resource
        Send a json with parameters of a single StarkInfra resource object and delete it
        you will update it.
        ## Parameters (required):
        - path [string]: StarkInfra resource's route. ex: "/pix-request/5699165527090460"
        - body [dict]: request parameters. ex: {"amount": 100}
        ## Parameters (optional):
        - user [Organization/Project object, default None]: Organization or Project object. Not necessary if StarkInfra.user
            was set before function call
        ## Return:
        - json of the resource with updated attributes
        """
    return rest.delete_raw(
        path=path,
        payload=body,
        user=user,
        prefix=request_methods_prefix,
        raiseException=False
    )
