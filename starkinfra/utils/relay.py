import starkinfra
from starkcore.utils.host import StarkHost


_api_version = "v2"


def set_relay(func):
    def wrapper(*args, **kwargs):
        kwargs.update({
            "sdk_version": starkinfra.version,
            "host": StarkHost.infra,
            "api_version": kwargs.get("version") or _api_version,
            "user": kwargs.get("user") or starkinfra.user,
            "language": kwargs.get("language") or starkinfra.language,
            "timeout": kwargs.get("timeout") or starkinfra.timeout,
        })
        return func(*args, **kwargs)
    return wrapper
