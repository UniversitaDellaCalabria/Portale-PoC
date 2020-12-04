import logging
import os

from django.conf import settings
from django.utils import timezone
from django.utils.module_loading import import_string

from . import settings as app_settings

logger = logging.getLogger(__name__)


CMS_PRESAVE_HOOKS = {k:[import_string(i) for i in v] 
                     for k,v in getattr(settings, 'CMS_PRESAVE_HOOKS', {}).items()}
CMS_POSTSAVE_HOOKS = {k:[import_string(i) for i in v]
                      for k,v in getattr(settings, 'CMS_POSTSAVE_HOOKS', {}).items()}


def load_app_settings():
    for i in dir(app_settings):
        if i[0] == '_': continue
        globals()[i] = getattr(settings, i, 
                               getattr(app_settings, i))


def remove_file(fpath):
    try:
        os.remove(fpath)
    except Exception as e:
        logger.error('{} cannot be removed: {}'.format(fpath, e))


def publication_base_filter():
    now = timezone.localtime()
    query_params = {'is_active': True,
                    'date_start__lte': now,
                    'date_end__gt': now
                    }
    return query_params


def publication_context_base_filter():
    pub_filter = publication_base_filter()
    pubcontx_filter = {f'publication__{k}':v 
                       for k,v in pub_filter.items()}
    pubcontx_filter['is_active'] = True
    return pubcontx_filter
    
        
def copy_page_as_draft(obj):
    draft = obj.__dict__.copy()
    draft['state'] = 'draft'
    draft['draft_of'] = obj.pk
    for attr in "id pk _state created_by modified_by created modified".split(' '):
        if draft.get(attr):
            draft.pop(attr)
    
    draft['date_start'] = timezone.localtime()
    new_obj = obj.__class__.objects.create(**draft)
    tags = [i for i in obj.tags.values_list('name', flat=1)]
    new_obj.tags.add(*tags)
    
    # now replicate all its childs and menus
    for i in ('pageblock_set', 'pagecarousel_set', 
              'pagelink_set', 'pagemenu_set'):
        childs = getattr(obj, i).all()
        for child in childs:
            child.pk = None
            child.id = None
            child.page = new_obj
            child.save()
    return new_obj


def save_hooks(obj, *args, **kwargs):
    _msg_hook_exp = 'Save Hook {} failed with: {}'
    # pre-Save HOOKS call
    for hook in CMS_PRESAVE_HOOKS.get(obj.__class__.__name__, {}):
        try:
            hook(obj)
        except Exception as e:
            logger.exception(_msg_hook_exp.format(hook, e))
        
    super(obj.__class__, obj).save(*args, **kwargs)
    
    # post-Save HOOKS call
    for hook in CMS_POSTSAVE_HOOKS.get(obj.__class__.__name__, {}):
        try:
            hook(obj)
        except Exception as e:
            logger.exception(_msg_hook_exp.format(hook, e))
