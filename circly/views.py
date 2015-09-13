from django.shortcuts import render

from django.http import HttpResponse
from django.template import RequestContext, loader
from django_twilio.decorators import twilio_view

from twilio.twiml import Response


def index(request):
    # Pull any data we need from DB
#    latest_question_list = Question.objects.order_by('-pub_date')[:5]

    template = loader.get_template('circly/index.html')
    context = RequestContext(request, {
#        'latest_question_list': latest_question_list,
    })

    return HttpResponse(template.render(context))

def checkmeout(request):
    template = loader.get_template('circly/checkmeout.html')
    context = RequestContext(request, {
#        'latest_question_list': latest_question_list,
    })

    return HttpResponse(template.render(context))

def flow(request):
    template = loader.get_template('circly/flow.html')
    context = RequestContext(request, {
#        'latest_question_list': latest_question_list,
    })

    return HttpResponse(template.render(context))

def email(request):
    from django.core.mail import send_mail

    send_mail('Reminder! Tell Kennedy to self-examine his breast', 'Hey Madelena, please send Kennedy a reminder to do a breast self-exam! Go to the page at http://j.mp/SelfChec to get some ideas for what to talk about.', 'from@example.com', ['madelena.mak@gmail.com'], fail_silently=False)

    return HttpResponse("Email sent.")

@twilio_view
def sms(request):
#    name = request.POST.get('Body', '')

    msg = 'Hey Mike, please send Kennedy a reminder to do a breast self-exam! Go to the page at http://j.mp/SelfChec to get some ideas for what to talk about.'
    r = Response()
    r.message(msg)

    return r

@twilio_view
def ring(request):
    r = Response()
    r.play('http://bit.ly/phaltsw')

    return r
