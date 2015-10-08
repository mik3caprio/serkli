from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^submitname/$', views.submitname, name='submitname'),
    url(r'^flow/$', views.flow, name='flow'),
    url(r'^invite/(?P<invite_hash>[0-9a-fA-F]+:[0-9a-fA-F]+)$', views.invite, name='invite'),
    url(r'^submitprofile/$', views.submitprofile, name='submitprofile'),
    url(r'^network/$', views.network, name='network'),
    url(r'^submitcircle/$', views.submitcircle, name='submitcircle'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^thankyou/$', views.thankyou, name='thankyou'),
    url(r'^checkmeout/$', views.checkmeout, name='checkmeout'),
]
