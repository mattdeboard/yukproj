from django.conf.urls.defaults import *
from tagging import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^yuk/$', 'yuk.views.index'),
    (r'^yuk/new_url/', 'yuk.views.new_url'),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
##    url(r'^yuk/tag/(?P<tag>[^/]+)/$',
##        tagged_object_list,
##        dict(model=Url, paginate_by=10, allow_empty=True,
##             template_object_name='url'),
##        name='url_tag_detail'),
)
