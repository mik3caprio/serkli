from django.shortcuts import render

from django.http import HttpResponse
from django_twilio.decorators import twilio_view

from twilio.twiml import Response


def index(request):
    return HttpResponse("Hello, world. You're at the circle index.")

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."

    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

@twilio_view
def sms(request):
    name = request.POST.get('Body', '')

    msg = 'Hey %s, how are you today?' % (name)
    r = Response()
    r.message(msg)

    return r

@twilio_view
def ring(request):
    r = Response()
    r.play('http://bit.ly/phaltsw')

    return r
