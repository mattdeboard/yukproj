import os
import sys

from django.contrib import admin
from django.conf.urls.defaults import *

from yukproj import localsettings

admin.autodiscover()

urlpatterns = patterns('',
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', 
     {'sitemaps': sitemaps})
    (r'^search/', 'yuk.views.search_results'),
    (r'^add_bookmark_remote/$', 'yuk.views.remote_new_url'),
    (r'^add_bookmark/$', 'yuk.views.new_url'),
    (r'^add_note/$', 'yuk.views.new_note'),
    (r'^add_quote/$', 'yuk.views.new_quote'),
    (r'^$', 'yuk.views.landing'),
    (r'^users/(?P<uname>\w+)/$', 'yuk.views.redir_to_profile'),
    (r'^bm_login/$', 'yuk.views.bm_login'),
    (r'^export/$', 'yuk.views.export'),
    (r'^login/$', 'yuk.views.login'),
    (r'^accounts/', include('registration.backends.simple.urls')),
    (r'^logout/$', 'django.contrib.auth.views.logout_then_login', 
     {'login_url':'/'}),
    (r'^accounts/profile/$', 'yuk.views.redir_to_profile'),
    (r'^import/$', 'yuk.views.import_text'),
    (r'^u:(?P<uname>\w+)/delete/$', 'yuk.views.del_item', {'item_id':None}),
    (r'^u:(?P<uname>\w+)/e:(?P<item_id>\d+)/$', 'yuk.views.edit_item'),
    (r'^u:(?P<uname>\w+)/$', 'yuk.views.profile'),
    (r'^u:(?P<uname>\w+)/t:(?P<tag>[\w-]+)/$', 'yuk.views.tag_detail'),
    (r'^u:(?P<uname>\w+)/import_rss/$', 'yuk.views.rss_import'),
)


if os.environ['DJANGO_SETTINGS_MODULE']:
    urlpatterns += patterns('',
                            (r"^site_media/(?P<path>.*)/$", 
                             'django.views.static.serve', 
                             {'document_root': localsettings.STATIC_DOC_ROOT})
)
                
