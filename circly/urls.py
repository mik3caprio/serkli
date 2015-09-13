from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.index, name='index'),
    # ex: /polls/5/
#    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
#    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
#    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),

    # Add our Twilio URLs
    url(r'^flow/$', views.flow, name='flow'),
    url(r'^checkmeout/$', views.checkmeout, name='checkmeout'),
    url(r'^sms/$', views.sms, name='sms'),
    url(r'^ring/$', views.ring, name='ring'),
    url(r'^email/$', views.email, name='email'),
]
