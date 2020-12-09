from cms.medias.utils import get_file_type_size


def set_file_meta(media_object):
    data = get_file_type_size(media_object)
    media_object.file_size = data['file_size']
    media_object.file_type = data['mime_type']
    
