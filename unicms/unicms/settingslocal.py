import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0jg!+quiguen7)-!%rl32(ya+uf6w8lr58)g4-k^s%5+-86b+l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
AUTH_USER_MODEL = 'accounts.User'

# Application definition

INSTALLED_APPS = [
    'accounts',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',

    'sass_processor',
    'bootstrap_italia_template',
    'django_unical_bootstrap_italia',

    'taggit',
    'tinymce',
    'nested_admin',

    'cms_templates',
    'cms_carousels',
    'cms_contexts',
    'cms_menus',
    'cms_medias',
    'cms',
    'cms_previews',

    'unical_templates',

    'rest_framework',

]

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DATA_UPLOAD_MAX_NUMBER_FIELDS = 100 * 100

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'it-it'
LANGUAGE = LANGUAGE_CODE.split('-')[0]
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [('ar', 'Arabic'),
             ('en', 'English'),
             ('es', 'Spanish'),
             ('fr', 'French'),
             ('it', 'Italian'),
             ('pt', 'Portuguese')]

# Static files (CSS, JavaScript, Images)
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# STATICFILES_DIRS = [
    # os.path.join(BASE_DIR, 'static'),
# ]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


ADMINS = [
    ('Giuseppe De Marco', 'giuseppe.demarco@unical.it'),
    ('Francesco Filicetti', 'francesco.filicetti@unical.it'),
]
MANAGERS = ADMINS

# Default to dummy email backend. Configure dev/production/local backend
# as per https://docs.djangoproject.com/en/stable/topics/email/#email-backends
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
EMAIL_SUBJECT_PREFIX = '[Portale Unical] '

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# TinyMCE CONFIGURATION
# https://django-tinymce.readthedocs.io/en/latest/installation.html#configuration

TINYMCE_DEFAULT_CONFIG = {
    # 'plugins': "table,spellchecker,paste,searchreplace",
    # 'theme': "advanced",
    # 'cleanup_on_startup': True,
    # 'custom_undo_redo_levels': 10,
    "theme": "silver",
    "height": 500,
    "menubar": True,
    "plugins": "advlist,autolink,lists,link,image,charmap,"
               "print,preview,anchor,"
               "searchreplace,visualblocks,code,fullscreen,"
               "insertdatetime,media,table,paste,hr,"
               "code,help,wordcount",
    "toolbar": "undo redo | formatselect | "
               "bold italic backcolor | alignleft aligncenter "
               "alignright alignjustify | bullist numlist outdent indent | "
               "removeformat | help",

    # added
    "a11y_advanced_options": True,
    "media_alt_source": False,

    # image upload
    # https://www.tiny.cloud/docs/general-configuration-guide/upload-images/
}
# TINYMCE_SPELLCHECKER = True
# TINYMCE_COMPRESSOR = True

# TINYMCE_EXTRA_MEDIA = {
    # 'css': {
        # 'all': [
            # ...
        # ],
    # },
    # 'js': [
        # ...
    # ],
# }

CMS_PATH_PREFIX = 'portale/'

CMS_PUBLICATION_VIEW_PREFIX_PATH = 'contents/news/view/'
CMS_PUBLICATION_LIST_PREFIX_PATH = 'contents/news/list'
CMS_PUBLICATION_URL_LIST_REGEXP = f'^(?P<context>[\/a-zA-Z0-9\.\-\_]*)({CMS_PUBLICATION_LIST_PREFIX_PATH})/?$'
CMS_PUBLICATION_URL_VIEW_REGEXP = f'^(?P<context>[\/a-zA-Z0-9\.\-\_]*)({CMS_PUBLICATION_VIEW_PREFIX_PATH})(?P<slug>[a-z0-9\-]*)'

CMS_HANDLERS_PATHS = [CMS_PUBLICATION_VIEW_PREFIX_PATH,
                      CMS_PUBLICATION_LIST_PREFIX_PATH]
CMS_APP_REGEXP_URLPATHS = {
    'cms.handlers.PublicationViewHandler' : CMS_PUBLICATION_URL_VIEW_REGEXP,
    'cms.handlers.PublicationListHandler' : CMS_PUBLICATION_URL_LIST_REGEXP,
}

OAS3_CONFIG = {'title': "Portale dell'Università della Calabria",
               # 'permission_classes': (permissions.AllowAny,),
               'description': "Portale dell'Università della Calabria",
               'termsOfService': 'https://tos.unical.it',
               'x-api-id': '00000000-0000-0000-0000-000000000024',
               'x-summary': "Portale dell'Università della Calabria",
               'license': dict(name='apache2',
                               url='http://www.apache.org/licenses/LICENSE-2.0.html'),
               'servers': [dict(description='description',
                                url='https://www.unical.it'),
                           dict(description='description',
                                url='https://www.unical.it')],
               'tags': [dict(description='description',
                             name='api'),
                        dict(description='description',
                             name='public')],
               'contact': dict(email = 'giuseppe.demarco@unical.it',
                               name = 'Giuseppe De Marco',
                               url = 'https://github.com/UniversitaDellaCalabria'),
               'version': "0.1.2"
}
