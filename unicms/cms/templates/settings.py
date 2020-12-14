import logging
import os

from django.utils.translation import gettext_lazy as _

from glob import glob
from pathlib import Path

logger = logging.getLogger(__name__)
# logging.basicConfig(level=getattr(logging, 'DEBUG'))


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


CMS_TEMPLATE_BLOCK_SECTIONS = (
                                ('pre-head', _('Pre-Header')),
                                ('head', _('Header')),
                                ('menu-1', _('Navigation Main Menu')),
                                ('menu-2', _('Navigation Menu 2')),
                                ('menu-3', _('Navigation Menu 3')),
                                ('menu-4', _('Navigation Menu 4')),
                                ('slider', _('Carousel/Slider')),
                                ('slider-2', _('Carousel/Slider 2')),
                                # ('1','1'),
                                # ('2','2'),
                                # ('3','3'),
                                # ('4','4'),
                                # ('5','5'),
                                # ('6','6'),
                                # ('7','7'),
                                # ('8','8'),
                                # ('9','9'),
                                ('pre-footer', _('Pre-Footer')),
                                ('footer', _('Footer')),
                                ('post-footer', _('Post-Footer')),

                                # breadcrumbs
                                ('breadcrumbs', _('Breadcrumbs')),

                                # section 1
                                ('section-1',
                                    (
                                       ('1-top', _('Section 1 - Top')),
                                       ('1-left-a', _('Section 1 - Left A')),
                                       ('1-left-b', _('Section 1 - Left B')),
                                       ('1-center-top-1', _('Section 1 - Center Top 1')),
                                       ('1-center-top-2', _('Section 1 - Center Top 2')),
                                       ('1-center-top-3', _('Section 1 - Center Top 3')),
                                       # ('1-center-mid-top-1', _('Section 1 - Center Middle Top 1')),
                                       # ('1-center-mid-top-2', _('Section 1 - Center Middle Top 2')),
                                       # ('1-center-mid-top-3', _('Section 1 - Center Middle Top 3')),
                                       ('1-center-content', _('Section 1 - Center Content')),
                                       # ('1-center-mid-bottom-1', _('Section 1 - Center Middle Bottom 1')),
                                       # ('1-center-mid-bottom-2', _('Section 1 - Center Middle Bottom 2')),
                                       # ('1-center-mid-bottom-3', _('Section 1 - Center Middle Bottom 3')),
                                       ('1-center-bottom-1', _('Section 1 - Center Bottom 1')),
                                       ('1-center-bottom-2', _('Section 1 - Center Bottom 2')),
                                       ('1-center-bottom-3', _('Section 1 - Center Bottom 3')),
                                       ('1-right-a', _('Section 1 - Right A')),
                                       ('1-right-b', _('Section 1 - Right B')),
                                       ('1-bottom', _('Section 1 - Bottom')),
                                    )
                                ),

                                # section 2
                                ('section-2',
                                    (
                                       ('2-top', _('Section 2 - Top')),
                                       ('2-left-a', _('Section 2 - Left A')),
                                       ('2-left-b', _('Section 2 - Left B')),
                                       ('2-center-top-1', _('Section 2 - Center Top 1')),
                                       ('2-center-top-2', _('Section 2 - Center Top 2')),
                                       ('2-center-top-3', _('Section 2 - Center Top 3')),
                                       # ('2-center-mid-top-1', _('Section 2 - Center Middle Top 1')),
                                       # ('2-center-mid-top-2', _('Section 2 - Center Middle Top 2')),
                                       # ('2-center-mid-top-3', _('Section 2 - Center Middle Top 3')),
                                       ('2-center-content', _('Section 2 - Center Content')),
                                       # ('2-center-mid-bottom-1', _('Section 2 - Center Middle Bottom 1')),
                                       # ('2-center-mid-bottom-2', _('Section 2 - Center Middle Bottom 2')),
                                       # ('2-center-mid-bottom-3', _('Section 2 - Center Middle Bottom 3')),
                                       ('2-center-bottom-1', _('Section 2 - Center Bottom 1')),
                                       ('2-center-bottom-2', _('Section 2 - Center Bottom 2')),
                                       ('2-center-bottom-3', _('Section 2 - Center Bottom 3')),
                                       ('2-right-a', _('Section 2 - Right A')),
                                       ('2-right-b', _('Section 2 - Right B')),
                                       ('2-bottom', _('Section 2 - Bottom')),
                                    )
                                ),

                                # section 1
                                ('section-3',
                                    (
                                       ('3-top', _('Section 3 - Top')),
                                       ('3-left-a', _('Section 3 - Left A')),
                                       ('3-left-b', _('Section 3 - Left B')),
                                       ('3-center-top-1', _('Section 3 - Center Top 1')),
                                       ('31-center-top-2', _('Section 3 - Center Top 2')),
                                       ('3-center-top-3', _('Section 3 - Center Top 3')),
                                       # ('3-center-mid-top-1', _('Section 3 - Center Middle Top 1')),
                                       # ('3-center-mid-top-2', _('Section 3 - Center Middle Top 2')),
                                       # ('3-center-mid-top-3', _('Section 3 - Center Middle Top 3')),
                                       ('3-center-content', _('Section 3 - Center Content')),
                                       # ('3-center-mid-bottom-1', _('Section 3 - Center Middle Bottom 1')),
                                       # ('3-center-mid-bottom-2', _('Section 3 - Center Middle Bottom 2')),
                                       # ('3-center-mid-bottom-3', _('Section 3 - Center Middle Bottom 3')),
                                       ('3-center-bottom-1', _('Section 3 - Center Bottom 1')),
                                       ('3-center-bottom-2', _('Section 3 - Center Bottom 2')),
                                       ('3-center-bottom-3', _('Section 3 - Center Bottom 3')),
                                       ('3-right-a', _('Section 3 - Right A')),
                                       ('3-right-b', _('Section 3 - Right B')),
                                       ('3-bottom', _('Section 3 - Bottom')),
                                    )
                                ),
                              )

