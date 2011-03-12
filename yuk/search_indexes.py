import datetime

from haystack.indexes import *
from haystack import site

from taggit.models import Tag

from yuk.models import Url, Note, Quote

class UrlIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    author = CharField(model_attr='user')
    private = CharField(model_attr='privacy_mode')
    url_id = CharField(model_attr='id')
    tags = MultiValueField()

    def get_queryset(self):
        """Used when the entire index for model is updated."""
        return Url.objects.filter(date_created__lte=datetime.datetime.now())

    def prepare_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]


site.register(Url, UrlIndex)
