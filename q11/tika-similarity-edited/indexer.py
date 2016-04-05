import json
import os


def index_from_json(type, file_name, child_node):
    with open(file_name, 'r') as f:
        json_obj = json.load(f)
        obj_dict = {}
        walk_json(type, json_obj, "", child_node, obj_dict)
    with open("fixed_%s" % file_name, 'w') as f:
        json.dump(obj_dict.values(), f)


def walk_json(type, root, parent_name, child_node, obj_dict):
    obj = {key: value for (key, value) in root.items() if key != child_node}
    obj['type'] = type
    if parent_name not in obj_dict:
        obj['parent'] = []
    else:
        obj['parent'] = obj_dict[parent_name]['parent'] + [parent_name]
    obj_dict[obj['name']] = obj
    if child_node in root:
        for child in root[child_node]:
            walk_json(type, child, obj['name'], child_node, obj_dict)


if __name__ == "__main__":
    # index_from_json("geo", "circle_geo.json", "children")
    # index_from_json("ms", "circle_ms.json", "children")
    index_from_json("sweet", "clusters_sweet.json", "children")
