from yukproj.settings import SITE_URL

def site_url_processor(request):
    return {'site_url': SITE_URL}
