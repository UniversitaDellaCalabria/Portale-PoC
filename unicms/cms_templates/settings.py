import logging
import os

from django.utils.translation import gettext_lazy as _

from glob import glob
from pathlib import Path

logger = logging.getLogger(__name__)
# logging.basicConfig(level=getattr(logging, 'DEBUG'))


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


CMS_TEMPLATE_BLOCK_SECTIONS = (('pre-head', _('Pre-Header')),
                               ('head', _('Header')),
                               ('menu', _('Navigation Menu')),
                               ('menu-2', _('Navigation Menu 2')),
                               ('menu-3', _('Navigation Menu 3')),
                               ('slider', _('Carousel/Slider')),
                               ('slider-2', _('Carousel/Slider 2')),
                               ('1','1'),
                               ('2','2'),
                               ('3','3'),
                               ('4','4'),
                               ('5','5'),
                               ('6','6'),
                               ('7','7'),
                               ('8','8'),
                               ('9','9'),
                               ('pre-footer', _('Pre-Footer')),
                               ('footer', _('Footer')),
                               ('post-footer', _('Post-Footer'))
                              )

CMS_BLOCK_TYPES = (
                       ('unicms.cms_templates.HTMLBlock', 'HTML Block'),
                       ('unicms.cms_templates.JSONBlock', 'JSON Block'),
                    )

CMS_BLOCK_TEMPLATES_FOLDERS = (f'{BASE_DIR}/templates/blocks',)
CMS_BLOCK_TEMPLATES = [(i[0].split(os.path.sep)[-1], i[0].split(os.path.sep)[-1])  for i in
                       [glob(f"{e}/*.html") for e in CMS_BLOCK_TEMPLATES_FOLDERS]
                       if len(i) > 0
                      ]

CMS_PAGE_TEMPLATES_FOLDERS = (f'{BASE_DIR}/templates/pages',)
CMS_PAGE_TEMPLATES = [(i[0].split(os.path.sep)[-1], i[0].split(os.path.sep)[-1]) for i in
                       [glob(f"{e}/*.html") for e in CMS_PAGE_TEMPLATES_FOLDERS]
                      if len(i) > 0
                      ]
if CMS_BLOCK_TEMPLATES:
    logger.info('Loading block template files:{}'.format('\n  '.join([i[1] for i in CMS_BLOCK_TEMPLATES])))
else:
    logger.warning('Block template files not found')

if CMS_PAGE_TEMPLATES:
    logger.info('Loading page template files: {}'.format(','.join([i[1] for i in CMS_PAGE_TEMPLATES])))
else:
    logger.warning('Page template files not found')

