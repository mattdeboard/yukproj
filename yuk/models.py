from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm, Form
from django import forms
from django.utils.encoding import smart_str
from tagging.models import Tag, TagManager
from urlparse import urlparse, urlunparse
import sys, urllib, datetime

class Url(models.Model):

        def __unicode__(self):
                return self.url

        url = models.URLField()
        url_name = models.CharField(max_length=200)
        tagstring = models.CharField(max_length=200)
        url_desc = models.TextField()
        user = models.ManyToManyField(User, through='UrlsToUsers')

        def save(self):
                super(Url, self).save()
                self.tags = self.tagstring

        def _get_tags(self):
                return Tag.objects.get_for_object(self)

        def _set_tags(self, tagstring):
                Tag.objects.update_tags(self, tagstring)

        tags = property(_get_tags, _set_tags)

class UrlsToUsers(models.Model):
        url = models.ForeignKey(Url)
        user = models.ForeignKey(User)
        date_added = models.DateField()
        class Meta:
                unique_together = ('url', 'user')
        
        
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
        tagstring = forms.CharField(label='tags separated by commas:', required=False)
        url_desc = forms.CharField(label='Description (max 500 chars):', widget=forms.Textarea, required=False)
        
        class Meta:
            model = Url
                
        def __init__(self, data=None, user=None, *args, **kwargs):
            super(UrlForm, self).__init__(data, *args, **kwargs)
            self.user = user

        def clean_url(self):
            url = self.cleaned_data['url']
            if UrlsToUsers.objects.filter(user=self.user).exists():
                print >> sys.stderr, 'exists'
                url_dicts = Url.objects.filter(user=self.user).values()
                for url_dict in url_dicts:
                    print >> sys.stderr, 'url_dict: %s' % url_dict.values()
                    if url in url_dict.values():
                        raise forms.ValidationError("This URL already exists for %s" % self.user)
            else:
                print >> sys.stderr, 'no exist'
                return url

        def save(self, *args, **kwargs):
            print >> sys.stderr, '1'
            url = super(UrlForm, self).save(*args, **kwargs)
            print >> sys.stderr, '2'
            UrlsToUsers.objects.create(url=url, user=self.user, date_added = datetime.datetime.now())
            print >> sys.stderr, '3'
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

        
