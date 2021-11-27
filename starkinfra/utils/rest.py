import starkinfra
import starkbank
from starkbank.utils import rest


def relaySettings(func):
    def wrapper(*args, **kwargs):
        starkbank.user = starkinfra.user
        starkbank.language = starkinfra.language
        starkbank.timeout = starkinfra.timeout
        return func(*args, **kwargs)
    return wrapper


get_page = relaySettings(rest.get_page)
get_stream = relaySettings(rest.get_stream)
get_id = relaySettings(rest.get_id)
get_content = relaySettings(rest.get_content)
get_sub_resource = relaySettings(rest.get_sub_resource)
get_sub_resources = relaySettings(rest.get_sub_resources)
post_multi = relaySettings(rest.post_multi)
post_single = relaySettings(rest.post_single)
delete_id = relaySettings(rest.delete_id)
patch_id = relaySettings(rest.patch_id)
