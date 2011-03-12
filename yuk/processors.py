import os

from yuk.forms import MySearchForm

from yukproj.settings import SITE_URL, MEDIA_URL
from yukproj.localsettings import SITE_URL as LOCAL_SITE_URL
from yukproj.localsettings import MEDIA_URL as LOCAL_MEDIA_URL


def site_url_processor(request):
    if os.environ['DJANGO_SETTINGS_MODULE'] == 'yukproj.localsettings':
        return {'site_url': LOCAL_SITE_URL, 'media_url': LOCAL_MEDIA_URL}

    return {'site_url': SITE_URL, 'media_url': MEDIA_URL}

def text_area_processor(request):
    '''Processor to make handling text area widgets in templates a little 
    easier.'''
    return {'text_areas':['url_desc', 'notes', 'quote']}

def search_processor(request):
    return {'search_form': MySearchForm()}