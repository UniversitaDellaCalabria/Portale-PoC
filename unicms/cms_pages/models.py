import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

from django.utils.translation import gettext_lazy as _

from cms_context.models import WebPath
from cms_templates.models import (CMS_TEMPLATE_BLOCK_SECTIONS,
                                  AbstractPageBlock,
                                  ActivableModel,
                                  PageTemplate,
                                  SortableModel,
                                  TimeStampedModel)
from taggit.managers import TaggableManager

from . settings import *

logger = logging.getLogger(__name__)
