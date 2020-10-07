from django.utils.translation import gettext_lazy as _

from glob import glob
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

CMS_IMAGE_THUMBSIZE = 51
CMS_IMAGE_CATEGORY_SIZE = 51
CMS_BLOCK_SCHEMAS = (
                       ('{}' ,_('heading')),
                       ('{}' ,_('body')),
                    )

CMS_BLOCK_TEMPLATES_FOLDERS = (f'{BASE_DIR}/cms_templates/blocks',)
CMS_BLOCK_TEMPLATES = [i for i in 
                       [glob(f"{CMS_BLOCK_TEMPLATES_FOLDERS}/*.html")] 
                      ]

CMS_PAGE_TEMPLATES_FOLDERS = (f'{BASE_DIR}/cms_templates/pages',)
CMS_PAGE_TEMPLATES = [i for i in 
                       [glob(f"{CMS_PAGE_TEMPLATES_FOLDERS}/*.html")] 
                      ]
