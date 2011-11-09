import datetime
from haystack import indexes
from yuk.models import Item

class ItemIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='user')
    private = indexes.CharField(model_attr='privacy_mode')
    url_id = indexes.CharField(model_attr='id')
    url = indexes.CharField(model_attr='url')
    url_name = indexes.CharField(model_attr='displays')
    url_desc = indexes.CharField(model_attr='description')
    tags = indexes.MultiValueField()

    def get_model(self):
        return Item

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return Item.objects.filter(date_created__lte=datetime.datetime.now())

    def prepare_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]

