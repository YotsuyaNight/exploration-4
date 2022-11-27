import json
from rev_index import build_rev_index, read_all_documents

def __index_objects_to_map__(object_list):
    object_dict = {}
    for obj in object_list: object_dict[obj.doc_id] = obj.doc_occurences
    return object_dict

reverse_index = build_rev_index(read_all_documents())
reverse_index = dict((k, __index_objects_to_map__(v)) for k, v in reverse_index.items())

with open("reverse_index_of_cars.txt", "w+", encoding="utf-8") as file:
    file.write(json.dumps(reverse_index, indent=4))