from django.contrib import admin

from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import ModelForm
from django import forms
import autocomplete_light



from models import *

class PubblicazioniAllegatiForm(forms.ModelForm):
    class Meta:
        model = Allegato
        # django 1.8, prevents "Creating a ModelForm without either the 'fields' attribute or the 'exclude' attribute is prohibited;"
        fields = '__all__'        

class PubblicazioniAllegatiInline(admin.TabularInline):
    form  = PubblicazioniAllegatiForm
    model = Allegato
    extra = 0


class PubblicazioniRelativeForm(forms.ModelForm):
    pubblicazione_relativa = forms.ModelChoiceField(Pubblicazione.objects.all(),
    widget=autocomplete_light.ChoiceWidget('PubblicazioneAutocomplete'))	
    class Meta:
        model = PubblicazioneRelativa
        # django 1.8, prevents "Creating a ModelForm without either the 'fields' attribute or the 'exclude' attribute is prohibited;"
        fields = '__all__'

class PubblicazioniRelativeInline(admin.TabularInline):
    form  = PubblicazioniRelativeForm
    model = PubblicazioneRelativa
    fk_name = 'pubblicazione'
    extra = 0

class PubblicazioneContestualeForm(forms.ModelForm):
    pubblicazione_relativa = forms.ModelChoiceField(Pubblicazione.objects.all(),
    widget=autocomplete_light.ChoiceWidget('PubblicazioneAutocomplete'))	
    class Meta:
        model = PubblicazioneContestuale
        # django 1.8, prevents "Creating a ModelForm without either the 'fields' attribute or the 'exclude' attribute is prohibited;"
        fields = '__all__'

class PubblicazioneContestualeInline(admin.TabularInline):
    form  = PubblicazioneContestualeForm
    model = PubblicazioneContestuale
    fk_name = 'pubblicazione'
    extra = 0

class PubblicazioniPhotogalleryForm(forms.ModelForm):
    class Meta:
        model = Photogallery
        fields = '__all__'        

class PubblicazioniPhotogalleryInline(admin.TabularInline):
    form  = PubblicazioniPhotogalleryForm
    model = Photogallery
    extra = 0

class LinksForm(forms.ModelForm):
    class Meta:
        model = Links
        fields = '__all__'        

class LinksInline(admin.TabularInline):
    form  = LinksForm
    model = Links
    extra = 0

class PubblicazioneMultilinguaForm(forms.ModelForm):
    pubblicazione= forms.ModelChoiceField(Pubblicazione.objects.all(),
    widget=autocomplete_light.ChoiceWidget('PubblicazioneAutocomplete'))	
    class Meta:
        model = PubblicazioneMultilingua
        # django 1.8, prevents "Creating a ModelForm without either the 'fields' attribute or the 'exclude' attribute is prohibited;"
        fields = '__all__'

class PubblicazioneMultilinguaInline(admin.TabularInline):
    form  = PubblicazioneMultilinguaForm
    model = PubblicazioneMultilingua
    fk_name = 'pubblicazione'
    extra = 0
