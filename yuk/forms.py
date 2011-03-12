from urlparse import urlparse, urlunparse

from django.forms import ModelForm
from django import forms

from haystack.forms import SearchForm

from yuk.models import Url, RssFeed, Note, Quote


class MySearchForm(SearchForm):
    q = forms.CharField(label="Search:",
                        widget=forms.TextInput(attrs={'size': '15'}))

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

    url = MyUrlField(label='URL:')
    url_name = forms.CharField(label = 'Name:', required=False)
    url_desc = forms.CharField(label = 'Description (max 500 chars):',
                               widget = forms.Textarea(attrs={'cols': '35', 
                                                              'rows':'15'}),
                               required = False)
    privacy_mode = forms.BooleanField(label="Private?", required=False,
                                      widget=forms.CheckboxInput)
    
    class Meta:
        model = Url
        exclude = ('user', 'date_created', 'source', 'last_updated')
        fields = ('url', 'url_name', 'url_desc',  'tags', 'privacy_mode')

    def __init__(self, data=None, user=None, *args, **kwargs):
        super(UrlForm, self).__init__(data, *args, **kwargs)
        self.user = user
            
    def clean_url(self):
        url = self.cleaned_data['url']
        if self.user.url_set.filter(url=url).count():
            raise forms.ValidationError("This URL already exists for %s" %
                                        self.user)
        else:
            return url
    
    def clean_tags(self):
        tags = self.cleaned_data['tags']
        for tag in tags:
            tags[tags.index(tag)] = tag.lower()
        return tags
        

class UrlEditForm(ModelForm):
    
    url = MyUrlField(label='URL:')
    url_name = forms.CharField(label='Name:', required=False)
    url_desc = forms.CharField(label='Description (max 500 chars):',
                               widget=forms.Textarea(attrs={'cols': '35', 
                                                            'rows':'15'}),
                               required=False)
    privacy_mode = forms.BooleanField(label = "Private?", required=False,
                                      widget=forms.CheckboxInput)

    class Meta:
        model = Url
        exclude = ('user', 'date_created', 'source', 'last_updated')
        fields = ('url', 'url_name', 'url_desc',  'tags', 'privacy_mode')

    def __init__(self, data=None, user=None, *args, **kwargs):
        super(UrlEditForm, self).__init__(data, *args, **kwargs)
        self.user = user

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        for tag in tags:
            tags[tags.index(tag)] = tag.lower()
        return tags

class RssImportForm(ModelForm):
    url = MyUrlField(label="URL of RSS feed:")
    
    class Meta:
        model = RssFeed
        exclude = ('user', 'date_created', 'last_updated', 'url_desc')

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
    
    title = forms.CharField(label='Title:', required=True)
    notes = forms.CharField(label='Notes:',
                            widget=forms.Textarea(attrs={'cols':'35',
                                                         'rows':'15'}),
                            required=False)
    privacy_mode = forms.BooleanField(label="Private?", required=False,
                                      widget=forms.CheckboxInput)
    tags = forms.CharField(label='Tags (optional):', required=False)
    
    class Meta:
        model = Note
        exclude = ('user', 'date_created', 'last_updated', 'url')
        fields = ('title', 'notes', 'tags', 'privacy_mode')


class QuoteForm(ModelForm):
    
    quote = forms.CharField(label='Quote:', 
                            widget=forms.Textarea(attrs={'cols':'35', 
                                                         'rows':'15'}),
                            required=False)
    source = forms.CharField(label='Who said it?', required=False)
    tags = forms.CharField(label='Tags (optional):', required=False)
    privacy_mode = forms.BooleanField(label="Private?", required=False,
                                      widget=forms.CheckboxInput)

    class Meta:
        model = Quote
        exclude = ('user', 'date_created', 'last_updated', 'url')
        fields = ('quote', 'source', 'tags', 'privacy_mode')
    
class UrlFormRemote(ModelForm):
    '''Bookmark form for the javascript bookmarklet view.'''
    url = MyUrlField(label='URL:')
    url_name = forms.CharField(label = 'Name:', required=False)
    url_desc = forms.CharField(label = 'Description (max 500 chars):',
                               widget = forms.Textarea(attrs={'cols': '35', 
                                                              'rows':'7'}),
                               required = False)
    privacy_mode = forms.BooleanField(label="Private?", required=False,
                                      widget=forms.CheckboxInput)
    
    class Meta:
        model = Url
        exclude = ('user', 'date_created', 'source', 'last_updated')
        fields = ('url', 'url_name', 'url_desc',  'tags', 'privacy_mode')

    def __init__(self, data=None, user=None, *args, **kwargs):
        super(UrlFormRemote, self).__init__(data, *args, **kwargs)
        self.user = user
            
    def clean_url(self):
        url = self.cleaned_data['url']
        if self.user.url_set.filter(url=url).count():
            raise forms.ValidationError("This URL already exists for %s" %
                                        self.user)
        else:
            return url
    
    def clean_tags(self):
        tags = self.cleaned_data['tags']
        for tag in tags:
            tags[tags.index(tag)] = tag.lower()
        return tags
