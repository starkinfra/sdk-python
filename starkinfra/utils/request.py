from time import time
from json import dumps, loads
from ellipticcurve import Ecdsa
from sys import version_info as python_version
from ..environment import Environment
from ..error import InternalServerError, InputErrors, UnknownError
from .url import urlencode
from .checks import check_user, check_language
import starkinfra


class Response:

    def __init__(self, status, content):
        self.status = status
        self.content = content

    def json(self):
        return loads(self.content.decode("utf-8"))


def fetch(method, path, payload=None, query=None, user=None, version="v2"):
    user = check_user(user or starkinfra.user)
    language = check_language(starkinfra.language)

    url = {
        Environment.production:  "https://api.starkinfra.com/",
        Environment.sandbox:     "https://sandbox.api.starkinfra.com/",
        Environment.development: "https://development.api.starkinfra.com/",
    }[user.environment] + version

    url = "{base_url}/{path}{query}".format(base_url=url, path=path, query=urlencode(query))

    agent = "Python-{major}.{minor}.{micro}-SDK-{sdk_version}".format(
        major=python_version.major,
        minor=python_version.minor,
        micro=python_version.micro,
        sdk_version=starkinfra.version,
    )

    access_time = str(time())
    body = dumps(payload) if payload else ""
    message = "{access_id}:{access_time}:{body}".format(access_id=user.access_id(), access_time=access_time, body=body)
    signature = Ecdsa.sign(message=message, privateKey=user.private_key()).toBase64()

    try:
        request = method(
            url=url,
            data=body,
            headers={
                "Access-Id": user.access_id(),
                "Access-Time": access_time,
                "Access-Signature": signature,
                "Content-Type": "application/json",
                "User-Agent": agent,
                "Accept-Language": language,
            },
            timeout=starkinfra.timeout
        )
    except Exception as exception:
        raise UnknownError("{}: {}".format(exception.__class__.__name__, str(exception)))

    response = Response(status=request.status_code, content=request.content)

    if response.status == 500:
        raise InternalServerError()
    if response.status == 400:
        raise InputErrors(response.json()["errors"])
    if response.status != 200:
        raise UnknownError(response.content)

    return response
