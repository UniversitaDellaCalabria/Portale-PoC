import logging
import json

from django.conf import settings
from . utils import detect_user_language

logger = logging.getLogger(__name__)


def detect_language_middleware(get_response):
    """
    get_response is a callable ...
    """
    def middleware(request):
        detect_user_language(request)
        response = get_response(request)
        return response

    return middleware
