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
STREAM_ID = "9e730f9975"    #  Revit
COMMIT_ID = "253cb3de39"

# get the specified commit data
commit = client.commit.get(STREAM_ID, COMMIT_ID)
# create an authenticated server transport from the client and receive the commit obj
transport = ServerTransport(client=client, stream_id=STREAM_ID)
speckle_data = operations.receive(commit.referencedObject, transport)


###definitions for volume

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
        "materials": materials,
        })


# For that pricebook number, find price and GWP
for elem in elems:
    post = get_post_by_code(r"./Data/RandomPriceRenBD.json", elem["code"])
    gwp_sqm = 0
    for prop in post[0]['dynamicProperties']:
        if prop['name'][0:16] == "Global warming B":
            gwp_sqm += float(prop['value'])
    price_sqm = float(post[0]['price'])

    elem['renovation_gwp'] = gwp_sqm * elem["area"]
    elem['renovation_price'] = price_sqm * elem["area"]


### calculate new product results:
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

for elem in elems:
    elem['new_gwp'] = 0
    elem['new_price'] = 0
    
    for material in elem['materials']:
        #TODO MARCINS CODE
        
        cost = calculate_cost(elem,data_s)
        lca = calculate_lca(elem,data_s)
        time = calculate_time(elem,data_s)

        print('cost=' + str(cost) + ' ; ' + 'lca=' + str(lca) + ' ; ' + 'time=' + str(time) )

        elem['new_gwp'] += gwp_sqm * material["volume"]
        elem['new_price'] = price_sqm * material["volume"]



