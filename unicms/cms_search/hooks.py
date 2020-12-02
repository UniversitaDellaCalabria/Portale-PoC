import logging

from django.conf import settings
from django.utils import timezone
from . import settings as app_settings


logger = logging.getLogger(__name__)


MONGO_SEARCH_DOC_SCHEMA = getattr(settings, 'MONGO_SEARCH_DOC_SCHEMA',
                                  app_settings.MONGO_SEARCH_DOC_SCHEMA)


def page_se_index(page_object):
    logger.debug(f'{page_object} succesfully indexed in search engine')


def publication_se_index(pub_object):
    logger.debug(f'{pub_object} succesfully indexed in search engine')

    
