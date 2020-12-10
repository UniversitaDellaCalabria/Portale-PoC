import logging
import os

from cms.medias.utils import get_file_type_size
from django.conf import settings
from io import BytesIO
from PIL import Image

from . import settings as app_settings


logger = logging.getLogger(__name__)
FILETYPE_IMAGE = getattr(settings, 'FILETYPE_IMAGE', 
                         app_settings.FILETYPE_IMAGE)


def set_file_meta(media_object):
    data = get_file_type_size(media_object)
    media_object.file_size = data['file_size']
    media_object.file_type = data['mime_type']

    
def image_optimizer(media_object):
    if media_object.file_type in FILETYPE_IMAGE:
        byte_io = BytesIO()
        if not hasattr(media_object.file, '_file'):
            return
        im = Image.open(media_object.file._file)
        try:
            im.save(byte_io, format = "WebP",  optimize=True, quality=66)
        except Exception as e:
            logger.exception(f'Media Hook image_optimized failed: {e}')
            return
        
        byte_io.seek(0, os.SEEK_END)
        content_size = byte_io.tell()
        
        byte_io.seek(0)
        target = media_object.file
        target._file.file = byte_io
        
        fname = '.'.join(media_object.file.name.split('.')[:-1])+'.webp'
        target._file._name = fname
        target.name = fname
        
        target._file.size = content_size
        target._file.content_type = 'image/webp'
        media_object.file_size = content_size
        media_object.file_type = 'image/webp'
        return True
