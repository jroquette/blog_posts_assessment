"""
Definition of application routes
"""
import multiprocessing
from flask import jsonify, request, abort

from blog_post import app, cache
from blog_post.utils import thread_tags, sort_by_key
from blog_post.validators import validate_sort_by, validate_direction


@app.route('/api/ping', methods=['GET'])
def health_check():
    """
    Health check method, show if system is up

    :return: Dictionary with 200 status code
    """
    return jsonify({"success": True}), 200


@app.route('/api/posts', methods=['GET'])
@cache.cached(timeout=15, query_string=True)
def get_posts():
    """
    Get posts to source "api.hatchways.io"

    :return: json parser
    """
    tags = request.args.get('tags')
    if tags is None:
        abort(400, "Tags parameter is required.")
    tags = tags.split(',')
    sort_by = request.args.get('sortBy', 'id')
    if sort_by:
        validate_sort_by(sort_by)
    direction = request.args.get('direction', 'asc')
    if direction:
        validate_direction(direction)
    response = []
    with multiprocessing.Pool() as pool:
        for subset in pool.imap_unordered(thread_tags, tags):
            response.extend(subset)
    response = sort_by_key(values=response, key=sort_by, direction=direction, delete_duplicated=True)
    return jsonify(response), 200
