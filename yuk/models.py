from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from django.utils.encoding import smart_str
from taggit.managers import TaggableManager
from urlparse import urlparse, urlunparse
import sys, urllib, datetime

class Url(models.Model):

    def __unicode__(self):
        return self.url

    url = models.URLField(verify_exists=False)
    url_name = models.CharField(max_length=200)
    url_desc = models.TextField()
    user = models.ForeignKey(User)
    date_created = models.DateTimeField(default=datetime.datetime.now(), auto_now=True, auto_now_add=True)
    source = models.CharField(max_length=200, default='UI')
    tags = TaggableManager()

class RssFeed(models.Model):

    def __unicode__(self):
        return self.url

    url = models.URLField(verify_exists=False)
    url_name = models.CharField(max_length=200)
    last_checked = models.DateTimeField(default=datetime.datetime.now(), auto_now=True, auto_now_add=True)
    user = models.ForeignKey(User)
    date_created = models.DateTimeField(default=datetime.datetime.now(), auto_now=True, auto_now_add=True)

    tags = TaggableManager()
    

    
##    def update(self):
##        urls = rssdownload(self.user, self.url)
##        for i in urls['messages']:
##            u = Url(url=i['url'], date_created=i['timestamp'], user=self.user, url_name=i['url_name'])
##            u.save()

class MyUrlField(forms.URLField):

    def to_python(self, value):
        '''Lowercase the URL input for validation.'''
        if '://' in value:
            return self.lowercase_domain(value)
        else:
            return self.lowercase_domain('http://%s' % value)

    def lowercase_domain(self, url):
        parsed = urlparse(url)
        retval = urlunparse((parsed.scheme,
                             parsed.netloc.lower(),
                             parsed.path,
                             parsed.params,
                             parsed.query,
                             parsed.fragment))
        if url.endswith('?') and not retval.endswith('?'):
            retval += '?'
        return retval
        
class UrlForm(ModelForm):
    
    url = MyUrlField(label='URL:')
    url_name = forms.CharField(label='Name:', required=False)
    url_desc = forms.CharField(label='Description (max 500 chars):', widget=forms.Textarea(attrs={'cols':'20'}), required=False)
                                          
    class Meta:
        model = Url
        exclude = ('user', 'date_created')

    def __init__(self, data=None, user=None, *args, **kwargs):
        super(UrlForm, self).__init__(data, *args, **kwargs)
        self.user = user
            
    def clean_url(self):
        url = self.cleaned_data['url']
        if self.user.url_set.filter(url=url).count():
            print >> sys.stderr, 'exist'
            raise forms.ValidationError("This URL already exists for %s" % self.user)
        else:
            print >> sys.stderr, 'no exist'
            return url

class UrlEditForm(ModelForm):
    
    url = MyUrlField(label='URL:')
    url_name = forms.CharField(label='Name:', required=False)
    url_desc = forms.CharField(label='Description (max 500 chars):', widget=forms.Textarea(attrs={'cols':'20'}), required=False)
    
    class Meta:
        model = Url
        exclude = ('user', 'date_created')

    def __init__(self, data=None, user=None, *args, **kwargs):
        super(UrlEditForm, self).__init__(data, *args, **kwargs)
        self.user = user

class RssImportForm(ModelForm):
    url = MyUrlField(label="URL of RSS feed:")

    class Meta:
        model = RssFeed
        exclude = ('user', 'date_created', 'last_checked', 'url_desc')

    def __init__(self, data=None, user=None, *args, **kwargs):
        super(RssImportForm, self).__init__(data, *args, **kwargs)
        self.user = user
        
    def clean_url(self):
        url = self.cleaned_data['url']
        if self.user.rssfeed_set.filter(url=url).count():
            print >> sys.stderr, 'exist'
            raise forms.ValidationError("This URL already exists for %s" % self.user)
        else:
            print >> sys.stderr, 'no exist'
            return url
            
# Monkey-patch
def func_to_method(func, cls, name=None):
    import new
    method = new.instancemethod(func, None, cls)
    if not name: name = func.__name__
    setattr(cls, name, method)

def get_absolute_url(self):
    return '/u:%s' % urllib.quote(smart_str(self.username))

func_to_method(get_absolute_url, User)
