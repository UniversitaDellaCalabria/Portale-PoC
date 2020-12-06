from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

DEFAULT_LANGUAGE = dict(settings.LANGUAGES)[settings.LANGUAGE].lower()


class SearchEntry(BaseModel):
    title : str
    heading : str
    content_type : str
    content_id : int
    content : Optional[str]
    sites : List[str]
    urls : List[str]
    tags : Optional[list]
    categories : Optional[list] = []
    indexed : datetime
    viewed : Optional[int]
    relevance : Optional[int]
    language : Optional[str]
    translations : List[dict] = []
    day : int
    month : int
    year : int
    
    # class Config:
        # arbitrary_types_allowed = True


def page_to_entry(page_object):
    app_label, model = page_object._meta.label_lower.split('.')
    contentype = ContentType.objects.get(app_label=app_label, model=model)
    sites = [page_object.webpath.site.domain]
    data = {
        "title": page_object.name,
        "heading": page_object.description,
        "content_type": page_object._meta.label,
        "content_id": page_object.pk,
        "content": "",
        "sites": sites,
        "urls": [f'{sites[0]}{page_object.webpath.get_full_path()}',],
        "tags": [i for i in page_object.tags.values_list('name', flat=1)],
        "indexed": timezone.localtime(),
        "viewed": 0,
        "language": DEFAULT_LANGUAGE,
        "day": page_object.date_start.day,
        "month": page_object.date_start.month,
        "year": page_object.date_start.year
    }
    search_entry = SearchEntry(**data)
    return search_entry


def publication_to_entry(pub_object):
    app_label, model = pub_object._meta.label_lower.split('.')
    contentype = ContentType.objects.get(app_label=app_label, model=model)
    contexts = pub_object.publicationcontext_set.filter(is_active=True)
    if not contexts:
        # it doesn't have any real publication
        return
    urls = set([f'//{i.webpath.site.domain}{i.url}' for i in contexts])
    sites = set([f'//{i.webpath.site.domain}' for i in contexts])
    data = {
        "title": pub_object.title,
        "heading": pub_object.subheading,
        "content_type": pub_object._meta.label,
        "content_id": pub_object.pk,
        "content": pub_object.content,
        "sites": list(sites),
        "urls": list(urls),
        "categories": [i.name for i in pub_object.categories.all()],
        "tags": [i for i in pub_object.tags.values_list('name', flat=1)],
        "indexed": timezone.localtime(),
        "published": pub_object.date_start,
        "viewed": 0,
        "language": DEFAULT_LANGUAGE,
        "day": pub_object.date_start.day,
        "month": pub_object.date_start.month,
        "year": pub_object.date_start.year
    }
    search_entry = SearchEntry(**data)
    return search_entry