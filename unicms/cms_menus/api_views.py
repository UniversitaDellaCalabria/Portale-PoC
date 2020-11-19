from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.decorators import method_decorator

from rest_framework import generics, viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from cms_contexts.decorators import detect_language

from . models import *


@method_decorator(detect_language, name='dispatch')
class ApiMenu(APIView):
    """
    """
    description = 'Get a Menu in JSON format'
    permission_classes = [permissions.IsAdminUser]
    
    def get(self, request, menu_id):
        menu = NavigationBar.objects.filter(is_active=True,
                                            pk=menu_id).first()
        if not menu:
            raise NotFound(detail="Error 404, page not found", code=404)
        lang = getattr(request, 'LANGUAGE_CODE', '')
        res = menu.serialize(lang=lang)
        return Response(res)
    

    def post(self, request, menu_id=None):
        name = request.data['name']
        is_active = request.data['is_active']
        childs = request.data.get('childs')
        menu = NavigationBar.objects.create(name=name, 
                                            is_active=is_active)
        menu.import_items(childs)
        return Response(menu.serialize())
