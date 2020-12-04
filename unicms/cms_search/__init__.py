import pymongo

from django.conf import settings
from django.utils import timezone


mongo_client = pymongo.MongoClient(settings.MONGO_URL, **settings.MONGO_DB_PARAMS)
