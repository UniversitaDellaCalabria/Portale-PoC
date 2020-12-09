import logging
import magic
import os

logger = logging.getLogger(__name__)


def get_file_type_size(media_obj) -> dict:
    fopen = media_obj.file
    mime = magic.Magic(mime=True)
    fopen.seek(0)
    content_type = mime.from_buffer(fopen.read())
    fopen.seek(0, os.SEEK_END)
    content_size = fopen.tell()
    fopen.seek(0)
    data = dict(mime_type=content_type, file_size=content_size)
    logger.debug(f'Media item hook get_file_type_size: {data}')
    return data
