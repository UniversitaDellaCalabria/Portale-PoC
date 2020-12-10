import logging
import os

from cms.medias.utils import get_file_type_size
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
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


def webp_image_optimizer(media_object):
    if media_object.file_type in FILETYPE_IMAGE:
        byte_io = BytesIO()
        if not hasattr(media_object.file, '_file'):
            return
        im = Image.open(media_object.file._file)
        try:
            im.save(byte_io, format = "WebP",  
                    optimize=True, quality=66)
        except Exception as e:
            logger.exception(f'Media Hook image_optimized failed: {e}')
            return
        
        byte_io.seek(0, os.SEEK_END)
        content_size = byte_io.tell()
        
        byte_io.seek(0)
        fname = '.'.join(media_object.file.name.split('.')[:-1])+'.webp'
        media_object.file._file= InMemoryUploadedFile(file = byte_io, 
                                                      name = fname,
                                                      content_type = 'image/webp',
                                                      size = content_size,
                                                      charset='utf-8',
                                                      field_name = 'file')
        media_object.file._file._name = fname
        media_object.file.name = fname

        media_object.file._file.size = content_size
        media_object.file._file.content_type = 'image/webp'
        
        media_object.file_size = content_size
        media_object.file_type = 'image/webp'
        return True


def remove_file(media_object):
    fpath = media_object.file.path
    try:
        os.remove(fpath)
    except Exception as e:
        _msg = 'Media Hook remove_file: {} cannot be removed: {}'
        logger.error(_msg.format(fpath, e))
