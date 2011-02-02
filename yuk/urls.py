from django.conf.urls.defaults import *
from tagging import *


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^yuk/$', include('yuk.views.index')),
    (r'^yuk/new_url/', include('yuk.views.new_url')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
##    url(r'^yuk/tag/(?P<tag>[^/]+)/$',
##        tagged_object_list,
##        dict(model=Url, paginate_by=10, allow_empty=True,
##             template_object_name='url'),
##        name='url_tag_detail'),
)
