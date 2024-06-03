from starkcore.utils.subresource import SubResource


class Statistic(SubResource):
    """# PixUser.Statistic object
    The PixUser.Statistic object modifies the behavior of Invoice objects when passed as an argument upon their creation.
    ## Parameters (required):
    - after [datetime.datetime]: start date filter for the first element count of this element. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - source [string]: source of the statistic. ex: "pix-key", "pix-request", "pix-fraud", "pix-infraction"...
    - type [string]: type of the statistic source. ex: "registered", "settled", "scam", "mule", "amount", "open", "denied"
    - updated [datetime.datetime]: latest update datetime for the Statistic object. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - value [integer]: Entity tyoe counter between after and updated. ex: 1234
    """

    def __init__(self, after, source, type, updated, value):
        self.after = after
        self.source = source
        self.type = type
        self.updated = updated
        self.value = value


_sub_resource = {"class": Statistic, "name": "Statistic"}