CMS_BLOCK_TYPES = (
                   ('cms.templates.blocks.NullBlock', 'Null Block'),
                   ('cms.templates.blocks.HtmlBlock', 'HTML Block'),
                   ('cms.templates.blocks.JSONBlock', 'JSON Block'),
)

CMS_TEMPLATES_FOLDER = f'{BASE_DIR}/templates/unicms'
CMS_BLOCK_TEMPLATES = []
blocks_templates_files = [glob(f"{CMS_TEMPLATES_FOLDER}/blocks/*.html")]
for i in blocks_templates_files[0]:
    fname = i.split(os.path.sep)[-1]
    CMS_BLOCK_TEMPLATES.append((fname, fname))

CMS_PAGE_TEMPLATES = []
pages_templates_files = [glob(f"{CMS_TEMPLATES_FOLDER}/pages/*.html") ]
for i in pages_templates_files[0]:
    fname = i.split(os.path.sep)[-1]
    CMS_PAGE_TEMPLATES.append((fname, fname))


if CMS_BLOCK_TEMPLATES:
    _elements = '\n  '.join([i[1] for i in CMS_BLOCK_TEMPLATES])
    logger.info('Loading block template files:{}'.format(_elements))
else:
    logger.warning('Block template files not found')

if CMS_PAGE_TEMPLATES:
    _elements = ','.join([i[1] for i in CMS_PAGE_TEMPLATES])
    logger.info('Loading page template files: {}'.format(_elements))
else:
    logger.warning('Page template files not found')

CMS_LINKS_LABELS = (('view', _('View')),
                    ('open', _('Open')),
                    ('read more', _('Read More')),
                    ('more', _('More')),
                    ('get in', _('Get in')),
                    ('enter', _('Enter')),
                    ('submit', _('Submit')),
                    ('custom', _('custom'))
                  )
