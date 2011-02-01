from django.db import models
from django.forms import ModelForm
from django import forms
from tagging.forms import TagField
import sys

class MyUrlField(models.URLField):
        # convert this-part.com to lowercase, but not xyz.com/ThisPart
        def post_init(self, model_instance):
                super(MyUrlField, self).post_init(model_instance)
                value = getattr(model_instance, self.attname)
                '''Lowercase the URL input for validation.'''
                return value.lower()

class Url(models.Model):

	def __unicode__(self):
		return self.url

	url = MyUrlField(verify_exists=True, unique=True)
	url_name = models.CharField(max_length=200)
	tagstring = models.CharField(max_length=200)
	url_desc = models.TextField()
        
class UrlForm(ModelForm):
        url = forms.URLField(label='URL:')
	url_name = forms.CharField(label='Name:')
	tagstring = forms.CharField(label='tags separated by commas:')
	url_desc = forms.CharField(label='Description (max 500 chars):', widget=forms.Textarea)
        class Meta:
                model = Url

