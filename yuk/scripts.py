from datetime import datetime

from django.contrib import messages
from yuk.models import Url

from BeautifulSoup import BeautifulSoup

def import_text_file(request):
    '''Allows import of bookmark text file using the pinboard/del.icio.us
    model of HTML exports. Each line containing a bookmark is marked by
    an unclosed <DT> tag, and a description set off by <DD></DD> tag.
    
    (Example of this: 

    <DT><A HREF="http://foo.com" TAGS="bar, baz, mu" PRIVATE="0">Foo</A>
    <DT><A HREF="http://bar.com" TAGS="tau, delta" PRIVATE="0">Bar</A>
    <DD>This is a description of a webpage about Bar.</DD>'''    
    
    attrs = {'href':'url', 
             'private':'privacy_mode', 
             'add_date':'date_created',
             'tags':'tags'}
    soup = BeautifulSoup(request.FILES['import_file'])
    alltags = soup.findAll('a')
    
    
    for item in alltags:
        # Create a new Url object for each <a> tag in the uploaded file.
        ts = float(item.get('add_date'))
        u = Url(user=request.user, url=item.get('href'), 
                url_name=item.text, privacy_mode=bool(int(item.get('private'))),
                date_created=datetime.fromtimestamp(ts))
        tags = item.get('tags').split(',')
        u.save()
        for tag in tags:
            u.tags.add(tag)
        u.save()

    
        
        