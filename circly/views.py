import datetime
from django.shortcuts import get_object_or_404, render

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django_twilio.decorators import twilio_view
from django.utils import timezone
from django.core.urlresolvers import reverse

from twilio.twiml import Response


def index(request):
    context = {}

    return render(request, 'circly/index.html', context)


def submitname(request):
    from .models import Circle, Member

    first_name = request.POST.get('cm-name', "")

    if (first_name != ""):
        # Create a circle
        new_circle = Circle(circle_name=first_name + "'s circle",
                            circle_created_date=timezone.now(),)
        new_circle.save()

        # Create our new member
        new_member = Member(circle=new_circle,
                            circle_owner=True,
                            member_name=first_name,
                            member_created_date=timezone.now(),)
        new_member.save()

        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('connect:flow', args=(new_circle, new_member,)))
    else:
        # Redisplay the name submission form
        return render(request, 'circly/index.html', {
            'error_message': "You didn't enter a name.",})


def flow(request, a_circle, a_member):
    from .models import Circle, Member

#    p = get_object_or_404(Question, pk=question_id)

    context = {}
    return render(request, 'circly/flow.html', context)


def network(request):
    from .models import Circle, Member

    # Create reminders to join the circle for all members except circle owner

#    m2 = Member.objects.get(member_name='Madelena Mak')

#    r2 = Reminder(member=m2,
#                 reminder_subject="Reminder! Tell Kennedy to self-examine their breast",
#                 reminder_message="Hey Mike, please tell Kennedy to do a breast self-exam! Go to the page at http://j.mp/SelfChec01 to get some ideas for what to talk about.",
#                 reminder_created_date=timezone.now(),
#                 reminder_send_date=timezone.now() + datetime.timedelta(seconds=20),
#                )

#    r2.save()

    context = {}
    return render(request, 'circly/network.html', context)


def dashboard(request):
    from .models import Circle, Member

    # Display all members of the circle with name and contact info

    template = loader.get_template('circly/dashboard.html')
    context = RequestContext(request, {
#        'latest_question_list': latest_question_list,
    })

    return HttpResponse(template.render(context))


def checkmeout(request):
    context = {}

    return render(request, 'circly/checkmeout.html', context)
