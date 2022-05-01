from .bacenid import create as _create_bacen_id


def create(bank_code):
    """
    Generates a random return-id based on your bank code (ISPB)
    ## Parameters (required):
    - bank_code [string]: Your bank code (ISPB). ex: "20018183"
    ## Return:
    - Random returnId based on your bank code.
    """
    return "D" + _create_bacen_id(bank_code)
