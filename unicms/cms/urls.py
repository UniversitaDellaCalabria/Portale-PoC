from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import re_path, path, include

from . import api_views
from . views import *

urlpatterns = []


# Public API Resources
urlpatterns += path(f'api/contexts',
                    api_views.api_contexts,
                    name='api_contexts'),

urlpatterns += path(f'api/news/by-context/<int:webpath_id>',
                    api_views.api_publications_by_context),

# too wide for us!
# urlpatterns += path(f'api/news/list',
                    # api_views.PublicationList.as_view()),

urlpatterns += path(f'api/news/detail/<str:slug>',
                    api_views.PublicationDetail.as_view(),
                    name='publication-detail'),

# uniCMS dispatcher
urlpatterns += re_path('.*', cms_dispatch, name='cms_dispatch'),
