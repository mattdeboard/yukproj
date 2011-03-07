import urllib
import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import smart_str
from taggit.managers import TaggableManager


class GeneralModel(models.Model):
    #Abstract model for URL-centric sub-classes. URLs and RSS feeds use 
    #this abstract. A URL is mandatory for each instance of this model.
    user = models.ForeignKey(User)
    date_created = models.DateTimeField(default=datetime.datetime.now())
    last_updated = models.DateTimeField(default=datetime.datetime.now(), 
                                        auto_now=True)
    tags = TaggableManager()
    privacy_mode = models.BooleanField()
    url = models.URLField(verify_exists=False)

    class Meta:
        abstract = True
        ordering = ['-date_created']


class LongFormEntry(models.Model):
    #Abstract model for text area-centric sub-classes. Notes and quotes
    #use this abstract. URL field is optional here.
    url = models.URLField(verify_exists=False, blank=True)
    privacy_mode = models.BooleanField()
    date_created = models.DateTimeField(default=datetime.datetime.now())
    last_updated = models.DateTimeField(default=datetime.datetime.now(), 
                                        auto_now=True)
    tags = TaggableManager()
    user = models.ForeignKey(User)

    class Meta:
        abstract = True
        ordering = ['-date_created']


class Url(GeneralModel):

    def __unicode__(self):
        return self.url

    url_name = models.CharField(max_length=200)
    url_desc = models.TextField()
    source = models.CharField(max_length=200, default='UI')


class RssFeed(GeneralModel):

    def __unicode__(self):
        return self.url
        
    url_name = models.CharField(max_length=200)


class Note(LongFormEntry):
    
    def __unicode__(self):
        return self.title

    title = models.CharField(max_length=200)
    notes = models.TextField()


class Quote(LongFormEntry):

    def __unicode__(self):
        return self.source

    quote = models.TextField()
    source = models.CharField(max_length=200)
    
    
# Monkey-patch
def func_to_method(func, cls, name=None):
    import new
    method = new.instancemethod(func, None, cls)
    if not name:
        name = func.__name__
    setattr(cls, name, method)

def get_absolute_url(self):
    return '/u:%s' % urllib.quote(smart_str(self.username))

func_to_method(get_absolute_url, User)
