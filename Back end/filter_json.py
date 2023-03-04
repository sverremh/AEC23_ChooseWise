import json
import pandas as pd

df = pd.read_json('Data\\RandomPriceRenBD.json')


with open('Data\\RandomPriceRenBD.json', mode="r", encoding="utf-8") as file:
    json_list = json.load(file) # list of nested dictionaries. One for each roof post


chapters = [] # list of the chapter for each post
for post in json_list: # iterate through all posts in the json list
    post_chapter = post['classifications'][5]['text']
    chapters.append(post['classifications'][5]['text'])
print(chapters)


search_string = 'Væg'
#json_walls = map(lambda dict: dict['classification'][5]['text'].contains(search_string), json_list)
selected_elems = [a_i for a_i in json_list \
     if search_string in a_i['classifications'][5]['text']] # elements in json list matching the search string.

# write to json with just walls
new_path = f'Data\\json_{search_string}.json'
with open(new_path, "w") as new_data:
   json.dump(selected_elems, new_data)


def filter_json_by_classification_text(search_strings, json_lst):
    """Get the json posts that matches the descriptions in the search string. 
    input: list of strings or single string. 
    returns: filtered list of dictionaries"""

    def test_string_containment(el, str_lst):
        """Check if the string matches any part of the search string"""
        match = False
        for str_i in str_lst: 
            if str_lst in el:
                match = True
                break
        return match
    
    if isinstance(search_string, str):
        search_strings = [search_strings] # convert single string to list
