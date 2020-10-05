from django.contrib import admin
from .models import *
from .forms import * 

#from mce_filebrowser.admin import MCEFilebrowserAdmin
from admin_inline_fk import *

class CategoriaAdmin(admin.ModelAdmin):
    #search_fields = ['codice_stazione_regione']
    list_display  = [ 'nome', 'get_img', 'is_active',  ]
    readonly_fields = ['nome', ]
    list_editable = ['is_active', ]
    #list_filter   = [ 'comune', 'provincia' ]
    pass
admin.site.register(Categoria, CategoriaAdmin)

class SottoCategoriaAdmin(admin.ModelAdmin):
    #search_fields = ['codice_stazione_regione']
    #list_display  = [ 'codice_stazione_regione', 'nome', 'comune', 'gboaga_est', 'gboaga_nord',  ]
    #list_filter   = [ 'comune', 'provincia' ]
    pass
admin.site.register(SottoCategoria, SottoCategoriaAdmin)

class PubblicazioneAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('titolo',), }
    search_fields = ['titolo']
    list_display  = [ 'titolo', 'slug', 'data_inserimento', 'data_modifica', 'pubblicato', 'in_evidenza'  ] # 'categorie', 'sotto_categorie',
    list_filter   = [ 'categorie', 'pubblicato', 'in_evidenza' , 'data_inserimento', 'data_modifica', 'modificato_da'  ] # 'categorie', 'sotto_categorie',
    inlines       = [ PubblicazioniAllegatiInline , PubblicazioneContestualeInline, PubblicazioniRelativeInline, PubblicazioniPhotogalleryInline,  LinksInline, PubblicazioneMultilinguaInline]
    def save_model(self, request, obj, form, change):
        obj.modificato_da = request.user # no need to check for it.
        obj.save()
admin.site.register(Pubblicazione, PubblicazioneAdmin)

class LinguaAdmin(admin.ModelAdmin):
    #search_fields = ['codice_stazione_regione']
    #list_display  = [ 'codice_stazione_regione', 'nome', 'comune', 'gboaga_est', 'gboaga_nord',  ]
    #list_filter   = [ 'comune', 'provincia' ]
    pass
admin.site.register(Lingua, LinguaAdmin)

class PubblicazioneMultilinguaAdmin(admin.ModelAdmin):
    form = PubblicazioneMultilinguaForm
    #search_fields = ['codice_stazione_regione']
    #list_display  = [ 'codice_stazione_regione', 'nome', 'comune', 'gboaga_est', 'gboaga_nord',  ]
    #list_filter   = [ 'comune', 'provincia' ]
    pass
admin.site.register(PubblicazioneMultilingua, PubblicazioneMultilinguaAdmin)

class AllegatoAdmin(admin.ModelAdmin):
    #search_fields = ['codice_stazione_regione']
    #list_display  = [ 'codice_stazione_regione', 'nome', 'comune', 'gboaga_est', 'gboaga_nord',  ]
    #list_filter   = [ 'comune', 'provincia' ]
    pass
admin.site.register(Allegato, AllegatoAdmin)

class PhotogalleryAdmin(admin.ModelAdmin):
    #search_fields = ['codice_stazione_regione']
    #list_display  = [ 'codice_stazione_regione', 'nome', 'comune', 'gboaga_est', 'gboaga_nord',  ]
    #list_filter   = [ 'comune', 'provincia' ]
    pass
admin.site.register(Photogallery, PhotogalleryAdmin)

