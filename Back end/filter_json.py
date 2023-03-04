import json
import pandas as pd


def append_time_to_post(path, post_numbers, times):
    """Add key for time spent on operation."""
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # test if string og list of string
    if isinstance(post_numbers, str): 
        post_numbers = [post_numbers] # convert single string to list
        try:
            times = [times] # convert single string to list
        except:
            return # something is wrong
    
    # iterate through the posts we want to 
    for post_num, time in zip(post_numbers, times):
        filtered_post_index = [i for i, el in enumerate(data) if el['number'] == post_num]
        #append the time key to relevant 
        if len(filtered_post_index) == 1: # should only be one match
            data[filtered_post_index[0]]['time'] = time
    # write modified data back to json
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(data, file)


def append_post_to_json(path, name, number, description, price, b3, b4, c4 = 0):
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # add new entry
    new_post = {
            "name": name,
            "number": number,
            "description": description,
            "unitId": "dummyID1234",
            "unitName": "m²",
            "price": price,
            "dynamicProperties": [
            {
                "id": None,
                "name": "pricetype",
                "value": "element",
                "description": None
            },
            {
                "id": "TABLE7GUID",
                "name": "Tabel7 GUID",
                "value": "dummyGUID",
                "descrption": "Linking building element to Table 7 data"
            },
            {
                "id": "Name_DK",
                "name": "Material name from Table 7",
                "value": "",
                "descrption": ""
            },
            {
                "id": "GlobalWarmingModuleA1_A3",
                "name": "Global warming A1 - A3",
                "value": "",
                "descrption": ""
            },
            {
                "id": "GlobalWarmingModuleB3",
                "name": "Global warming B3",
                "value": b3,
                "descrption": ""
            },
            {
                "id": "GlobalWarmingModuleB4",
                "name": "Global warming B4",
                "value": b4,
                "descrption": ""
            },
            {
                "id": "GlobalWarmingModuleC3",
                "name": "Global warming C3",
                "value": "0",
                "descrption": ""
            },
            {
                "id": "GlobalWarmingModuleC4",
                "name": "Global warming C4",
                "value": c4,
                "descrption": ""
            },
            {
                "id": "GlobalWarmingModuleD",
                "name": "Global warming D",
                "value": "",
                "descrption": ""
            },
            {
                "id": "DeclaratedFactor_FU",
                "name": "Declareted factor",
                "value": "",
                "descrption": ""
            },
            {
                "id": "DeclaratedUnit_FU",
                "name": "Declarated unit",
                "value": "",
                "descrption": ""
            },
            {
                "id": "MassFactor",
                "name": "Mass factor",
                "value": "",
                "descrption": ""
            }
            ],
            "dimension": None,
            "keywords": [
            "dummy",
            "dummy",
            "dummy"
            ],
            "classifications": [
            {
                "type": "pricebook",
                "code": "2QNIL-7EWD6",
                "text": "Renovering – Bygningsdele"
            },
            {
                "type": "pricebookno",
                "code": number,
                "text": ""
            },
            {
                "type": "CCS-TypeId",
                "code": "",
                "text": ""
            },
            {
                "type": "CCS-kode",
                "code": "",
                "text": ""
            },
            {
                "type": "Huseftersynsordningen",
                "code": "1.1",
                "text": "Tagbelægning/rygning"
            },
            {
                "type": "pricebooksection",
                "code": "1.1",
                "text": "Tagbelægning/rygning"
            },
            {
                "type": "ccsclass",
                "code": "",
                "text": None
            }
            ],
            "posts": [
            {
                "order": 0,
                "amount": 1,
                "post": {
                "name": "Overstrygning af gamle tage med mørtel",
                "number": None,
                "unitId": "dummy01234",
                "unitName": "m²",
                "dimension": "",
                "description": description,
                "dynamicProperties": None,
                "keywords": [],
                "tags": None,
                "classifications": [
                    {
                    "type": "pricebook",
                    "code": "Renovering – Fagdele",
                    "text": ""
                    },
                    {
                    "type": "pricebookno",
                    "code": "(47)12.32,01",
                    "text": ""
                    },
                    {
                    "type": "SFB",
                    "code": "(47)12.",
                    "text": "Tegl"
                    }
                ],
                "resources": [
                    {
                    "usage": 1,
                    "tariffUsage": None,
                    "factor": 0,
                    "resource": {
                        "dimension": None,
                        "name": name,
                        "typeCode": "MATERIAL",
                        "typeName": "Materiale",
                        "keywords": None,
                        "tags": None,
                        "products": None,
                        "dynamicProperties": None,
                        "unitId": None,
                        "unitName": "m²",
                        "classifications": None,
                        "suggestedPrice": 18.018335342407227,
                        "id": None,
                        "version": None,
                        "internalId": None
                    }
                    },
                    {
                    "usage": 1.1056666374206543,
                    "tariffUsage": None,
                    "factor": 0,
                    "resource": {
                        "dimension": None,
                        "name": "Løn murerarbejde",
                        "typeCode": "MANPOWER",
                        "typeName": "Løn",
                        "keywords": None,
                        "tags": None,
                        "products": None,
                        "dynamicProperties": None,
                        "unitId": None,
                        "unitName": "Timer",
                        "classifications": None,
                        "suggestedPrice": 436.76753997802734,
                        "id": None,
                        "version": None,
                        "internalId": None
                    }
                    }
                ],
                "price": price,
                "adjustmentFactors": [
                    {
                    "amount": 200,
                    "factor": 100
                    }
                ],
                "id": "dummy01234",
                "version": None,
                "internalId": None
                },
                "factor": 0
            }
            ],
            "tags": [
            {
                "id": None,
                "name": None
            }
            ],
            "adjustmentFactors": [
            {
                "amount": 100,
                "factor": 0
            }
            ],
            "images": [
            None
            ],
            "id": "dummy1234",
            "version": "3",
            "internalId": "dummy1234",
            "ccstypeid": ""
        }  
    data.append(new_post)
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(data, file)
            
