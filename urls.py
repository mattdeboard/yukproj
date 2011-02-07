from django.conf.urls.defaults import *
from yukproj import settings
from tagging import *


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/a/mattdeboard.net/yukproj/yuk/static'}),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^$', 'yuk.views.do_login'),
    (r'^users/(?P<uname>\w+)/$', 'yuk.views.redir_to_profile'),
    (r'^accounts/', include('registration.backends.simple.urls')),
    (r'^accounts/profile/$', 'yuk.views.redir_to_profile'),
    (r'^u:(?P<uname>\w+)/new_url/$', 'yuk.views.new_url'),
    (r'^u:(?P<uname>\w+)/$', 'yuk.views.profile'),
    (r'^u:(?P<uname>\w+)/t:(?P<tag>\w+)/$', 'yuk.views.tag_detail'),
    (r'^u:(?P<uname>\w+)/e:(?P<url_id>\d+)/$', 'yuk.views.edit_url'),
)
