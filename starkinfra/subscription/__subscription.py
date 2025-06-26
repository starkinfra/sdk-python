from starkcore.utils.subresource import SubResource
from starkcore.utils.checks import check_datetime_or_date


class Subscription(SubResource):
    """# Subscription object
    Subscription is a recurring payment that can be used to charge a user periodically.
    ## Attributes (return-only):
    - amount [integer]: amount to be charged in cents. ex: 1000 = R$ 10.00
    - amount_min_limit [integer]: minimum amount limit for the subscription. ex: 500 = R$ 5.00
    - bacen_id [string]: BACEN (Brazilian Central Bank) identifier.
    - created [datetime.datetime]: creation datetime for the subscription. ex: datetime(2020, 3, 10)
    - description [string]: description of the subscription.
    - installment_end [datetime.datetime]: end datetime for the installments. ex: datetime(2020, 3, 10)
    - installment_start [datetime.datetime]: start datetime for the installments. ex: datetime(2020, 3, 10)
    - interval [string]: interval for the recurring charge. ex: "monthly"
    - pull_retry_limit [integer]: maximum number of retries for pulling the payment.
    - receiver_bank_code [string]: bank code of the receiver.
    - receiver_name [string]: name of the receiver.
    - receiver_tax_id [string]: tax ID of the receiver.
    - reference_code [string]: reference code for the subscription.
    - sender_final_name [string]: final sender name.
    - sender_final_tax_id [string]: final sender tax ID.
    - status [string]: current status of the subscription.
    - type [string]: type of the subscription.
    - updated [datetime.datetime]: last update datetime for the subscription. ex: datetime(2020, 3, 10)
    """

    def __init__(self, amount, amount_min_limit=None, bacen_id=None, created=None, description=None,
        installment_end=None, installment_start=None, interval=None, pull_retry_limit=None, receiver_bank_code=None,
        receiver_name=None, receiver_tax_id=None, reference_code=None, sender_final_name=None, sender_final_tax_id=None,
        status=None, type=None, updated=None
    ):
        self.amount = amount
        self.amount_min_limit = amount_min_limit
        self.bacen_id = bacen_id
        self.created = check_datetime_or_date(created)
        self.description = description
        self.installment_end = check_datetime_or_date(installment_end)
        self.installment_start = check_datetime_or_date(installment_start)
        self.interval = interval
        self.pull_retry_limit = pull_retry_limit
        self.receiver_bank_code = receiver_bank_code
        self.receiver_name = receiver_name
        self.receiver_tax_id = receiver_tax_id
        self.reference_code = reference_code
        self.sender_final_name = sender_final_name
        self.sender_final_tax_id = sender_final_tax_id
        self.status = status
        self.type = type
        self.updated = check_datetime_or_date(updated)


_resource = {"class": Subscription, "name": "Subscription"}
