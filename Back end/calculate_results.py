from specklepy.api import operations
from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account
from specklepy.transports.server import ServerTransport
from pprint import pprint
from filter_json import filter_json_by_classification_text, get_post_by_code
import csv


# create and authenticate a client
client = SpeckleClient(host="https://speckle.xyz/")
account = get_default_account()
client.authenticate_with_account(account)

# Get a commit by its ID
STREAM_ID = "9e730f9975"
COMMIT_ID = "c6384a23fd"    # Revit Renovation
# COMMIT_ID = "a693fd7939"    # Revit New


# get the specified commit data
commit = client.commit.get(STREAM_ID, COMMIT_ID)
# create an authenticated server transport from the client and receive the commit obj
transport = ServerTransport(client=client, stream_id=STREAM_ID)
speckle_data = operations.receive(commit.referencedObject, transport)


### Calculate renovation results

# Find all walls and list their pricebook numbers
elems = []
for elem in speckle_data['@Walls']:
    materials = []
    for material in elem.materialQuantities:
        m={}
        m['name'] = material.material.name
        m['volume'] = material.volume
        materials.append(m)
    elems.append({
        "id": elem.id,
        "area": elem.parameters.HOST_AREA_COMPUTED.value,
        "code": elem.parameters.pricebook_number.value,
        "is_new": elem.parameters.IsNew.value,
        "materials": materials,
        })


# For that pricebook number, find price and GWP
for elem in elems:
    if not elem['is_new']:
        post = get_post_by_code(r"./Data/RandomPriceRenBD.json", elem["code"])
        gwp_sqm = 0
        for prop in post[0]['dynamicProperties']:
            if prop['name'][0:16] == "Global warming B":
                gwp_sqm += float(prop['value'])
        price_sqm = float(post[0]['price'])

        elem['gwp'] = gwp_sqm * elem["area"]
        elem['price'] = price_sqm * elem["area"]


### calculate new product results:

for elem in elems:
    if elem['is_new']:
        elem['gwp'] = 0
        elem['price'] = 0
        for material in elem['materials']:
            #TODO MARCINS CODE
            elem['gwp'] += gwp_sqm * material["volume"]
            elem['price'] = price_sqm * material["volume"]



