from django.shortcuts import render_to_response
from django.template import RequestContext
from django import forms
from yuk.models import Url, UrlForm
from tagging.models import Tag
import sys

def new_url(request):
    form = UrlForm()
    if request.method == 'POST':
        form = UrlForm(request.POST)
        if form.errors:
            return render_to_response('new_url.html', {'form':form}, context_instance=RequestContext(request))            
        else:
            form.save()
            f = Url.objects.get(url=form['url'].data)
            Tag.objects.update_tags(f, form['tagstring'].data)
            return render_to_response('stored.html', {'form':form}, context_instance=RequestContext(request))

    return render_to_response('new_url.html', {'form':form}, context_instance=RequestContext(request))

def index(request):
    for url in Url.objects.all():
        tags = Tag.objects.get_for_object(url)
        url.tagstring = [tag.name for tag in tags]
    return render_to_response('index.html', {'urls':Url.objects.all()})
