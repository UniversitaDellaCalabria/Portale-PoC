import logging
import cms_search.settings as app_settings

from django.conf import settings
from django.utils import timezone

from . import mongo_collection
from . models import page_to_entry, publication_to_entry

logger = logging.getLogger(__name__)


MONGO_SEARCH_DOC_SCHEMA = getattr(settings, 'MONGO_SEARCH_DOC_SCHEMA',
                                  app_settings.MONGO_SEARCH_DOC_SCHEMA)
MONGO_DB_NAME = getattr(settings, 'MONGO_DB_NAME')
MONGO_COLLECTION_NAME = getattr(settings, 'MONGO_COLLECTION_NAME')


def page_se_index(page_object):
    data = MONGO_SEARCH_DOC_SCHEMA.copy()
    collection = mongo_collection()
    search_entry = page_to_entry(page_object).__dict__
    # check if it doesn't exists or remove it and recreate
    doc_query = {"content_type": page_object._meta.label, 
                 "content_id": search_entry['content_id']}
    doc = collection.find_one(doc_query)
    if doc:
        collection.delete_many(doc_query)
        logger.info(f'{page_object} removed from search engine')
        
    if page_object.is_publicable:
        doc = collection.insert_one(search_entry)
    
    logger.info(f'{page_object} succesfully indexed in search engine')


def publication_se_index(pub_object):
    data = MONGO_SEARCH_DOC_SCHEMA.copy()
    collection = mongo_collection()   
    search_entry = publication_to_entry(pub_object).__dict__
    # check if it doesn't exists or remove it and recreate
    doc_query = {"content_type": pub_object._meta.label, 
                 "content_id": search_entry['content_id']}
    doc = collection.find_one(doc_query)
    if doc:
        collection.delete_many(doc_query)
        logger.info(f'{pub_object} removed from search engine')
        
    if pub_object.is_publicable:
        doc = collection.insert_one(search_entry)
    
    logger.info(f'{pub_object} succesfully indexed in search engine')

    
