from django.shortcuts import render

from django.http import HttpResponse
from django_twilio.decorators import twilio_view

from twilio.twiml import Response


def index(request):
    return HttpResponse("Hello, world. You're at the circle index.")

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

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
