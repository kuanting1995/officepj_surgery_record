
from settings import Config
from flask_caching import Cache

cache= None

def initial_cache(flask_app):
    global cache
    if(cache == None):
        cache = Cache(
            flask_app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': Config.CACHE_REDIS_URL})
    return cache

