import urllib
import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import smart_str
from taggit.managers import TaggableManager


class Item(models.Model):

    user = models.ForeignKey(User)
    url = models.URLField(verify_exists=False, blank=True, max_length=500)
    date_created = models.DateTimeField(default=datetime.datetime.now())
    last_updated = models.DateTimeField(default=datetime.datetime.now(), 
                                        auto_now=True)
    tags = TaggableManager()
    privacy_mode = models.BooleanField()
    # 'displays' attribute is "source" for QuoteItem, "title" for 
    # NoteItem and Bookmark.
    displays = models.CharField(max_length=500, blank=True)
    # URL description for bookmarks, text of the quote for QuoteItems,
    # text of the note for Notes.
    description = models.CharField(max_length=500)
    # bookmark, note or quote
    item_type = models.CharField(max_length=200)

    class Meta:
        ordering = ['-date_created']


# monkey-patch to get my profile page URLs how I want them.
def func_to_method(func, cls, name=None):
    import new
    method = new.instancemethod(func, None, cls)
    if not name:
        name = func.__name__
    setattr(cls, name, method)

def get_absolute_url(self):
    return '/u:%s' % urllib.quote(smart_str(self.username))

func_to_method(get_absolute_url, User)

