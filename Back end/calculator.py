from specklepy.api import operations
from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account
from specklepy.transports.server import ServerTransport
from pprint import pprint


# create and authenticate a client
client = SpeckleClient(host="https://speckle.xyz/")
account = get_default_account()
client.authenticate_with_account(account)

# Get a commit by its ID
STREAM_ID = "579715d27f"    
COMMIT_ID = "cb57d1ddb8"

# get the specified commit data
commit = client.commit.get(STREAM_ID, COMMIT_ID)
# create an authenticated server transport from the client and receive the commit obj
transport = ServerTransport(client=client, stream_id=STREAM_ID)
speckle_data = operations.receive(commit.referencedObject, transport)


def calculate_cost(element):
    return cost

def calculate_lca(element):
    return cost

def calculate_time(element):
    return cost

def send_to_speckle(element):
    pass


roofs = []
for roof in speckle_data['@Roofs']:
    roof_dict = {}
    roof_dict['id'] = roof.id
    roof_dict['materials'] = []
    for material in roof.materialQuantities:
        m={}
        m['name'] = roof.materialQuantities[0].material.name
        m['volume'] = roof.materialQuantities[0].volume
        roof_dict['materials'].append(m)
    roofs.append(roof_dict)

pprint(roofs)

# [{'id': 'f4ffdd94e2b1c226f082a9b90ceb5a44', 'materials': [{'name': 'Default Roof', 'volume': 11.03377918962492}]}]
for element in roofs:
    cost = calculate_cost(element)
    lca = calculate_lca(element)
    time = calculate_time(element)
    send_to_speckle(element)
