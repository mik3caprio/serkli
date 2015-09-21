from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^submitname/$', views.submitname, name='submitname'),
    url(r'^flow/(?P<member>[0-9]+)', views.flow, name='flow'),
    url(r'^submitprofile/$', views.submitprofile, name='submitprofile'),
    url(r'^network/(?P<member>[0-9]+)$', views.network, name='network'),
    url(r'^submitcircle/$', views.submitcircle, name='submitcircle'),
    url(r'^dashboard/(?P<member>[0-9]+)$', views.dashboard, name='dashboard'),
    url(r'^checkmeout/$', views.checkmeout, name='checkmeout'),
]
