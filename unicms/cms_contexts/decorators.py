import logging

from django.conf import settings
from . utils import detect_user_language


logger = logging.getLogger(__name__)


def detect_language(func_to_decorate):
    """ store_params_in_session as a funcion decorator
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]
        request.LANGUAGE_CODE = detect_user_language(request)
        return func_to_decorate(*original_args, **original_kwargs)
    return new_func
