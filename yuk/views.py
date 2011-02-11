from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import login
from django.core.exceptions import ObjectDoesNotExist
from registration.forms import RegistrationFormUniqueEmail
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django import forms
from yuk.models import Url, UrlForm, UrlEditForm

import sys, datetime


@login_required
def new_url(request, uname):
    if request.user.is_authenticated:
        if uname != request.user.username:
            return redirect('yuk.views.redir_to_profile')
        form = UrlForm()
        if request.method == 'POST':
            form = UrlForm(request.POST, request.user)
            if form.is_valid():
                g = form.save(commit=False)
                g.user = request.user
                g.date_created = datetime.datetime.now()
                g.save()
                form.save_m2m()
                return redirect('yuk.views.profile', uname=request.user)
            else:
                return render_to_response('new_url.html', {'form':form}, context_instance=RequestContext(request))            

        return render_to_response('new_url.html', {'form':form, 'user':request.user}, context_instance=RequestContext(request))
    else:
        return redirect(login)

@login_required
def tag_detail(request, uname, tag):
    tag = tag.replace('-',' ')
    return render_to_response('tag.html', {'urls':Url.objects.filter(tags__name__in=[tag]), 'tag':tag, 'uname':uname}, context_instance=RequestContext(request))

@login_required
def edit_url(request, uname, url_id):
##  Generalize edit URL by something like:
##    urls.py: (r'^u:(?P<uname>\w+)/edit/$', 'yuk.views.edit_url', {'uname':None, 'url_id':None})
##    yuk.views.edit_url:
    try:
        url = Url.objects.get(id=url_id, user=request.user)
    except ObjectDoesNotExist:
        return render_to_response('401.html', {'user':request.user})
    form = UrlEditForm(instance=url)
    if request.method=='POST':
        form = UrlEditForm(request.POST, request.user)
        attrs = ['url', 'url_name', 'url_desc']
        if form.is_valid():
            for attr in attrs:
                setattr(url, attr, form.cleaned_data[attr])
            print >> sys.stderr, form.cleaned_data['tags'], url.tags.all()
            update_tags(url, form)
            url.save()
            return redirect('yuk.views.profile', uname=request.user.username)
        
    return render_to_response('edit_url.html', {'form':form, 'user':request.user}, context_instance=RequestContext(request))

@login_required
def redir_to_profile(request, uname=None):
    return HttpResponseRedirect(request.user.get_absolute_url())

@login_required
def profile(request, uname):
    if request.user.is_authenticated:
        urls = Url.objects.filter(user=request.user)
        if uname != request.user.username:
            return redirect('yuk.views.redir_to_profile')
        return render_to_response('user_profile.html', {'urls':urls, 'user':request.user.username})
    else:
        return redirect(login)

@login_required
def del_url(request, uname, url_id):
    print >> sys.stderr, request.method, request.POST.copy()['url_id']
    if request.method=='POST':
        url = Url.objects.get(id=request.POST['url_id'])
        url.delete()
        return HttpResponse("Deleted.")
    else:
        return redirect('yuk.views.profile', uname=request.user)
    

def update_tags(url, form):
    urlset = set(url.tags.all())
    tagstringset = set(form.cleaned_data['tags'])
    print >> sys.stderr, urlset.difference(tagstringset)
    for tag in urlset.difference(tagstringset):
        url.tags.remove(tag)
    for tag in tagstringset.difference(urlset):
        url.tags.add(tag)
    return url
    
    
    
        
        

