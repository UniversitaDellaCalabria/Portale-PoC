import logging
import os

from django.utils.translation import gettext_lazy as _

from glob import glob
from pathlib import Path

logger = logging.getLogger(__name__)
logging.basicConfig(level=getattr(logging, 'DEBUG'))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

CMS_IMAGE_THUMBSIZE = 51
CMS_IMAGE_CATEGORY_SIZE = 51
CMS_BLOCK_SCHEMAS = (
                       ('{}' ,_('heading')),
                       ('{}' ,_('body')),
                    )

CMS_BLOCK_TEMPLATES_FOLDERS = (f'{BASE_DIR}/cms_templates/blocks',)
CMS_BLOCK_TEMPLATES = [(i[0], i[0].split(os.path.sep)[-1])  for i in 
                       [glob(f"{e}/*.html") for e in CMS_BLOCK_TEMPLATES_FOLDERS]
                       if len(i) >= 1
                      ]

CMS_PAGE_TEMPLATES_FOLDERS = (f'{BASE_DIR}/cms_templates/pages',)
CMS_PAGE_TEMPLATES = [(i[0], i[0].split(os.path.sep)[-1]) for i in 
                       [glob(f"{e}/*.html") for e in CMS_PAGE_TEMPLATES_FOLDERS] 
                      if len(i) >= 1
                      ]
if CMS_BLOCK_TEMPLATES:
    logger.info('Loading block template files:{}'.format('\n  '.join([i[1] for i in CMS_BLOCK_TEMPLATES])))
else:
    logger.warning('Block template files not found')

logger.info('Loading page template files: {}'.format(','.join([i[1] for i in CMS_PAGE_TEMPLATES])))
