from specklepy.api import operations
from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account
from specklepy.transports.server import ServerTransport
from pprint import pprint
from filter_json import filter_json_by_classification_text, get_post_by_code
import csv
import numpy


# create and authenticate a client
client = SpeckleClient(host="https://speckle.xyz/")
account = get_default_account()
client.authenticate_with_account(account)

# Get a commit by its ID
STREAM_ID = "9e730f9975"    #  Revit
COMMIT_ID = "7bc90188b9"
# STREAM_ID = "9e730f9975"  # IFC
# COMMIT_ID = "5316a76472"

# get the specified commit data
commit = client.commit.get(STREAM_ID, COMMIT_ID)
# create an authenticated server transport from the client and receive the commit obj
transport = ServerTransport(client=client, stream_id=STREAM_ID)
speckle_data = operations.receive(commit.referencedObject, transport)


def calculate_cost(element,data):
    cost =0
    volume = 0
    for em in element['materials']:
        e_name = em['name']
        for d in data:
            data_name = d['name']
            #print(data_name)
            #print(e_name)
            #find the same names of material
            if (e_name == data_name):
                volume = em['volume']
                #calculate the cost
                data_cost = d['cost']
                print('dataCost=' + str(data_cost) + ' , ' + ' volume=' + str(volume) )
                cost = float(volume) * float(data_cost)
                print('cost of the element= ' + str(cost))
    
    
    return cost

def calculate_lca(element,data):
    lca =0
    volume = 0
    for em in element['materials']:
        e_name = em['name']
        for d in data:
            data_name = d['name']
            #print(data_name)
            #print(e_name)
            #find the same names of material
            if (e_name == data_name):
                volume = em['volume']
                #calculate the cost
                data_LCA = d['LCA']
                print('dataLCA=' + str(data_LCA) + ' , ' + ' volume=' + str(volume) )
                lca = float(volume) * float(data_LCA)
                print('lca of the element= ' + str(lca))
    
    return lca

def calculate_time(element,data):
    time =0
    volume = 0
    for em in element['materials']:
        e_name = em['name']
        for d in data:
            data_name = d['name']
            #print(data_name)
            #print(e_name)
            #find the same names of material
            if (e_name == data_name):
                volume = em['volume']
                #calculate the cost
                data_time = d['time']
                print('dataTime=' + str(data_time) + ' , ' + ' volume=' + str(volume) )
                time = float(volume) * float(data_time)
                print('time of the element= ' + str(time))
    
    return time

def send_to_speckle(element):
    pass


walls = []
for roof in speckle_data['@Walls']:
    roof_dict = {}
    roof_dict['id'] = roof.id
    roof_dict['materials'] = []
    for material in roof.materialQuantities:
        m={}
        m['name'] = roof.materialQuantities[0].material.name
        m['volume'] = roof.materialQuantities[0].volume
        roof_dict['materials'].append(m)
    walls.append(roof_dict)

pass

#pprint(roofs)

# [{'id': 'f4ffdd94e2b1c226f082a9b90ceb5a44', 'materials': [{'name': 'Default Roof', 'volume': 11.03377918962492}]}]

data_s= []


with open('Data\\NewProducts.csv', newline='') as csvfile:
    dataRead = csv.reader(csvfile, delimiter=',')
    
    for row in dataRead:
        data = {}
        data['name'] = row[0]
        data['cost'] = row[1]
        data['LCA'] = row[2]
        data['time'] = row[3]
        data_s.append(data) 

print(data_s)

for element in roofs:
    cost = calculate_cost(element,data_s)
    lca = calculate_lca(element,data_s)
    time = calculate_time(element,data_s)
    #print('cost=' + cost + ' ; ' + 'lca=' + lca + ' ; ' + 'time=' + time)

send_to_speckle(element)


# Open JSON and find a code:
JSON_PATH = r"./Data/json_VægVindu.json"
CODE_NUMBER = "3.2-1.1,01"
SEARCH_STRING = "Væg"
# filter_json_by_classification_text(JSON_PATH, SEARCH_STRING)
post = get_post_by_code(JSON_PATH, CODE_NUMBER)


for elem in post:
    print(elem['price'])
    for prop in elem.dynamicproperties:
        if prop['name'][0:3] == "Gl":
            print(prop['name'])



pass