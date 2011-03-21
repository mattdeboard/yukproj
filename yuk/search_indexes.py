import datetime
from haystack.indexes import *
from haystack import site
from yuk.models import Item

class ItemIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    author = CharField(model_attr='user')
    private = CharField(model_attr='privacy_mode')
    url_id = CharField(model_attr='id')
    url = CharField(model_attr='url')
    url_name = CharField(model_attr='displays')
    url_desc = CharField(model_attr='description')
    tags = MultiValueField()

    def get_queryset(self):
        """Used when the entire index for model is updated."""
        return Item.objects.filter(date_created__lte=datetime.datetime.now())

    def prepare_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]


site.register(Item, ItemIndex)
