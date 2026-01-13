from starkcore.utils.subresource import SubResource


class Transaction(SubResource):
    """# PixDispute.Transaction object
    Transaction object related to the PixDispute.
    ## Attributes (return-only):
    - end_to_end_id [string]: Central Bank's unique transaction id. ex: "E79457883202101262140HHX553UPqeq"
    - amount [integer]: refundable amount. ex: 11234 (= R$ 112.34)
    - nominal_amount [integer]: transaction amount. ex: 11234 (= R$ 112.34)
    - receiver_type [string]: receiver person type. Options: "individual", "business"
    - receiver_tax_id_created [string]: receiver's taxId creation date. For business type only.
    - receiver_account_created [string]: receiver's account creation date.
    - receiver_bank_code [string]: receiver's bank code. ex: "20018183"
    - receiver_id [string]: identifier of accountholder in the graph.
    - sender_type [string]: sender person type. Options: "individual", "business"
    - sender_tax_id_created [string]: sender's taxId creation date. For business type only.
    - sender_account_created [string]: sender's account creation date.
    - sender_bank_code [string]: sender's bank code. ex: "20018183"
    - sender_id [string]: identifier of accountholder in the graph.
    - settled [datetime.datetime]: settled datetime of the transaction. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, end_to_end_id=None, amount=None, nominal_amount=None, receiver_type=None,
                 receiver_tax_id_created=None, receiver_account_created=None, receiver_bank_code=None,
                 receiver_id=None, sender_type=None, sender_tax_id_created=None, sender_account_created=None,
                 sender_bank_code=None, sender_id=None, settled=None):
        self.end_to_end_id = end_to_end_id
        self.amount = amount
        self.nominal_amount = nominal_amount
        self.receiver_type = receiver_type
        self.receiver_tax_id_created = receiver_tax_id_created
        self.receiver_account_created = receiver_account_created
        self.receiver_bank_code = receiver_bank_code
        self.receiver_id = receiver_id
        self.sender_type = sender_type
        self.sender_tax_id_created = sender_tax_id_created
        self.sender_account_created = sender_account_created
        self.sender_bank_code = sender_bank_code
        self.sender_id = sender_id
        self.settled = settled


_sub_resource = {"class": Transaction, "name": "Transaction"}
