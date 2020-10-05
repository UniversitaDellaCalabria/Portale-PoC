from django.utils.translation import gettext_lazy as _ 


CMS_CONTEXT_PERMISSIONS = (('-1', _('nothing')),
                           ('0', _('everything')),
                           ('1', _('can edit created by him/her')),
                           ('2', _('can edit all pages in his/her context')),
                           ('3', _('can edit all pages')),
                           ('4', _('can edit his/her own')),
                           ('5', _('can translate all pages in his/her context')),
                           ('6', _('can translate all pages')),
                           ('7', _('can publish created by him/her')),
                           ('8', _('can publish all pages in his/her context')),
                           ('9', _('can publish all pages')),
                           )
