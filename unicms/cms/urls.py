from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . views import *

urlpatterns = [
    path('', cms_content, name='cms_content'),
    ]
