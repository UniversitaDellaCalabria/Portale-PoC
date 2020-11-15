from rest_framework import generics, viewsets, permissions

from . models import *
from . serializers import *


class PublicationContextList(generics.ListAPIView):
    description = 'News by Contexts'
    queryset = PublicationContext.objects.filter(is_active=True)
    serializer_class = PublicationContextSerializer


class PublicationList(generics.ListAPIView):
    description = 'News list'
    queryset = Publication.objects.filter(is_active=True)
    serializer_class = PublicationSerializer


class PublicationDetail(generics.RetrieveAPIView):
    name = 'publication-detail'
    description = 'News'
    queryset = Publication.objects.filter(is_active=True)
    serializer_class = PublicationSerializer
    lookup_field = 'slug'
