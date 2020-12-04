import logging
import json
import re
import time # debug wait

from bson.json_util import dumps
from django.core.exceptions import ValidationError
from django.utils import timezone, dateparse
from django.utils.decorators import method_decorator

from rest_framework import generics, viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from cms.models import Page, Publication
from cms.paginators import Paginator, Page
from cms_contexts.decorators import detect_language
from cms_contexts.models import WebPath

from . import mongo_client


logger = logging.getLogger(__name__)


def _handle_date_string(date_string):
    date = dateparse.parse_date(date_string)
    dt = timezone.datetime(date.year, date.month, date.day)
    return timezone.make_aware(dt)
    

@method_decorator(detect_language, name='dispatch')
class ApiSearchEngine(APIView):
    """
    """
    description = 'Search Engine'
    
    def get(self, request):
        # get database from client/connection
        mdb = mongo_client.unicms
        # get collection
        collection = mdb.search
        
        # get only what's really needed
        search_regexp = re.match('^[\w\+\-\s\(\)\[\]\=\"\']*', 
                                 request.GET.get('search', ''), 
                                 re.UNICODE)
        query = {}
        if search_regexp:
            search = search_regexp.group()
            if search:
                query = {"$text": {"$search": search}}            
        
        year = request.GET.get('year')
        if year.isdigit():
            year = int(year)
            query['year'] = year
        
        date_start = request.GET.get('date_start')
        date_end = request.GET.get('date_end')
        if date_start or date_end:
            query['published'] = {}
        if date_start:
            query['published']["$gte"] = _handle_date_string(date_start)
        if date_end:
            query['published']["$lt"] = _handle_date_string(date_end)

        
        logger.debug('Search query: {}'.format(query))
        if search:
            res = collection.find(query, {'relevance': {'$meta': "textScore"}}).\
                             sort([('relevance', {'$meta': 'textScore'})])
        else:
            res = collection.find(query)
        
        return Response(json.loads(dumps(res)))
    
