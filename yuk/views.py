import datetime
import sys

from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.contrib.sites.models import get_current_site
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.signals import request_finished
from django.shortcuts import (render_to_response, redirect, get_object_or_404,
                              get_list_or_404)
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages

from haystack.query import SearchQuerySet

from yuk.models import Item
from yuk.forms import *
from yuk.rss_module import rssdownload
from yuk.scripts import import_text_file


def landing(request):
    if request.user.is_authenticated():
        return redirect("yuk.views.profile", uname=request.user)
    return render_to_response("landing.html", 
                              context_instance=RequestContext(request))

@csrf_protect
@never_cache
def login(request, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm):
    """Displays the login form and handles the login action."""

    if request.user.is_authenticated():
        return redirect("yuk.views.profile", uname=request.user)

    redirect_to = request.REQUEST.get(redirect_field_name, '')

    if request.method == "POST":
        form = authentication_form(data=request.POST)
        if form.is_valid():
            # Light security check -- make sure redirect_to isn't garbage.
            if not redirect_to or ' ' in redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Heavier security check -- redirects to http://example.com should
            # not be allowed, but things like /view/?param=http://example.com
            # should be allowed. This regex checks if there is a '//' *before* a
            # question mark.
            elif '//' in redirect_to and re.match(r'[^\?]*//', redirect_to):
                    redirect_to = settings.LOGIN_REDIRECT_URL

            # Okay, security checks complete. Log the user in.
            auth_login(request, form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            return HttpResponseRedirect(redirect_to)
    
        if form.non_field_errors():
            messages.error(request, 
                           "Invalid user/pass combo. Is your caps lock on?", 
                           extra_tags="bad_login")
        if 'password' in form.errors.keys():
            messages.error(request, 
                           "Please enter your password.",
                           extra_tags="bad_password")



    else:
        form = authentication_form(request)

    request.session.set_test_cookie()

    current_site = get_current_site(request)

    return render_to_response(template_name, {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }, context_instance=RequestContext(request))

@login_required
def search_results(request, results=None):
    sqs = SearchQuerySet()
    if request.method=="POST":
        results = sqs.auto_query(request.POST.get('q')).filter_and(author=request.user)
    return render_to_response("search/search.html", 
                              {"results": results},
                              context_instance=RequestContext(request))

@login_required
def new_url(request):
    form = UrlForm()
    item_type = "bookmark"
    if request.method == 'POST':
        form = UrlForm(request.POST, request.user)
        if form.is_valid():
            g = form.save(commit=False)
            g.user = request.user
            g.item_type = item_type
            g.save()
            form.save_m2m()
            messages.success(request, "Your bookmark was saved!")
            return redirect('yuk.views.profile', uname=request.user)
                        
    return render_to_response('new_item.html', {'form':form},
                              context_instance=RequestContext(request))

@login_required
def new_quote(request):
    form = QuoteForm()
    item_type = "quote"
    if request.method == 'POST':
        form = QuoteForm(request.POST, request.user)
        if form.is_valid():
            g = form.save(commit=False)
            g.user = request.user
            g.item_type = item_type
            g.save()
            if g.tags:
                form.save_m2m()
            messages.success(request, "Your quote was saved!")
            return redirect('yuk.views.profile', uname=request.user)
            
    return render_to_response('new_item.html', {'form':form},
                              context_instance=RequestContext(request))

@login_required
def new_note(request):
    form = NoteForm()
    item_type = "note"
    if request.method == 'POST':
        form = NoteForm(request.POST, request.user)
        if form.is_valid():
            g = form.save(commit=False)
            g.user = request.user
            g.item_type = item_type
            g.save()
            form.save_m2m()
            messages.success(request, "Your note was saved!")
            return redirect('yuk.views.profile', uname=request.user)
    return render_to_response('new_item.html', {'form':form},
                              context_instance=RequestContext(request))
            

def remote_new_url(request):
    if not request.user.is_authenticated():
        return redirect('/bm_login/?next=%s' % request.get_full_path())

    init_data = {'url': request.GET.get('url', ' '), 
                 'description': request.GET.get('description', ' '),
                 'displays': request.GET.get('title', ' ')}
    form = UrlForm(init_data)
    
    if request.method == 'POST':
        form = UrlForm(request.POST, request.user)
        if form.is_valid():
            g = form.save(commit=False)
            g.user = request.user
            g.date_created = datetime.datetime.now()
            g.item_type = "bookmark"
            g.save()
            if g.tags:
                form.save_m2m()
            return HttpResponse('''
                                <script type="text/javascript">
                                window.close();
                                </script>''')
    
    return render_to_response('bookmarklet_add.html',
                              {'form': form},
                              context_instance=RequestContext(request))


def bm_login(request):
    form = AuthenticationForm()
    redirect_to = "/add_bookmark_remote?&url=%s&description=%s&title=%s" % (
        request.GET.get('url'), 
        request.GET.get('description'), 
        request.GET.get('title'),
    )

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            print >> sys.stderr, "1"
            auth_login(request, form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            return redirect(redirect_to)
        else:
            return render_to_response('bm_login.html',
                                      {'form': form},
                                      context_instance=RequestContext(request))
    else:
        form = AuthenticationForm(request)

    request.session.set_test_cookie()
    return render_to_response('bm_login.html', 
                              {'form': form, 'redir': redirect_to},
                              context_instance=RequestContext(request))

def tag_detail(request, uname, tag):
    tag = tag.replace('-',' ')
    results = get_list_or_404(Item, user=User.objects.get(username=uname),
                              tags__name__in=[tag])
    return render_to_response('tag.html',
                              {'results':results,
                               'tag':tag,
                               'uname':uname}, 
                              context_instance=RequestContext(request))

@login_required
def edit_item(request, uname, item_id):
    item = get_object_or_404(Item, id=item_id, user=request.user)

    if item.item_type == "quote":
        itemform = QuoteForm
    elif item.item_type == "note":
        itemform = NoteForm
    else:
        itemform = UrlEditForm

    form = itemform(instance=item)

    if request.method=='POST':
        form = itemform(request.POST, request.user)
        attrs = ['displays', 'description', 'privacy_mode']
        if form.is_valid():
            for attr in attrs:
                setattr(item, attr, form.cleaned_data[attr])
            update_tags(item, form)
            item.save()
            return redirect('yuk.views.profile', uname=request.user.username)
        
    return render_to_response('edit_url.html',
                              {'form':form},
                              context_instance=RequestContext(request))


@login_required
def redir_to_profile(request, uname=None):
    return HttpResponseRedirect(request.user.get_absolute_url())

def profile(request, uname):
    if request.user.is_authenticated() and uname == request.user.username:
        results = Item.objects.filter(user=request.user)
    else:
        results = get_list_or_404(Item, user=User.objects.get(username=uname),
                                  privacy_mode=False)

    return render_to_response('user_profile.html', {'results':results, 
                                                    'uname':uname},
                              context_instance=RequestContext(request))

@login_required
def del_item(request, uname, item_id):
    if request.method=='POST':
        item = Item.objects.get(id=request.POST['item_id'])
        item.delete()
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
                        user=request.user, url_name=i['url_name'])
                u.save()
            return redirect('yuk.views.profile', uname=request.user)
    return render_to_response('rss_import.html', {'form':form},
                              context_instance=RequestContext(request))

def update_tags(item, form):
    itemset = set(item.tags.all())
    tagstringset = set(form.cleaned_data['tags'])
    for tag in itemset.difference(tagstringset):
        item.tags.remove(tag)
    for tag in tagstringset.difference(itemset):
        item.tags.add(tag)
    return item

@login_required
def export(request):
    return render_to_response("export.html", 
                              {"items":Item.objects.filter(user=request.user)}, 
                              mimetype="text/plain")

@login_required    
def import_text(request):
    form = BookmarkUploadForm()
    if request.method == 'POST':
        form = BookmarkUploadForm(request.POST, request.FILES)
        if form.is_valid():
            import_text_file(request)
            messages.success(request, "Your bookmarks have been imported"
                             " successfully!")
            return redirect("yuk.views.profile", uname=request.user)
        else:
            messages.error(request, "Your upload failed. Please retry.")
    return render_to_response("bookmark_import.html", {"form":form}, 
                              context_instance=RequestContext(request))
        

            
    
        
        

