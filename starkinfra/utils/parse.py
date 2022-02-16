from ..utils import cache
from ..utils.request import fetch
from json import loads, dumps
from requests import get as get_request
from ellipticcurve import Ecdsa, PublicKey, Signature
from ..utils.api import from_api_json
from ..error import InvalidSignatureError


def parse_and_verify(content, signature, user, _resource, key=None):

    request = from_api_json(_resource, loads(content))
    if key is not None:
        request = from_api_json(_resource, loads(content)[key])

    try:
        signature = Signature.fromBase64(signature)
    except:
        raise InvalidSignatureError("The provided signature is not valid")

    public_key = get_public_key(user=user)
    if is_valid(content=content, signature=signature, public_key=public_key):
        return request

    public_key = get_public_key(user=user, refresh=True)
    if is_valid(content=content, signature=signature, public_key=public_key):
        return request

    raise InvalidSignatureError("The provided signature and content do not match the Stark Infra public key")


def is_valid(content, signature, public_key):
    if Ecdsa.verify(message=content, signature=signature, publicKey=public_key):
        return True

    normalized = dumps(loads(content), sort_keys=True)
    if Ecdsa.verify(message=normalized, signature=signature, publicKey=public_key):
        return True

    return False


def get_public_key(user, refresh=False):
    public_key = cache.get("starkinfra-public-key")
    if public_key and not refresh:
        return public_key

    pem = fetch(method=get_request, path="/public-key", query={"limit": 1}, user=user).json()["publicKeys"][0]["content"]
    public_key = PublicKey.fromPem(pem)
    cache["starkinfra-public-key"] = public_key
    return public_key
