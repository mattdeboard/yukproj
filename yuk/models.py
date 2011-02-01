from django.db import models
from django.forms import ModelForm
from django import forms
from tagging.forms import TagField
from urlparse import urlparse, urlunparse
import sys

class MyUrlField(forms.URLField):

        def to_python(self, value):
                '''Lowercase the URL input for validation.'''
                if value.startswith('http://'):
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
                

class Url(models.Model):

	def __unicode__(self):
		return self.url

	url = models.URLField(verify_exists=True, unique=True)
	url_name = models.CharField(max_length=200)
	tagstring = models.CharField(max_length=200)
	url_desc = models.TextField()
        
class UrlForm(ModelForm):
        url = MyUrlField(label='URL:')
	url_name = forms.CharField(label='Name:')
	tagstring = forms.CharField(label='tags separated by commas:')
	url_desc = forms.CharField(label='Description (max 500 chars):', widget=forms.Textarea)
        class Meta:
                model = Url

