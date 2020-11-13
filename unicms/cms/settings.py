import logging
import os

from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)

CMS_IMAGE_CATEGORY_SIZE = 128
CMS_IMAGE_THUMBSIZE = 128

CMS_PUBLICATION_PREFIX_RESERVED_WORD = 'content/posts/'
CMS_PUBLICATION_URL_VIEW_REGEXP = f'(?P<context>[\/a-zA-Z0-9\.\-\_]*)({CMS_PUBLICATION_PREFIX_RESERVED_WORD})(?P<slug>[a-z0-9\-]*)'

CMS_APP_REGEXP_URLPATHS = {
    'cms.handlers.ContentViewHandler' : CMS_PUBLICATION_URL_VIEW_REGEXP,
}

# re.match(CMS_PUBLICATION_URL_REGEXP, '/content/posts/content/post/yessa-man-again-20')

# .groups()
# Out[29]: ('content/post/', 'yessa-man-again-20')

# .groupdict()
# {'slug': 'yessa-man-again-20'}
