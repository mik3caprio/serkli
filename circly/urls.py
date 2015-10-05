from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^submitname/$', views.submitname, name='submitname'),
    url(r'^flow/$', views.flow, name='flow'),
    url(r'^invite/$', views.invite, name='invite'),
    url(r'^submitinvite/$', views.submitinvite, name='submitinvite'),
    url(r'^submitprofile/$', views.submitprofile, name='submitprofile'),
    url(r'^network/$', views.network, name='network'),
    url(r'^submitcircle/$', views.submitcircle, name='submitcircle'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^checkmeout/$', views.checkmeout, name='checkmeout'),

#    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
#    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
#    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
