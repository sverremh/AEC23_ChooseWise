from specklepy.api import operations
from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account
from specklepy.transports.server import ServerTransport
from specklepy.objects import Base

from pprint import pprint
from filter_json import filter_json_by_classification_text, get_post_by_code
import csv
import pandas as pd
import json


# Input databases
MOLIO_JSON = r"./Data/els_with_epd_vals_appended.json" #Path to condensed Molio DB

NEW_JSON = r"./Data/New_products.json" # Path to DB of new products

# Read the input data files
with open(NEW_JSON, 'r', encoding='utf-8') as new_db_file:
    new_data = json.load(new_db_file)
#file = open(NEW_JSON, 'r', encoding='utf-8')

with open(MOLIO_JSON, 'r', encoding='utf-8') as old_db_file: 
    process_data = json.load(old_db_file)
#file = open(MOLIO_JSON, 'r', encoding='utf-8')


# Authenticate Speckle
client = SpeckleClient(host="https://speckle.xyz/")
account = get_default_account()
client.authenticate_with_account(account)


def fetch_speckle(STREAM_ID, COMMIT_ID):
    """
    Fetches a speckle stream and returns the date

    Parameters
    ----------
    STREAM_ID : string
        STREAM_ID for the speckle string.
    COMMIT_ID : string
        ID of the specific commit to fetch

    Returns
    -------
    List
        all data from the speckle commit
    """
    # get the specified commit data
    commit = client.commit.get(STREAM_ID, COMMIT_ID)
    # create an authenticated server transport from the client and receive the commit obj
    transport = ServerTransport(client=client, stream_id=STREAM_ID)
    speckle_data = operations.receive(commit.referencedObject, transport)
    return speckle_data


def calculate_renovation(elem):
    """
    Calculates LCA, Cost, and time of a speckle element 
    and appends information to the speckle element. 

    Parameters
    ----------
    elem : Speckle Element
        The element to calculate the renovation cost of.

    Returns
    -------
    Speckle element
        The speckle element with relevant information added.
    """
    # For that pricebook number, find price and GWP
    if elem.parameters['Phase'].value == "ForRenovation" or elem.parameters['Phase'].value == "Demolished":
        post = [el for el in process_data if el['number'] == elem.parameters.PricebookCode.value]
        gwp_sqm = 0
        for prop in post[0]['dynamicProperties']:
            if prop['name'][0:16] == "Global warming B":
                gwp_sqm += float(prop['value'])
        cost_sqm = float(post[0]['price'])
        time_sqm = float(post[0]['time'])
        
        elem.parameters['GWP'] = gwp_sqm * elem.parameters.HOST_AREA_COMPUTED.value
        elem.parameters['Cost'] = cost_sqm * elem.parameters.HOST_AREA_COMPUTED.value
        elem.parameters['Time'] = time_sqm * elem.parameters.HOST_AREA_COMPUTED.value
    return elem
    

def calculate_new_construction(elem):
    """
    Calculates LCA, Cost, and time of a new speckle element 
    and appends information to the speckle element. 

    Parameters
    ----------
    elem : Speckle Element
        The element to calculate the renovation cost of.

    Returns
    -------
    Speckle element
        The speckle element with relevant information added.
    """
    # Takes volumes of materials and multiplies by data from EPD/pricebook
    if elem.parameters['Phase'].value == "New":
        elem.parameters['GWP'] = 0
        elem.parameters['Cost'] = 0
        elem.parameters['Time'] = 0
        for material in elem.materialQuantities:
            try:
                material_data = [el for el in new_data if el['name'] == material.material.name][0]
                cost_sqm = material_data['Cost']
                gwp_sqm = material_data['GWP_A1-A3']
                time_sqm = material_data['Time']
                elem.parameters['Cost'] += cost_sqm * material.volume
                elem.parameters['GWP'] += gwp_sqm * material.volume
                elem.parameters['Time'] += time_sqm * material.volume
            except IndexError:
                print(f"no such material as {material['name']} in the New Product database.")
    return elem


def send_back_to_speckle(data):
    """
    Commits the data back to the speckle stream. 

    Parameters
    ----------
    data : Speckle Data
        All speckle data to send back.

    Returns
    -------
        prints information about the results
    """
    # Create a new Base object and send it to the stream.
    base = Base(name="Test123", values=data)
    # Create a new transport for sending objects to the stream.
    transport = ServerTransport(client=client, stream_id=STREAM_ID)
    # Send the new Base object to the stream.
    hash = operations.send(base=base, transports=[transport])
    # Create a new commit on the stream with the new object.
    commit_id = client.commit.create(
        stream_id=STREAM_ID,
        branch_name=BRANCH_NAME,
        object_id=hash,
        message="Uploaded model with calculations from Python"
    )
    print(f"Sent {data.totalChildrenCount} elements to stream {STREAM_ID} with commit {commit_id}")


if __name__ == '__main__':
    # Mocked IDs, ideally this could be replaced by webhook triggering event
    STREAM_ID="9e730f9975"
    BRANCH_NAME = "svhs/branch_1"
    COMMIT_ID = "4e154c8a6b" 
    # OBJ_ID = "6bf18ee3a41ce18d8936e92f26130d4e"

    speckle_data = fetch_speckle(STREAM_ID, COMMIT_ID)

    # TODO speckle_data['@Windows']:
    # TODO handle IFC data structure from Speckle as well
    for elem in speckle_data['@Walls']:
        elem = calculate_renovation(elem)
        elem = calculate_new_construction(elem)
        pprint(elem.parameters.__dict__)
    for elem in speckle_data['@Roofs']:
        elem = calculate_renovation(elem)
        elem = calculate_new_construction(elem)
        pprint(elem.parameters.__dict__)

    send_back_to_speckle(speckle_data)
