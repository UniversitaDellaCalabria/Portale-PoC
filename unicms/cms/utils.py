from django.conf import settings

from . import settings as app_settings


def load_app_settings():
    for i in dir(app_settings):
        if i[0] == '_': continue
        globals()[i] = getattr(settings, i, 
                               getattr(app_settings, i))
