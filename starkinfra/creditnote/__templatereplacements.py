from starkcore.utils.subresource import SubResource


class TemplateReplacements(SubResource):
    """# creditnote.TemplateReplacements object
    The creditnote.TemplateReplacements object carries the custom values used to fill the placeholders
    of the contract template of a CreditNote. Its attributes are free: they depend on the template.
    ## Parameters (optional):
    - **kwargs [string]: placeholder name and its value. Write the names in snake_case: they are converted to
        camelCase when sent, and values that are None are not sent.
        Names starting with an underscore are not allowed. ex: guarantor_name="Jon Snow"
    One dict may also be passed as the only positional argument, and the keyword arguments win over its keys.
    """

    def __init__(*args, **kwargs):
        # self comes from args so that a placeholder named "self" does not collide with it (Python 3.4+)
        self = args[0]
        values = dict(_positional_values(args[1:]))
        values.update(kwargs)
        for key, value in values.items():
            if key.startswith("_"):
                raise ValueError("template replacement names cannot start with an underscore: {key}".format(key=key))
            setattr(self, key, value)


def _positional_values(args):
    # Accepts at most one dict, like dict() does, so the usage from the other SDKs does not silently produce an empty object
    if len(args) == 0:
        return {}
    if len(args) > 1 or not isinstance(args[0], dict):
        raise TypeError("TemplateReplacements takes at most one positional dict, plus keyword arguments, got: {types}".format(
            types=", ".join(type(arg).__name__ for arg in args)
        ))
    return args[0]
