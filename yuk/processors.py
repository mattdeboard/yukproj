import os

from yuk.forms import MySearchForm

from yuk.settings import SITE_URL, MEDIA_URL, BLUEPRINT_PATH
from yuk.localsettings import SITE_URL as LOCAL_SITE_URL
from yuk.localsettings import MEDIA_URL as LOCAL_MEDIA_URL
from yuk.localsettings import BLUEPRINT_PATH as LOCAL_BLUEPRINT_PATH

def site_url_processor(request):
    if os.environ['DJANGO_SETTINGS_MODULE'] == 'yuk.localsettings':
        return {'site_url': LOCAL_SITE_URL, 
                'media_url': LOCAL_MEDIA_URL, 
                'blueprint_path': LOCAL_BLUEPRINT_PATH}

    return {'site_url': SITE_URL, 
            'media_url': MEDIA_URL, 
            'blueprint_path': BLUEPRINT_PATH}

def text_area_processor(request):
    '''Processor to make handling text area widgets in templates a little 
    easier.'''
    return {'text_areas':['url_desc', 'notes', 'quote']}

def search_processor(request):
    return {'search_form': MySearchForm()}