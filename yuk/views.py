from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from yuk.models import Url, UrlForm, UrlEditForm, RssImportForm
from yuk.rss_module import rssdownload

import datetime


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
                return render_to_response('new_url.html', {'form':form},
                                          context_instance=RequestContext(request))            

        return render_to_response('new_url.html',
                                  {'form':form, 'user':request.user},
                                  context_instance=RequestContext(request))
    else:
        return redirect(login)

@login_required
def tag_detail(request, uname, tag):
    tag = tag.replace('-',' ')
    return render_to_response('tag.html',
                              {'urls':Url.objects.filter(tags__name__in=[tag]),
                               'tag':tag, 'uname':uname},
                              context_instance=RequestContext(request))

@login_required
def edit_url(request, uname, url_id):
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
            update_tags(url, form)
            url.save()
            return redirect('yuk.views.profile', uname=request.user.username)
        
    return render_to_response('edit_url.html',
                              {'form':form, 'user':request.user},
                              context_instance=RequestContext(request))

@login_required
def redir_to_profile(request, uname=None):
    return HttpResponseRedirect(request.user.get_absolute_url())

@login_required
def profile(request, uname):
    if request.user.is_authenticated:
        #Returns all URLs input via UI only. This is to later sort imported URLs
        #from manually entered ones.
        urls = Url.objects.filter(user=request.user, source='UI')
        if uname != request.user.username:
            return redirect('yuk.views.redir_to_profile')
        return render_to_response('user_profile.html',
                                  {'urls':urls, 'user':request.user.username})
    else:
        return redirect(login)

@login_required
def del_url(request, uname, url_id):
    if request.method=='POST':
        url = Url.objects.get(id=request.POST['url_id'])
        url.delete()
        return HttpResponse("Deleted.")
    else:
        return redirect('yuk.views.profile', uname=request.user)
    
@login_required
def rss_import(request, uname):
    form = RssImportForm()
    if request.method == 'POST':
        form = RssImportForm(request.POST, request.user)
        if form.is_valid():
            feed = form.save(commit=False)
            feed.user = request.user
            feed.save()
            urls = rssdownload(request.user, feed.url)
            for i in urls['messages']:
                u = Url(url=i['url'], date_created=i['timestamp'],
                        user=request.user, url_name=i['url_name'],
                        source='RSS - %s' % feed.url)
                u.save()
            return redirect('yuk.views.profile', uname=request.user)
    return render_to_response('rss_import.html', {'form':form},
                              context_instance=RequestContext(request))

    

def update_tags(url, form):
    urlset = set(url.tags.all())
    tagstringset = set(form.cleaned_data['tags'])
    for tag in urlset.difference(tagstringset):
        url.tags.remove(tag)
    for tag in tagstringset.difference(urlset):
        url.tags.add(tag)
    return url


    
    
    
        
        

