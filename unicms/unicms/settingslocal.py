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
    'cms_context',
    'cms_medias',
    'cms',

    'unical_templates',

]

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
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
