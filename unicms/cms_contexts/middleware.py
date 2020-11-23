import logging
import json

from django.conf import settings
from . utils import detect_user_language

logger = logging.getLogger(__name__)


def detect_language_middleware(get_response):
    """
    get_response is a callable ...
    """
    def language_middleware(request):
        detect_user_language(request)
        response = get_response(request)
        return response

    return language_middleware


def show_template_blocks_sections(get_response):
    def blocks_sections_visibility(request):
        if request.user.is_staff:
            arg = 'show_template_blocks_sections'
            state = request.GET.get(arg)
            if state in ('1', 'true', 'True'):
                state = True
            elif state in ('0', 'false', 'False'):
                state = False
            elif arg in request.GET:
                state = True
                state_session = request.session.get(arg, False)
                if state_session == None: 
                    state_session = False
                state ^= state_session
            
            request.session[arg] = state
            response = get_response(request)
            return response
    
    return blocks_sections_visibility
