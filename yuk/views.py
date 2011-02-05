from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django import forms
from yuk.models import Url, UrlForm
from tagging.models import Tag, TaggedItem
from registration.forms import RegistrationFormUniqueEmail
import sys

def new_url(request, uname):
    form = UrlForm()
    if request.method == 'POST':
        form = UrlForm(request.POST)
        if form.errors:
            print >> sys.stderr, form.errors
            return render_to_response('stored.html', {'form':form}, context_instance=RequestContext(request))            
        else:
            form.save()
            return redirect('/u:%s' % uname)

    return render_to_response('new_url.html', {'form':form}, context_instance=RequestContext(request))

def tag_detail(request, uname, tag):
    tag_tag = [tag for tag in Tag.objects.usage_for_model(Url, filters=dict(user=request.session['_auth_user_id']))]
    return render_to_response('tag.html', {'urls':TaggedItem.objects.get_by_model(Url, tag_tag), 'tag':tag}, context_instance=RequestContext(request))

def redir_to_profile(request, uname=None):
    user = get_current_user(request)
    return redirect('/u:%s' % user.username)

def profile(request, uname):
    urls = Url.objects.filter(user=request.session['_auth_user_id'])
    current_user = get_current_user(request)
    return render_to_response('index.html', {'urls':urls, 'user':current_user.username})

def do_login(request):
    try:
        current_user = get_current_user(request)
        return redirect('/u:%s' % current_user.username)
    except KeyError:
        return redirect('/accounts/login')

def do_logout(request):
    logout(request)

def get_current_user(request):
    return User.objects.get(id=request.session['_auth_user_id'])

def current_user_urls(request):
    current_user = get_current_user(request)
    return [url for url in Url.objects.all() if url.user==current_user.username]

    
        
    
        
        

