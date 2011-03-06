from django.conf.urls.defaults import *
from yukproj import settings

from django.contrib import admin
admin.autodiscover()

sdr = settings.STATIC_DOC_ROOT

urlpatterns = patterns('',
    (r'^site_media/(?P<path>.*)/$', 'django.views.static.serve',
        {'document_root': sdr}),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^new_url', 'yuk.views.remote_new_url'),
    (r'^$', 'yuk.views.redir_to_profile'),
    (r'^users/(?P<uname>\w+)/$', 'yuk.views.redir_to_profile'),
    (r'^bm_login/$', 'yuk.views.bm_login'),
    (r'^export/$', 'yuk.views.export'),
    (r'^accounts/', include('registration.backends.simple.urls')),
    (r'^accounts/profile/$', 'yuk.views.redir_to_profile'),
    (r'^u:(?P<uname>\w+)/new_url/$', 'yuk.views.new_url'),
    (r'^import/$', 'yuk.views.import_text'),
    (r'^u:(?P<uname>\w+)/delete/$', 'yuk.views.del_url', {'url_id':None}),
    (r'^u:(?P<uname>\w+)/$', 'yuk.views.profile'),
    (r'^u:(?P<uname>\w+)/t:(?P<tag>[\w-]+)/$', 'yuk.views.tag_detail'),
    (r'^u:(?P<uname>\w+)/e:(?P<url_id>\d+)/$', 'yuk.views.edit_url'),
    (r'^u:(?P<uname>\w+)/import_rss/$', 'yuk.views.rss_import'),
)
