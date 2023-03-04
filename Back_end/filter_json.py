import json
import pandas as pd

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

    selected_elems = [a_i for a_i in json_list \
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
    """
    epd_posts = filter_by_edp_values('Data\\RandomPriceRenBD.json')

    