def filter_json_by_classification_text(json_lst, search_strings):
    """Get the json posts that matches the descriptions in the search string. 
    input: list of strings or single string. 
    returns: filtered list of dictionaries"""

    def test_string_containment(el, str_lst):
        """Check if the string matches any part of the search string"""
        match = False
        for str_i in str_lst: 
            if str_i in el:
                match = True
                break
        return match

    # test if string og list of string
    if isinstance(search_strings, str): 
        search_strings = [search_strings] # convert single string to list

    selected_elems = [a_i for a_i in json_lst \
     if test_string_containment(a_i['classifications'][5]['text'], search_strings)] # elements in json list matching the search string.
    
    return selected_elems

def get_post_by_code(json_path, code_str):
    """Get post from json by code string"""
    with open(json_path, 'r', encoding='utf-8') as file:
        data_list = json.load(file)
    filtered_post = [el for el in data_list if el['number'] == code_str]

    #TODO return information if nothing is found
    return filtered_post

def write_json(list, path):
    """Write list of dicts to json"""
    with open(path, "w") as new_data:
        json.dump(list, new_data)

def filter_by_edp_values(json_path):
    """Get only posts from handbook with epd-numbers"""
    def find_non_empty_vals(dict_lst, key):
        match = False
        for d in dict_lst:
            if len(d[key]) > 0:
                match = True
                break
        return match
    # get json as list of dicts
    with open(json_path, 'r', encoding='utf-8') as file:
        json_lst = json.load(file)
    
    #iterate through list of posts
    non_empty_epd = [el for el in json_lst if find_non_empty_vals(el['dynamicProperties'][3:9], 'value')]
    
    # write non-empty epds to 
    write_json(non_empty_epd, 'Data\\els_with_epd_vals.json')



if __name__ == '__main__':
    search_post = '8.2-8.1,01'
    # open the json
    
    """
    with open('Data\\RandomPriceRenBD.json', mode="r", encoding="utf-8") as file:
        json_list = json.load(file) # list of nested dictionaries. One for each roof post

    # Find unique chapters
    chapters = [] # list of the chapter for each post
    for post in json_list: # iterate through all posts in the json list
        post_chapter = post['classifications'][5]['text']
        chapters.append(post['classifications'][5]['text'])
    print(chapters)


    search_string = ['Væg']
    filtered_json = filter_json_by_classification_text(json_list, search_strings = search_string)
    # change name to find string
    if isinstance(search_string, list):
        search_string = ''.join(search_string)

    # find post in json
    post_dict = get_post_by_code('Data\\json_VægVindu.json', search_post)
      
    # write to json with just walls    
    new_path = f'Data\\json_{search_string}.json'
    write_json(filtered_json, new_path)
    
    epd_posts = filter_by_edp_values('Data\\RandomPriceRenBD.json')
   
   
    
    post_list = ['2.5-3.2,02', '2.5-2.1,02', '2.5-1.1,01', '9.1-9.1,01', '9.1-9.1,02', '1.1-3.4,02']
    times = [0.5, 0.5, 0.5, 0.4, 0.45, .8]
    append_time_to_post(f'Data\\els_with_epd_vals_appended.json', post_list, times)
"""
