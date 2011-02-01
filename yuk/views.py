from django.shortcuts import render_to_response
from django.template import RequestContext
from django import forms
from yuk.models import Url, UrlForm
from tagging.models import Tag
from django.db import IntegrityError
import sys

def new_url(request):
    form = UrlForm()
    if request.method == 'POST':
        form = UrlForm(request.POST)
        if form.errors:
            print >> sys.stderr, form.errors
            return render_to_response('stored.html', {'form':form}, context_instance=RequestContext(request))            
        else:
            form.save()
            return render_to_response('stored.html', {'form':form, 'urls':Url.objects.all()}, context_instance=RequestContext(request))

    return render_to_response('new_url.html', {'form':form}, context_instance=RequestContext(request))

def index(request):
    for url in Url.objects.all():
        f = Url.objects.get(url=url.url)
        Tag.objects.update_tags(f, url.tagstring)
        tags = Tag.objects.get_for_object(url)
        url.tagstring = ','.join([tag.name for tag in tags])
        url.save()
    return render_to_response('index.html', {'urls':Url.objects.all(), 'tags':tags})

##def tag_detail(request, tag):
##    return render_to_response('tag.html', {
