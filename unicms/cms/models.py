import logging

from django.contrib.auth import get_user_model()
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _ 

from cms_context.models import *
from mdeditor.fields import MDTextField

logger = logging.getLogger(__name__)


class Category(TimeStampedModel):
    name        = models.CharField(max_length=160, blank=False, 
                                   null=False, unique=False)
    description = models.TextField(max_length=1024, 
                                   null=False, blank=False)
    image       = models.ImageField(upload_to="page_categories/images/", 
                                    null=True, blank=True, 
                                    max_length=254)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = _("Category")
    
    def __str__(self):
        return self.name
    
    def image_as_html(self):
        if getattr(self.image, 'url', None):
            src_img = self.image.url
        else:
            src_img = "{}/images/no-image.jpg".format(settings.STATIC_URL)
        return '<img width={} src="{}"/>'.format(src_img)
        
    image_as_html.short_description = _('Image of this Category')
    image_as_html.allow_tags = True


class SubCategory(TimeStampedModel):
    name = models.CharField(max_length=160, 
                            blank=False, null=False, unique=False)
    category = models.ForeignKey(PageCategory, 
                                 null=False, blank=False)
    description  = models.TextField(max_length=1024, 
                                    null=False, blank=False)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = _("SubCategory")
    
    def __str__(self):
        return self.name


class PageTemplate(TimeStampedModel):
    name = 


class Page(TimeStampedModel):
    title        = models.CharField(max_length=126, 
                                    null=False,blank=False)    
    created_by = models.ForeignKey(get_user_model(), 
                                   related_name='created_by', 
                                   null=True, blank=True)
    modified_by = models.ForeignKey(get_user_model(), 
                                    related_name='modified_by', 
                                    null=True, blank=True)
    
    catenaccio    = RichTextUploadingField(max_length=1024, null=True,blank=True, help_text="max 1024 caratteri")
#    testo         = HTMLField(max_length=4096, null=True,blank=True,       help_text="max 4096 caratteri")
    testo         = RichTextUploadingField(max_length=12000, null=True,blank=True,       help_text="max 12000 caratteri")
    categorie     = models.ManyToManyField(PageCategory, null=True,blank=True)
    sotto_categorie     = models.ManyToManyField(SottoPageCategory, null=True,blank=True) 
    nota          = models.TextField(max_length=256, null=True,blank=True)
    pubblicato    = models.BooleanField()
    in_evidenza    = models.BooleanField()    
#    in_evidenza_catenaccio_html = models.BooleanField()
    rimuovi_data = models.BooleanField()    
    rimuovi_titolo = models.BooleanField()        
    data_inizio_Page_evidenza = models.DateTimeField(null=True,blank=True)
    data_fine_Page_evidenza = models.DateTimeField(null=True,blank=True)
    slug          = models.SlugField(unique=True)
    
    def delete(self, *args, **kwargs):
        pubs = PageRelativa.objects.filter(Page_relativa=self)
        for pubss in pubs:
            pubss.delete()
        super(Page, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        super(Page, self).save(*args, **kwargs)
        for rel in PageRelativa.objects.filter(Page=self):
            if not PageRelativa.objects.filter\
            (Page=rel.Page_relativa, Page_relativa=self):   
                PageRelativa.objects.create\
                (Page=rel.Page_relativa, Page_relativa=self, is_active=True)    
    
    class Meta:
        #db_table = u'dipartimenti'
        ordering = ['created']
        verbose_name_plural = "contenuti sito DIATIC.unical.it"   
        
    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id_tabella,))
        
    def get_thumbnail(self):
        import re
        a = re.findall( '<img.*/>', self.testo)
        if a: return a[0]
        #else: return ['',]
        
    def get_translation(self, lang_id):
        pub = PageMultiLanguage.objects\
              .filter(Language__pk=lang_id, Page=self, pubblicato=True)\
              .order_by('-created')
        if pub: return pub
    
    def get_categorie_img(self):
        l = []
        for i in self.categorie.all():
            l.append( i.get_img() )
        return l  
    
    def __str__(self):
        return smart_unicode('%s' % self.titolo)


class Language(TimeStampedModel):
    id_tabella          = models.AutoField(primary_key=True)
    name                = models.CharField(max_length=160, blank=False, 
                                           null=False, unique=False)
    short_name          = models.CharField(max_length=12, 
                                           blank=False, null=False)
    created    = models.DateTimeField(auto_now=True)
    icon                = models.ImageField(upload_to="languages_icons/", 
                                            null=True, blank=True, max_length=133)    
    is_active           = models.BooleanField()
    
    class Meta:
        ordering = ['nome']
        verbose_name_plural = "Lingue"        
    
    def __str__(self):
        return self.nome


