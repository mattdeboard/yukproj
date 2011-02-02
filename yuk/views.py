from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django import forms
from yuk.models import Url, UrlForm
from tagging.models import Tag, TaggedItem
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
            return redirect('/yuk')

    return render_to_response('new_url.html', {'form':form}, context_instance=RequestContext(request))

def index(request):
    return render_to_response('index.html', {'urls':Url.objects.order_by('-id')})


##def tag_detail(request, tag):
##    return render_to_response('tag.html', {


