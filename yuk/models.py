from django.db import models
from django.forms import ModelForm
from django import forms

class Url(models.Model):

	def __unicode__(self):
		return self.url

	url = models.URLField(verify_exists=True, unique=True)
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