class PageMultiLanguage(TimeStampedModel):
    id_tabella = models.AutoField(primary_key=True)
    page       = models.ForeignKey(Page, null=False, blank=False)    
    Language              = models.ForeignKey(Language, null=False, blank=False, default=Language.objects.get(short_name='en'))    
    #name = models.CharField(max_length=160, blank=False, null=False, unique=False)
    created = models.DateTimeField(auto_now=True)
    modificato_da = models.ForeignKey(get_user_model(), related_name='mod_da', null=True, blank=True)
    data_modifica = models.DateTimeField(auto_now_add=True)
    titolo        = models.CharField(max_length=127, null=False,blank=False)
    catenaccio    = RichTextField(max_length=1024, null=True,blank=True)
    testo         = RichTextField(max_length=12000, null=True,blank=True,       help_text="max 12000 caratteri")
    nota          = models.TextField(max_length=256, null=True,blank=True)
    pubblicato    = models.BooleanField()
    #def save(self, *args, **kwargs):
        #self.name = self.nome.upper()
        #super(Istituzioni, self).save(*args, **kwargs)
    class Meta:
        #db_table = u'dipartimenti'
        ordering = ['created']
        verbose_name_plural = "Traduzioni contenuti sito DIATIC.unical.it"
        unique_together = ("Page", "Language")
    def __str__(self):
        return '%s - %s' % (self.page, self.Language)


class PageRelated(TimeStampedModel):
    id_tabella = models.AutoField(primary_key=True)
    Page                = models.ForeignKey(Page, null=False, blank=False, related_name='parent')    
    Page_relativa       = models.ForeignKey(Page, null=False, blank=False, related_name="pub_rel")    
    created = models.DateTimeField(auto_now=True)
    data_modifica = models.DateTimeField(auto_now_add=True)
    ordine = models.IntegerField(null=True, blank=True,)
    is_active    = models.BooleanField()
    class Meta:
        ordering = ['ordine']
        verbose_name_plural = "Pubblicazioni collegate"
        unique_together = ("Page", "Page_relativa")
    def __str__(self):
        return smart_unicode('%s - %s' % (self.Page, self.Page_relativa))


class PageContestuale(TimeStampedModel):
    id_tabella = models.AutoField(primary_key=True)
    Page                = models.ForeignKey(Page, null=False, blank=False, related_name='parent_contx')    
    Page_relativa       = models.ForeignKey(Page, null=False, blank=False, related_name="pub_rel_contx")    
    created = models.DateTimeField(auto_now=True)
    data_modifica = models.DateTimeField(auto_now_add=True)
    ordine = models.IntegerField()
    is_active    = models.BooleanField()
    class Meta:
        #db_table = u'dipartimenti'
        ordering = ['ordine']
        verbose_name_plural = "Pubblicazioni contestuali"
        unique_together = ("Page", "Page_relativa")
    def __str__(self):
        return smart_unicode('%s - %s' % (self.Page, self.Page_relativa))


class Attachment(TimeStampedModel):
    id_tabella          = models.AutoField(primary_key=True)
    name                = models.CharField(max_length=256, blank=False, null=False, unique=False)
    docfile             = models.FileField(upload_to='allegati/%Y/%m/%d')
    Page       = models.ForeignKey(Page, null=False, blank=False)
    created    = models.DateTimeField(auto_now=True)
    data_Page  = models.DateTimeField(null=True,blank=True)    
    is_active           = models.BooleanField()
    
    class Meta:
        ordering = ['-data_Page']
        verbose_name_plural = "Allegati"        
    def __str__(self):
        return '%s' % self.nome


class Photogallery(TimeStampedModel):
    photo      = models.FileField(upload_to='photogallery/%Y/%m/%d')
    page       = models.ForeignKey(Page, null=False, blank=False)
    created    = models.DateTimeField(auto_now=True)
    data_Page  = models.DateTimeField(null=True,blank=True)    
    is_active  = models.BooleanField()
    
    class Meta:
        ordering = ['data_page']
        verbose_name_plural = "Photogallery"    
    
    def __str__(self):
        return '%s' % self.photo


class Link(TimeStampedModel):
    name               = models.CharField(max_length=160, blank=False, null=False)
    url               = models.CharField(max_length=512, blank=False, null=False)
    page       = models.ForeignKey(Page, null=False, blank=False)    
    created    = models.DateTimeField(auto_now=True)
    data_Page  = models.DateTimeField(null=True,blank=True)    
    is_active           = models.BooleanField()
    class Meta:
        ordering = ['-data_page']
        verbose_name_plural = "Links esterni"        
    def __str__(self):
        return '%s' % self.nome
