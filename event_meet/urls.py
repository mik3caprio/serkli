from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = [url(r'', include('circly.urls', namespace="connect")),
               url(r'^admin/', include(admin.site.urls)),
]
