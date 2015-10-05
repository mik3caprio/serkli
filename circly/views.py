import datetime
from django import forms
from django.shortcuts import get_object_or_404, render

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.views import generic

from forms import *
from choices_member import *
from helpers import set_member_and_circle, get_current_member, get_current_circle

from models import Circle, Member, Reminder


def index(request):
    if request.method == "POST":
        person_form = NameForm(request.POST)

        if person_form.is_valid():
            return HttpResponseRedirect(reverse("connect:submitname", 
                                        kwargs={}))
    else:
        person_form = NameForm(auto_id="f_%s")

    context = {"form": person_form, }
    return render(request, "circly/index.html", context)


def submitname(request):
    first_name = request.POST.get("name", "")

    if (first_name != ""):
        # Create a circle
        new_circle = Circle(circle_name=first_name + "'s circle",
                            circle_created_date=timezone.now(), )
        new_circle.save()

        # Create our new member
        new_member = Member(circle=new_circle,
                            circle_owner=True,
                            member_name=first_name,
                            member_created_date=timezone.now(), )
        new_member.save()

        set_member_and_circle(request, new_circle, new_member)

        return HttpResponseRedirect(reverse("connect:flow", 
                                            kwargs={}))
    else:
        # Redisplay the name submission form
        return render(request, 
                      "circly/index.html", 
                      {"error_message": "You didn't enter a name.", })


def flow(request):
    new_member = get_current_member(request)

    if request.method == "POST":
        profile_form = FlowForm(request.POST)

        if profile_form.is_valid():
            return HttpResponseRedirect(reverse("connect:submitprofile", 
                                        kwargs={}))
    else:
        profile_form = FlowForm(auto_id="f_%s")

    context = {"member":new_member, "form": profile_form, }
    return render(request, "circly/flow.html", context)


def invite(request):
    if request.method == "POST":
        new_member = get_current_member(request)

        profile_form = FlowForm(request.POST)

        if profile_form.is_valid():
            return HttpResponseRedirect(reverse("connect:submitprofile", 
                                        kwargs={}))
    else:
        # Get member from invite code
        invite_member_id = get_member_id_from_invite()

        new_member = get_object_or_404(Member, pk=invite_member_id)
        new_circle = get_object_or_404(Circle, pk=new_member.circle.id)

        set_member_and_circle(request, new_circle, new_member)

        profile_form = FlowForm(auto_id="f_%s")

    context = {"member":new_member, "form": profile_form, }
    return render(request, "circly/invite.html", context)


def submitinvite(request):
    new_member = get_current_member(request)

    chromosome = request.POST.get("chromosome", "")
    age = request.POST.get("age", "")
    ethnicity = request.POST.get("ethnicity", "")
    drink = request.POST.get("drink", "")
    smoke = request.POST.get("smoke", "")
    exercise = request.POST.get("exercise", "")
    bmi = request.POST.get("bmi", "")
    relatives = int(request.POST.get("relatives", 0))

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

    return HttpResponseRedirect(reverse("connect:dashboard", 
                                        kwargs={}))


def submitprofile(request):
    new_member = get_current_member(request)

    chromosome = request.POST.get("chromosome", "")
    age = request.POST.get("age", "")
    ethnicity = request.POST.get("ethnicity", "")
    drink = request.POST.get("drink", "")
    smoke = request.POST.get("smoke", "")
    exercise = request.POST.get("exercise", "")
    bmi = request.POST.get("bmi", "")
    relatives = int(request.POST.get("relatives", 0))

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

    return HttpResponseRedirect(reverse("connect:network", 
                                        kwargs={}))


def network(request):
    new_member = get_current_member(request)

    if request.method == "POST":
        circle_form = NetworkForm(request.POST)

        if circle_form.is_valid():
            return HttpResponseRedirect(reverse("connect:submitcircle", 
                                        kwargs={}))
    else:
        circle_form = NetworkForm(auto_id="f_%s")

    context = {"member":new_member, "form": circle_form, }
    return render(request, "circly/network.html", context)


def submitcircle(request):
    new_member = get_current_member(request)
    new_circle = get_current_circle(request)

    count = 2
    posted_members = {}

    while count <= CONTACT_RANGE:
        member_contact = {}

        current_name = request.POST.get("name_" + count, "")
        current_contact = request.POST.get("contact_" + count, "")

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

        # Create invite code with link for profile sign up


        # Create reminders for all new members to join the circle
        remind = Reminder(member=next_member,
                          reminder_subject=" would like you to join their circle of support",
                          reminder_message="Hey Mike, please tell Kennedy to do a breast self-exam! Go to the page at http://j.mp/SelfChec01 to get some ideas for what to talk about.",
                          reminder_created_date=timezone.now(),
                          reminder_send_date=timezone.now(), )
        remind.save()

    return HttpResponseRedirect(reverse("connect:dashboard", 
                                        kwargs={}))


def dashboard(request):
    new_member = get_current_member(request)
    new_circle = get_current_circle(request)

    # Get all members of the circle, display their join status
    

    context = {"member":new_member, "circle":new_circle, }
    return render(request, "circly/dashboard.html", context)


def checkmeout(request):
    context = {}

    return render(request, "circly/checkmeout.html", context)
