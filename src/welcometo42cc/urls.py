import os.path as op

from django.conf import settings
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^welcometo42cc/', include('welcometo42cc.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     (r'^admin/', include(admin.site.urls)),
)

# static urls will be disabled in production mode,
if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
        url(r'^admin-media/(.*)$', 'django.views.static.serve', {'document_root': op.join(op.dirname(admin.__file__), 'media')}),
        )
