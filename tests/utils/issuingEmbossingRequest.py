from copy import deepcopy
from starkinfra import IssuingEmbossingRequest, issuingholder, issuingcard
from tests.utils.card import generateExampleCardsJson


example_embossing_request = IssuingEmbossingRequest(
    card_id="5699347823984640", 
    card_design_id="5648359658356736", 
    display_name_1="teste", 
    envelope_design_id="5747368922185728", 
    shipping_city="Sao Paulo", 
    shipping_country_code="BRA", 
    shipping_district="Bela Vista", 
    shipping_service="loggi", 
    shipping_state_code="SP", 
    shipping_street_line_1="teste", 
    shipping_street_line_2="teste", 
    shipping_tracking_number="teste", 
    shipping_zip_code="12345-678",
    embosser_id="5746980898734080"
)


def generateExampleEmbossingRequestsJson(n=1):
    requests = []
    holder = next(issuingholder.query(limit=1))
    for _ in range(n):
        card = issuingcard.create(cards=generateExampleCardsJson(n=1, holder=holder, bin_id="52233227", type="physical"))[0]
        example_embossing_request.card_id = card.id
        requests.append(deepcopy(example_embossing_request))
    return requests
