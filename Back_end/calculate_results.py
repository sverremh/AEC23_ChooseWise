from specklepy.api import operations
from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account
from specklepy.transports.server import ServerTransport
from pprint import pprint
from filter_json import filter_json_by_classification_text, get_post_by_code
import csv
import pandas as pd
import json


MOLIO_JSON = r"./Data/RandomPriceRenBD.json"
NEW_JSON = r"./Data/New_products.json"

# create and authenticate a client
client = SpeckleClient(host="https://speckle.xyz/")
account = get_default_account()
client.authenticate_with_account(account)

# Get a commit by its ID
STREAM_ID = "9e730f9975"
# COMMIT_ID = "c6384a23fd"    # Revit Renovation
COMMIT_ID = "c1a5d145bd"    # Revit New


# get the specified commit data
commit = client.commit.get(STREAM_ID, COMMIT_ID)
# create an authenticated server transport from the client and receive the commit obj
transport = ServerTransport(client=client, stream_id=STREAM_ID)
speckle_data = operations.receive(commit.referencedObject, transport)


### Calculate renovation results

# Find all walls and list their pricebook numbers
elems = []
# TODO walls, Roofs, Windows
# TODO New, ForRenovation, Demolished, and ignore blanks
for elem in speckle_data['@Walls']:
# for elem in speckle_data['@Roofs']:
# for elem in speckle_data['@Windows']:
    materials = []
    for material in elem.materialQuantities:
        m={}
        m['name'] = material.material.name
        m['volume'] = material.volume
        materials.append(m)
    elems.append({
        "id": elem.id,
        "area": elem.parameters.HOST_AREA_COMPUTED.value,
        "code": elem.parameters.PricebookCode.value,
        "is_new": elem.parameters.IsNew.value,
        "phase": elem.parameters.Phase.value,
        "materials": materials,
        })
    pass

# For that pricebook number, find price and GWP
for elem in elems:
    if not elem['is_new']:

        post = get_post_by_code(MOLIO_JSON, elem["code"])
        gwp_sqm = 0
        for prop in post[0]['dynamicProperties']:
            if prop['name'][0:16] == "Global warming B":
                gwp_sqm += float(prop['value'])
        cost_sqm = float(post[0]['price'])

        elem['gwp'] = gwp_sqm * elem["area"]
        elem['cost'] = cost_sqm * elem["area"]


### calculate new product results:

with open(NEW_JSON, 'r', encoding='utf-8') as file:
    new_data = json.load(file)


for elem in elems:
    if elem['is_new']:
        elem['gwp'] = 0
        elem['cost'] = 0
        elem['time'] = 0
        for material in elem['materials']:
            try:
                material_data = [el for el in new_data if el['name'] == material['name']][0]
                cost_sqm = material_data['Cost']
                gwp_sqm = material_data['GWP_A1-A3']
                time_sqm = material_data['Time']
                elem['cost'] += cost_sqm * material["volume"]
                elem['gwp'] += gwp_sqm * material["volume"]
                elem['time'] += time_sqm * material["volume"]
            except IndexError:
                print(f"no such material as {material['name']} in the New Product database.")

pprint(elems)

