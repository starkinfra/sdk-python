from .bacenid import create as _create_bacen_id


def create(bank_code, prefix):
    """
    Generates a random Pix subscription bacenId based on your bank code (ISPB)
    ## Parameters (required):
    - bank_code [string]: Your bank code (ISPB). ex: "20018183"
    - prefix [string]: Subscription prefix. ex: "RR"
    ## Return:
    - Random bacenId based on your bank code.
    """
    return prefix + _create_bacen_id(bank_code, "%Y%m%d")
