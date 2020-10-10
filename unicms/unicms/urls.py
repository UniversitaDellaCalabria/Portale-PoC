"""unicms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from filebrowser.sites import site

# site.storage.location = "media/"
# site.directory = "uploads/"

ADMIN_PATH = getattr(settings, 'ADMIN_PATH', 'admin')

urlpatterns = [
    path(f'{ADMIN_PATH}/', admin.site.urls),
    # path('mdeditor/', include('mdeditor.urls')),
    
    path('tinymce/', include('tinymce.urls')),
    
    # TODO, better configuration here
    # https://django-filebrowser.readthedocs.io/en/latest/settings.html
    # https://www.tiny.cloud/docs/general-configuration-guide/upload-images/
    # path(f'{ADMIN_PATH}/filebrowser/', 
         # include((site.urls[0], 'filebrowser'), namespace='filebrowser')),
    
    path('', include('cms.urls')),
]


if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

