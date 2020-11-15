from rest_framework import generics, viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from cms_contexts.models import WebPath
from . models import *
from . serializers import *


class PublicationDetail(generics.RetrieveAPIView):
    name = 'publication-detail'
    description = 'News'
    queryset = Publication.objects.filter(is_active=True)
    serializer_class = PublicationSerializer
    lookup_field = 'slug'


# @api_view(['GET'])
# def api_publications_by_context(request, webpath_id):

class ApiPublicationByContext(APIView):
    """
    """
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]
    
    def get(self, request, webpath_id):
        pubcontx = PublicationContext.objects.filter(webpath__pk=webpath_id,
                                                     is_active=True)
        count = pubcontx.count()
        
        pubs = [i.publication.serialize() 
                for i in pubcontx 
                if i.publication.is_publicable]
        return Response(pubs)


@api_view(['GET'])
def api_contexts(request):
    webpaths = WebPath.objects.filter(is_active=True)
    pubs = ({i.pk: f'{i.site.domain}{i.fullpath}'} for i in webpaths)
    return Response(pubs)
