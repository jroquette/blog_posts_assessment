"""
Create blog post Flask application
"""
import os
from flask import Flask
from flask_caching import Cache
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

config = {
    "CACHE_TYPE": os.getenv('CACHE_TYPE'),
    "CACHE_REDIS_HOST": os.getenv('CACHE_REDIS_HOST'),
    "CACHE_REDIS_PORT": os.getenv('CACHE_REDIS_PORT'),
    "CACHE_REDIS_DB": os.getenv('CACHE_REDIS_DB'),
    "CACHE_REDIS_URL": os.getenv('CACHE_REDIS_URL'),
    "CACHE_DEFAULT_TIMEOUT": os.getenv('CACHE_DEFAULT_TIMEOUT'),
}

app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)

from blog_post import routes
