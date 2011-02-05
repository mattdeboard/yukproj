from django.conf.urls.defaults import *
from tagging import *


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^$', 'yuk.views.do_login'),
    (r'^users/(?P<uname>\w+)/$', 'yuk.views.redir_to_profile'),
    (r'^accounts/', include('registration.backends.simple.urls')),
    (r'^accounts/profile/$', 'yuk.views.redir_to_profile'),
    (r'^u:(?P<uname>\w+)/new_url/$', 'yuk.views.new_url'),
    (r'^u:(?P<uname>\w+)/$', 'yuk.views.profile'),
    (r'^u:(?P<uname>\w+)/t:(?P<tag>\w+)/$', 'yuk.views.tag_detail'),
##    url(r'^yuk/tag/(?P<tag>[^/]+)/$',
##        tagged_object_list,
##        dict(model=Url, paginate_by=10, allow_empty=True,
##             template_object_name='url'),
##        name='url_tag_detail'),
)
