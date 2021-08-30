"""
Utils to application
"""

import json
import re

import requests


def get(url, params, raise_error=True):
    """
    Get url

    :param url: url to get
    :param params: to get
    :param raise_error: Raise error no HTTP error (e.g. 500 error)
    :return: parsed json (dictionary)
    """
    if params is None:
        params = {}
    ans = requests.get(url, params=params)
    if raise_error:
        ans.raise_for_status()
    try:
        return ans.json()
    except Exception:
        replaced_text = ans.text.replace("\r", "").replace("\n", "")
        replaced_text = re.sub(r"(\\)(\w)", r"\\\\\2", replaced_text)
    try:
        output_dict = json.loads(replaced_text)
    except Exception:
        output_dict = eval(replaced_text)
    return output_dict


def thread_tags(tag):
    ans = get(url="https://api.hatchways.io/assessment/blog/posts", params=dict(tag=tag))
    return ans.get('posts')


def remove_duplicated(values):
    return [value for key, value in enumerate(values) if value not in values[key + 1:]]


def sort_by_element(values, element='id', direction='asc', not_duplicated=True):
    if not_duplicated:
        values = remove_duplicated(values)
    return sorted(values, key=lambda i: i[element], reverse=False if direction == 'asc' else False)
