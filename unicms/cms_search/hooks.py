import logging
import cms_search.settings as app_settings

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from . import mongo_client

logger = logging.getLogger(__name__)


MONGO_SEARCH_DOC_SCHEMA = getattr(settings, 'MONGO_SEARCH_DOC_SCHEMA',
                                  app_settings.MONGO_SEARCH_DOC_SCHEMA)


def page_se_index(page_object):
    data = MONGO_SEARCH_DOC_SCHEMA.copy()
    collection = mongo_client.unicms.search
    app_label, model = page_object._meta.label_lower.split('.')
    contentype = ContentType.objects.get(app_label=app_label, model=model)
    site = page_object.webpath.site.domain
    webpath = page_object.webpath.get_full_path()
    data = {
        "title": page_object.name,
        "heading": page_object.description,
        "content-type": page_object._meta.label,
        "content-type-id": contentype.pk,
        "content": "",
        "site": site,
        "webpath": webpath,
        "urls": [f'{site}{webpath}',],
        "tags": [i for i in page_object.tags.values_list('name', flat=1)],
        "indexed": timezone.localtime(),
        "published": page_object.date_start,
        "viewed": 0,
        "language": "italian",
        "year": page_object.date_start.year
    }
    # check if it doesn't exists or remove it and recreate
    doc_query = {"content-type": page_object._meta.label, 
                 "content-type-id": contentype.pk}
    doc = collection.find_one(doc_query)
    if doc:
        collection.delete_many(doc_query)
        logger.info(f'{page_object} removed from search engine')
        
    if page_object.is_publicable:
        doc = collection.insert_one(data)
    
    logger.info(f'{page_object} succesfully indexed in search engine')


def publication_se_index(pub_object):
    logger.debug(f'{pub_object} succesfully indexed in search engine')

    
