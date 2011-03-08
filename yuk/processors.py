from yukproj.settings import SITE_URL, MEDIA_URL

def site_url_processor(request):
    return {'site_url': SITE_URL, 'media_url': MEDIA_URL}

def text_area_processor(request):
    '''Processor to make handling text area widgets in templates a little 
    easier.'''
    return {'text_areas':['url_desc', 'notes', 'quote']}

