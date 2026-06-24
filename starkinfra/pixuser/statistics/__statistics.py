from starkcore.utils.subresource import SubResource
from starkcore.utils.checks import check_datetime


class Statistics(SubResource):
    """# PixUser.Statistics object
    The PixUser.Statistics object stores fraud statistics data of a Pix user.
    ## Attributes (return-only):
    - value [integer]: aggregated value of the statistic. ex: 3
    - type [string]: type of the statistic. ex: "infractions"
    - source [string]: source of the statistic. ex: "keyManagement"
    - after [datetime.datetime]: start datetime considered for the statistic aggregation. ex: datetime.datetime(2020, 4, 23, 23, 0, 0)
    - updated [datetime.datetime]: latest update datetime for the statistic. ex: datetime.datetime(2020, 4, 23, 23, 0, 0)
    """

    def __init__(self, value=None, type=None, source=None, after=None, updated=None):
        self.value = value
        self.type = type
        self.source = source
        self.after = check_datetime(after)
        self.updated = check_datetime(updated)


_sub_resource = {"class": Statistics, "name": "Statistics"}
