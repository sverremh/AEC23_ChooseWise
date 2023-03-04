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


speckle_data['@Roofs'][0].materialQuantities[0].volume

speckle_data['@Roofs'][0].materialQuantities[0].material.name

# if hasattr(speckle_data, "@Roof"):
#     for element in speckle_data[category_name]:
#         if hasattr(element, 'materialQuantities'):
#             if element.materialQuantities: # not true for curtain walls as they don't have materials
#                 for material in element.materialQuantities:
#                     volume = convert2si(material.volume, material.units, order=3)
#                     category = material.material.name # possible also .materialCategory
#                     if category in materials:
#                         materials[category] += volume
#                     else:
#                         materials[category] = volume
#     materials = {key : round(materials[key], ROUNDING) for key in materials}

pprint(speckle_data['roofs'])


def calculate_cost(element):
    # if hasattr(element, '@Roofs'):
    #     for roof in speckle_data['@Roofs']:
    #         # N.b.: this is actual surface area, not flat area
    #         area = convert2si(roof.parameters.HOST_AREA_COMPUTED.value, roof.parameters.HOST_AREA_COMPUTED.applicationUnit, order=2)

    #         # measure circumference
    #         circumference = 0
    #         for line in roof.outline.segments:
    #             circumference += convert2si(line.length, line.units)
    #         if circumference > area**(0.5):
    #             circumferences.append(round(circumference, ROUNDING))
    #         else:
    #             circumferences.append(round(area**(0.5), ROUNDING))

    #         # measure height
    #         try:
    #             top = convert2si(roof.parameters.ACTUAL_MAX_RIDGE_HEIGHT_PARAM.value, roof.units)
    #             bottom = convert2si(roof.parameters.ROOF_LEVEL_OFFSET_PARAM.value, roof.units)
    #             lvl_elev = convert2si(roof.level.elevation, roof.level.units)
    #             height = top - bottom - lvl_elev
    #         except AttributeError:
    #             vertex_heights=[]
    #             for mesh in roof.displayValue:
    #                 vertex_heights = vertex_heights + mesh.vertices[3 - 1::3]
    #             single_height = max(vertex_heights) - min(vertex_heights)
    #             height = convert2si(single_height, roof.units)
    #         heights.append(round(height, ROUNDING))

    #         # assess roof type. Alternatively: roof.parameters.ROOF_SLOPE.value
    #         if height < 0.5:
    #             types.append("flat")
    #         else:
    #             types.append("gable")

    # return areas, circumferences, heights, types




    return cost

def calculate_lca(element):
    return cost

def calculate_time(element):
    return cost

def send_to_speckle(element, cost, lca, time):
    pass

for element in input_data:
    cost = calculate_cost(element)
    lca = calculate_lca(element)
    time = calculate_time(element)
    send_to_speckle(element, cost, lca, time)
