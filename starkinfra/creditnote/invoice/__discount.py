from starkcore.utils.subresource import SubResource


class Discount(SubResource):
    """# creditnote.invoice.Discount object
    Invoice discount information.
    ## Parameters (required):
    - percentage [float]: percentage of discount applied until specified due date
    - due [datetime.datetime or string]: due datetime for the discount
    """

    def __init__(self, percentage, due):
        self.percentage = percentage
        self.due = due


resource = {"class": Discount, "name": "Discount"}
