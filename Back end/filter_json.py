import json
import pandas as pd

#json_walls = map(lambda dict: dict['classification'][5]['text'].contains(search_string), json_list)
#selected_elems = [a_i for a_i in json_list \
#     if search_string in a_i['classifications'][5]['text']] # elements in json list matching the search string.


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
    if isinstance(search_string, str): 
        search_strings = [search_strings] # convert single string to list

    selected_elems = [a_i for a_i in json_list \
     if test_string_containment(a_i['classifications'][5]['text'], search_strings)] # elements in json list matching the search string.
    
    return selected_elems


# try with new methods
df = pd.read_json('Data\\RandomPriceRenBD.json')

with open('Data\\RandomPriceRenBD.json', mode="r", encoding="utf-8") as file:
    json_list = json.load(file) # list of nested dictionaries. One for each roof post

# Find unique chapters
chapters = [] # list of the chapter for each post
for post in json_list: # iterate through all posts in the json list
    post_chapter = post['classifications'][5]['text']
    chapters.append(post['classifications'][5]['text'])
print(chapters)



search_string = ['Væg', 'Vindu']
filtered_json = filter_json_by_classification_text(json_list, search_strings = search_string)


# write to json with just walls
if isinstance(search_string, list):
    search_string = ''.join(search_string)
new_path = f'Data\\json_{search_string}.json'
with open(new_path, "w") as new_data:
   json.dump(filtered_json, new_data)