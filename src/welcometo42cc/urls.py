import os.path as op

from django.conf import settings
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
     url(r'^$', 'common.views.homepage'),
     url(r'^form/$', 'common.views.userform', name="userform"),
     url(r'^form/ajax/$', 'common.views.userform_ajax', name="userform_ajax"),
     url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name="login"),
     url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': settings.LOGIN_URL}, name="logout"),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     (r'^admin/', include(admin.site.urls)),
)

# static urls will be disabled in production mode
urlpatterns += patterns(
    '',
    url(r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^admin-media/(.*)$', 'django.views.static.serve', {'document_root': op.join(op.dirname(admin.__file__), 'media')}),
)
