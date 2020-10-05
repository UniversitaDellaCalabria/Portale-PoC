import autocomplete_light
from models import Pubblicazione

class PubblicazioneAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields=['titolo']
    autocomplete_js_attributes = {'placeholder': 'titolo'}
    widget_attrs               = {'data-widget-maximum-values': 4}

autocomplete_light.register(Pubblicazione, PubblicazioneAutocomplete)
