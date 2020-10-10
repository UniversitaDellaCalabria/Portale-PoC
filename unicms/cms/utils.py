import logging
import os

from django.conf import settings

from . import settings as app_settings

logger = logging.getLogger(__name__)


def load_app_settings():
    for i in dir(app_settings):
        if i[0] == '_': continue
        globals()[i] = getattr(settings, i, 
                               getattr(app_settings, i))


def remove_file(fpath):
    try:
        os.remove(fpath)
    except Exception as e:
        logger.error('{} cannot be removed: {}'.format(fpath, e))
