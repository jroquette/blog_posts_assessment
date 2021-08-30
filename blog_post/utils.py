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
    """

    :param tag:
    :return:
    """
    ans = get(url="https://api.hatchways.io/assessment/blog/posts", params=dict(tag=tag))
    return ans.get('posts')


def remove_duplicated(values):
    """
    Remove duplicated values in a list of dictionaries

    :param values: list of dictionaries
    :return: list of dictionaries without duplicated values
    """
    return [value for key, value in enumerate(values) if value not in values[key + 1:]]


def sort_by_key(values, key='id', direction='asc', delete_duplicated=True):
    """
    Sort dictionary by a key

    :param values: list of dictionaries with values
    :param key: key
    :param direction:
    :param delete_duplicated: flag to remove values duplicated
    :return:
    """
    if delete_duplicated:
        values = remove_duplicated(values)
    return sorted(values, key=lambda i: i[key], reverse=False if direction == 'asc' else True)
