import sys
from urlparse import urlparse, urlunparse

from django.forms import ModelForm
from django import forms
from taggit.forms import TagField
from haystack.forms import SearchForm

from yuk.models import Item


class MySearchForm(SearchForm):
    q = forms.CharField(label="Search:",
                        widget=forms.TextInput(attrs={'size': '35',
                                                      'rows': '2'}))

    def __init__(self, load_all=True, *args, **kwargs):
        super(MySearchForm, self).__init__(*args, **kwargs)


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

    url = MyUrlField(label='URL:', widget=forms.TextInput(attrs={'size':'35'}), 
                     required=True)
    displays = forms.CharField(label = 'Name:', required=False,
                               widget=forms.TextInput(attrs={'size':'35'}))
    description = forms.CharField(label='Description (max 500 chars):',
                                  widget = forms.Textarea(attrs={'cols': '35',
                                                                 'rows':'10'}),
                                  required = False)
    privacy_mode = forms.BooleanField(label="Private?", required=False,
                                      widget=forms.CheckboxInput)
    
    class Meta:
        model = Item
        exclude = ('user', 'date_created', 'last_updated', 'item_type')
        fields = ('url', 'displays', 'description',  'tags', 'privacy_mode')

    def __init__(self, data=None, user=None, *args, **kwargs):
        super(UrlForm, self).__init__(data, *args, **kwargs)
        self.user = user
            
    def clean_url(self):
        url = self.cleaned_data['url']
        if self.user.item_set.filter(url=url).count():
            raise forms.ValidationError("You already saved this bookmark!")
        else:
            return url
    
    def clean_tags(self):
        tags = self.cleaned_data['tags']
        for tag in tags:
            tags[tags.index(tag)] = tag.lower()
        return tags
        

class UrlEditForm(ModelForm):
    url = MyUrlField(label='URL:', widget=forms.TextInput(attrs={'size':'35'}), 
                     required=True)
    displays = forms.CharField(label = 'Name:', required=False,
                               widget=forms.TextInput(attrs={'size':'35'}))
    description = forms.CharField(label='Description (max 500 chars):',
                                  widget = forms.Textarea(attrs={'cols': '35',
                                                                 'rows':'10'}),
                                  required = False)
    privacy_mode = forms.BooleanField(label="Private?", required=False,
                                      widget=forms.CheckboxInput)
    
    class Meta:
        model = Item
        exclude = ('user', 'date_created', 'last_updated', 'item_type')
        fields = ('url', 'displays', 'description',  'tags', 'privacy_mode')

    def __init__(self, data=None, user=None, *args, **kwargs):
        super(UrlEditForm, self).__init__(data, *args, **kwargs)
        self.user = user

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        for tag in tags:
            tags[tags.index(tag)] = tag.lower()
        return tags

class RssImportForm(ModelForm):
    url = MyUrlField(label="URL of RSS feed:", required=True)
    
    class Meta:
        model = Item
        exclude = ('user', 'date_created', 'last_updated', 'description',
                   'displays', 'privacy_mode', 'tags')

    def __init__(self, data=None, user=None, *args, **kwargs):
        super(RssImportForm, self).__init__(data, *args, **kwargs)
        self.user = user
        
    def clean_url(self):
        url = self.cleaned_data['url']
        if self.user.rssfeed_set.filter(url=url).count():
            raise forms.ValidationError("This URL already exists for %s" %
                                        self.user)
        else:
            return url

class BookmarkUploadForm(forms.Form):            
    
    filename = forms.CharField(max_length=50)
    import_file = forms.FileField()


class NoteForm(ModelForm):
    
    displays = forms.CharField(label='Title:', required=True,
                               widget=forms.TextInput(attrs={'size':'35'}))
    description = forms.CharField(label='Notes:',
                                  widget=forms.Textarea(attrs={'cols':'35',
                                                               'rows':'15'}),
                                  required=False)
    privacy_mode = forms.BooleanField(label="Private?", required=False,
                                      widget=forms.CheckboxInput)
    
    class Meta:
        model = Item
        exclude = ('user', 'date_created','url', 'last_updated')
        fields = ('displays', 'description', 'tags', 'privacy_mode')

    def __init__(self, data=None, user=None, *args, **kwargs):
        super(NoteForm, self).__init__(data, *args, **kwargs)
        self.user = user

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        for tag in tags:
            tags[tags.index(tag)] = tag.lower()
        return tags


class QuoteForm(ModelForm):
    
    description = forms.CharField(label='Quote:', 
                                  widget=forms.Textarea(attrs={'cols':'35', 
                                                               'rows':'15'}),
                                  required=True)
    displays = forms.CharField(label='Who said it?', required=True,
                               widget = forms.TextInput(attrs={'size':'35'}))
    privacy_mode = forms.BooleanField(label="Private?", required=False,
                                      widget=forms.CheckboxInput)
    tags = TagField(required=False)
    class Meta:
        model = Item
        exclude = ('user', 'date_created', 'url', 'last_updated')
        fields = ('description', 'displays', 'tags', 'privacy_mode')

    def __init__(self, data=None, user=None, *args, **kwargs):
        super(QuoteForm, self).__init__(data, *args, **kwargs)
        self.user = user

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        print >> sys.stderr, tags
        for tag in tags:
            tags[tags.index(tag)] = tag.lower()
        return tags
