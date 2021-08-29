"""
Definition of validators of requisitions
"""

from flask import abort


def validate_sort_by(sort_by):
    """
    Validate param sortBy
    :param sort_by:
    :return:
    """
    fields_required = ['id', 'reads', 'likes', 'popularity']
    if sort_by not in fields_required:
        abort(400, f"sortBy parameter is invalid")
    return True


def validate_direction(direction):
    """
    Validate param direction

    :param direction:
    :return:
    """
    fields_required = ['asc', 'desc']
    if direction not in fields_required:
        abort(400, f"direction parameter is invalid")
    return True
