import datetime
from django.shortcuts import get_object_or_404, render

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django_twilio.decorators import twilio_view
from django.utils import timezone
from django.core.urlresolvers import reverse

from twilio.twiml import Response


CIRCLE_SIZE = 8


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
        return HttpResponseRedirect(reverse('connect:flow', 
                                            kwargs={'member':new_member.id}))
    else:
        # Redisplay the name submission form
        return render(request, 
                      'circly/index.html', 
                      {'error_message': "You didn't enter a name.",})


def flow(request, member):
    from .models import Circle, Member

    new_member = get_object_or_404(Member, pk=member)

    context = {'member':new_member}
    return render(request, 'circly/flow.html', context)


def submitprofile(request, member):
    from .models import Circle, Member

    new_member = get_object_or_404(Member, pk=member)

    chromosome = request.POST.get('cm-chromosome', "")
    age = request.POST.get('cm-age', "")
    ethnicity = request.POST.get('cm-ethnicity', "")
    drink = request.POST.get('cm-drink', "")
    smoke = request.POST.get('cm-smoke', "")
    exercise = request.POST.get('cm-exercise', "")
    bmi = request.POST.get('cm-bmi', "")
    relatives = int(request.POST.get('cm-relatives', 0))

    new_member.age_range = age
    new_member.sex_range = chromosome
    new_member.ethnicity_range = ethnicity
    new_member.bmi_range = bmi
    new_member.cancer_family = relatives

    if (drink == "yes"):
        new_member.drinker = True
    else:
        new_member.drinker = False

    if (smoke == "yes"):
        new_member.smoker = True
    else:
        new_member.smoker = False

    if (exercise == "yes"):
        new_member.exercises = True
    else:
        new_member.exercises = False

    new_member.member_profile_entered_date = timezone.now()

    new_member.save()

    return HttpResponseRedirect(reverse('connect:network', 
                                        kwargs={'member':new_member.id}))


def network(request, member):
    from .models import Circle, Member

    count = CIRCLE_SIZE
    contact_range_str = ""

    while count != 1:
        contact_range_str = contact_range_str + str(count)
        count = count - 1

    # Reverse the string of numbers
    contact_range_str = contact_range_str[::-1]

    context = {'num_range_str':contact_range_str}
    return render(request, 'circly/network.html', context)


def submitcircle(request, member):
    from .models import Circle, Member, Reminder

    new_member = get_object_or_404(Member, pk=member)
    new_circle = get_object_or_404(Circle, pk=new_member.circle.id)

    count = 2
    posted_members = {}

    while count <= CONTACT_RANGE:
        member_contact = {}

        current_name = request.POST.get('cm-name_' + count, "")
        current_contact = request.POST.get('cm-contact_' + count, "")

        if (current_name != ""):
            if (current_contact != ""):
                # Check to see if current contact info is valid phone or email
                if (is_phone(current_contact)):
                    member_contact["contact_type"] = "phone"
                elif (is_email(current_contact)):
                    member_contact["contact_type"] = "email"

                member_contact["contact_info"] = current_contact

                posted_members[current_name] = member_contact

    for each_member in posted_members.keys():
        # Create new members and add to the circle
        if (posted_members[each_member]["contact_type"] == "email"):
            next_member = Member(circle=new_circle,
                                 circle_owner=False,
                                 member_name=each_member,
                                 member_email=posted_members[each_member]["contact_info"],
                                 member_created_date=timezone.now(),)
        elif (posted_members[each_member]["contact_type"] == "phone"):
            next_member = Member(circle=new_circle,
                                 circle_owner=False,
                                 member_name=each_member,
                                 member_phone=posted_members[each_member]["contact_info"],
                                 member_created_date=timezone.now(),)

        next_member.save()

        # Create reminders for all new members to join the circle
        remind = Reminder(member=next_member,
                          reminder_subject=" would like you to join their circle of support",
                          reminder_message="Hey Mike, please tell Kennedy to do a breast self-exam! Go to the page at http://j.mp/SelfChec01 to get some ideas for what to talk about.",
                          reminder_created_date=timezone.now(),
                          reminder_send_date=timezone.now(), )
        remind.save()

    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('connect:dashboard', 
                                        kwargs={'member':new_member.id}))


def dashboard(request, member):
    from .models import Circle, Member

    new_member = get_object_or_404(Member, pk=member)
    new_circle = get_object_or_404(Circle, pk=new_member.circle.id)

    # Get all members of the circle, display their join status
    

    context = {'member':new_member}
    return render(request, 'circly/dashboard.html', context)


def checkmeout(request):
    context = {}

    return render(request, 'circly/checkmeout.html', context)
