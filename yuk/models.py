from django.db import models
from django.forms import ModelForm
from django import forms
from tagging.forms import TagField
import sys

class MyUrlField(forms.URLField):
        # convert this-part.com to lowercase, but not xyz.com/ThisPart
        def to_python(self, value):
                '''Lowercase the URL input for validation.'''
                return value.lower()

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

