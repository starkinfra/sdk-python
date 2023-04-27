from copy import deepcopy
from starkinfra import IssuingEmbossingRequest, issuingholder, issuingcard, issuingembossingkit
from tests.utils.card import generateExampleCardsJson
from tests.utils.holder import generateExampleHoldersJson

example_embossing_request = IssuingEmbossingRequest(
    card_id="9898989898989898",
    kit_id="9898989898989898",
    display_name_1="Eren Jaeger",
    shipping_city="Paradis Island",
    shipping_country_code="BRA",
    shipping_district="Shiganshina",
    shipping_service="loggi", 
    shipping_state_code="SP",
    shipping_street_line_1="Wall Maria",
    shipping_street_line_2="Wall Rose",
    shipping_tracking_number="1234567890",
    shipping_zip_code="12345-678",
    embosser_id="5746980898734080"
)


def generateExampleEmbossingRequestsJson(n=1):
    requests = []
    kit = next(issuingembossingkit.query(limit=1))
    holder = issuingholder.create(generateExampleHoldersJson())[0]
    for _ in range(n):
        card = issuingcard.create(cards=generateExampleCardsJson(n=1, holder=holder, product_id="52233227", type="physical"))[0]
        example_embossing_request.card_id = card.id
        example_embossing_request.kit_id = kit.id
        requests.append(deepcopy(example_embossing_request))
    return requests
