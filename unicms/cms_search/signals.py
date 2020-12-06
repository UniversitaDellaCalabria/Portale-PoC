from django.contrib.auth.models import User
from django.db.models.signals import (pre_save, post_save,
                                      pre_delete, post_delete)

from cms.models import Page, Publication
from cms.utils import load_hooks


def cms_pre_save(instance, *args, **kwargs):
    load_hooks(instance, 'PRESAVE', *args, **kwargs)

def cms_post_save(instance, *args, **kwargs):
    load_hooks(instance, 'POSTSAVE', *args, **kwargs)

def cms_pre_delete(instance, *args, **kwargs):
    load_hooks(instance, 'PREDELETE', *args, **kwargs)

def cms_post_delete(instance, *args, **kwargs):
    load_hooks(instance, 'POSTDELETE', *args, **kwargs)


# Page
pre_save.connect(cms_pre_save, sender=Page)
post_save.connect(cms_post_save, sender=Page)
pre_delete.connect(cms_pre_delete, sender=Page)
post_delete.connect(cms_post_delete, sender=Page)

# Publication
pre_save.connect(cms_pre_save, sender=Publication)
post_save.connect(cms_post_save, sender=Publication)
pre_delete.connect(cms_pre_delete, sender=Publication)
post_delete.connect(cms_post_delete, sender=Publication)
