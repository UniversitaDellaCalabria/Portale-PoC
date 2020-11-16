from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.decorators import method_decorator

from rest_framework import generics, viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from cms_contexts.decorators import detect_language
from cms_contexts.models import WebPath

from . models import *
from . paginators import Paginator, Page
from . serializers import *
from . utils import publication_context_base_filter


class PublicationDetail(generics.RetrieveAPIView):
    name = 'publication-detail'
    description = 'News'
    queryset = Publication.objects.filter(is_active=True)
    serializer_class = PublicationSerializer
    lookup_field = 'slug'


@method_decorator(detect_language, name='dispatch')
class ApiPublicationsByContext(APIView):
    """
    """
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]
    
    def get(self, request, webpath_id):
        query_params = publication_context_base_filter()
        query_params.update({'webpath__pk': webpath_id})
        pubcontx = PublicationContext.objects.filter(**query_params)
        count = pubcontx.count()
        # serialized = []
        # for i in pubcontx:
            # i.publication.translate_as(lang=request.LANGUAGE_CODE)
            # if i.publication.is_publicable:
                # serialized.append(i.serialize())
        paginator = Paginator(queryset=pubcontx, request=request)
        
        try:
            page_num = int(request.GET.get('page_number', 1))
        except:
            raise ValidationError('Wrong page_number value')
        # breakpoint()
        paged = paginator.get_page(page_num)
        result = paged.serialize()
        return Response(result)


@api_view(['GET'])
def api_contexts(request):
    webpaths = WebPath.objects.filter(is_active=True)
    pubs = ({i.pk: f'{i.site.domain}{i.fullpath}'} for i in webpaths)
    return Response(pubs)
