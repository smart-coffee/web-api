from typing import List


def filter_none_values(l: List) -> List:
    return [x for x in l if x is not None]


def filter_empty_strings(l: List) -> List:
    return [x for x in l if x]


def is_dict_structure_equal(template: dict, json_obj):
    list_to_check = []
    if type(json_obj) is list:
        list_to_check.extend(json_obj)
    else:
        list_to_check.append(json_obj)

    for obj in list_to_check:
        if not obj.keys() == template.keys():
            return False

    return True