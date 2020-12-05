import pymongo

from django.conf import settings
from django.utils import timezone


class MongoClientFactory(object):
    mongo_client = None
    
    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.mongo_client, cls) or \
           not cls.mongo_client.server_info():
            cls.mongo_client = pymongo.MongoClient(settings.MONGO_URL, 
                                                   **settings.MONGO_DB_PARAMS)
        return cls.mongo_client
    
