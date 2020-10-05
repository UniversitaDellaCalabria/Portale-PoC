from django import template
from datetime import date, timedelta
from pubblicazioni.models import *
import datetime, pytz
from pubblicazioni.models import Language
from django.shortcuts import render_to_response, get_object_or_404

register = template.Library()

# @register.assignment_tag
# def years(opt=None):
    ## sezione anni motore ricerca
    # anno_inizio = 2014
    # ultima_pub = Page.objects.last()
    # if ultima_pub:
        # if ultima_pub.data_inserimento.year == anno_inizio:
            # anni = [ 2014 ]
        # else:
            # anni = range( anno_inizio, ultima_pub.data_inserimento.year+1 )[::-1]
    # else:
        # anni = [ ]
    # return anni


@register.assignment_tag(takes_context=True)
def avvisi(context):
    timezone = pytz.timezone ("UTC")
    today = timezone.localize(datetime.datetime.now())    
    request = context['request']
    lang = request.session.get('lang')
    ele = Page.objects.filter(pubblicato=True, in_evidenza=True)\
                        .exclude(  data_fine_Page_evidenza__lte=today  )\
                        .exclude( categorie__nome__icontains='Bandi' ).exclude\
                         ( categorie__nome__icontains='Eventi' ).exclude\
                         ( categorie__nome__icontains='Organizzazione' ).exclude\
                         ( categorie__nome__icontains='Highlight' ).order_by('-data_modifica')
    if lang:
        language = Language.objects.filter(short_name=lang)
        if language: language = language[0]
        for i in ele:
            ele_trans = PageLocalization.objects\
                        .filter(Language=language, Page=i, pubblicato=True)
                        
            if ele_trans:
                ele_trans = ele_trans.order_by('-data_modifica')[0]
                #print ele_trans
                i.titolo = ele_trans.titolo
                i.catenaccio = ele_trans.catenaccio
                i.testo = ele_trans.testo
                #print ele.nome
        
    return ele    


@register.assignment_tag(takes_context=True)
def avvisi_didattica(context):
    timezone = pytz.timezone ("UTC")
    today = timezone.localize(datetime.datetime.now())    
    request = context['request']
    lang = request.session.get('lang')    
    ele = Page.objects.filter( categorie__nome__iexact='Didattica',pubblicato=True, in_evidenza=True ).order_by('-data_modifica')
    if lang:
        language = Language.objects.filter(short_name=lang)
        if language: language = language[0]
        for i in ele:
            print i
            ele_trans = PageLocalization.objects\
                        .filter(Language=language, Page=i, pubblicato=True)
                        
            if ele_trans:
                ele_trans = ele_trans.order_by('-data_modifica')[0]
                #print ele_trans
                i.titolo = ele_trans.titolo
                i.catenaccio = ele_trans.catenaccio
                i.testo = ele_trans.testo
                #print ele.nome
        
    return ele  


@register.assignment_tag(takes_context=True)
def avvisi_eventi(context):
    timezone = pytz.timezone ("UTC")
    today = timezone.localize(datetime.datetime.now())    
    request = context['request']
    lang = request.session.get('lang')        
    ele =Page.objects.filter( categorie__nome__iexact='Eventi',pubblicato=True, in_evidenza=True )\
                            .exclude(  data_fine_Page_evidenza__lte=today  ).order_by('-data_modifica')
    if lang:
        language = Language.objects.filter(short_name=lang)
        if language: language = language[0]        
        for i in ele:
            ele_trans = PageLocalization.objects\
                        .filter(Language=language, Page=i, pubblicato=True)
                        
            if ele_trans:
                ele_trans = ele_trans.order_by('-data_modifica')[0]
                #print ele_trans
                i.titolo = ele_trans.titolo
                i.catenaccio = ele_trans.catenaccio
                i.testo = ele_trans.testo
                #print ele.nome
        
    return ele    
    
@register.assignment_tag(takes_context=True)
def avvisi_bandi(context):
    timezone = pytz.timezone ("UTC")
    today = timezone.localize(datetime.datetime.now())  
    request = context['request']
    lang = request.session.get('lang')    
    ele = Page.objects.filter( categorie__nome__in=['Bandi', 'Organizzazione'], \
                          pubblicato=True, in_evidenza=True )\
                          .exclude(  data_fine_Page_evidenza__lte=today  )\
                          .order_by('-data_modifica')
    if lang:
        language = Language.objects.filter(short_name=lang)
        if language: language = language[0]        
        for i in ele:
            ele_trans = PageLocalization.objects\
                        .filter(Language=language, Page=i, pubblicato=True)
                        
            if ele_trans:
                ele_trans = ele_trans.order_by('-data_modifica')[0]
                #print ele_trans
                i.titolo = ele_trans.titolo
                i.catenaccio = ele_trans.catenaccio
                i.testo = ele_trans.testo
                #print ele.nome
        
    return ele


@register.assignment_tag(takes_context=True)
def categorie(context):
    timezone = pytz.timezone ("UTC")
    today = timezone.localize(datetime.datetime.now())    
    return PageCategory.objects.filter(is_active=True)


@register.assignment_tag(takes_context=True)
def highlights(context):
    timezone = pytz.timezone ("UTC")
    today = timezone.localize(datetime.datetime.now())
    request = context['request']
    lang = request.session.get('lang')        
    ele = Page.objects.filter(pubblicato=True, categorie__nome__iexact='Highlights').exclude\
                                       (categorie__nome__iexact='Avvisi',pubblicato=True, in_evidenza=True)\
                               .exclude(  data_fine_Page_evidenza__lte=today  )
    if lang:
        language = Language.objects.filter(short_name=lang)
        if language: language = language[0]
        for i in ele:
            ele_trans = PageLocalization.objects\
                        .filter(Language=language, Page=i, pubblicato=True)
                        
            if ele_trans:
                ele_trans = ele_trans.order_by('-data_modifica')[0]
                i.titolo = ele_trans.titolo
                i.catenaccio = ele_trans.catenaccio
                i.testo = ele_trans.testo
        
    return ele    
