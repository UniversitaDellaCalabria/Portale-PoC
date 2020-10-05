from django import forms
from .models import *
import autocomplete_light

import datetime, pytz

class PubblicazioneMultilinguaForm(forms.ModelForm):
    pubblicazione = forms.ModelChoiceField(Pubblicazione.objects.all(),
    widget=autocomplete_light.ChoiceWidget('PubblicazioneAutocomplete'))
    class Meta:
        model = PubblicazioneMultilingua
        fields = "__all__" 
