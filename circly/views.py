import datetime
from django import forms

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext, loader
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.views import generic

from choices_member import *
from forms import *
from helpers import set_member_and_circle, get_current_member, get_current_circle
from helpers import get_member_id_from_invite, hash_invite
from helpers import is_phone, is_email
from helpers import random_bitly

import phonenumbers

from models import Circle, Member, Reminder, Invitation


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
            return HttpResponseRedirect(reverse("connect:submitinvite", 
                                        kwargs={}))
    else:
        # Check for valid invite code
        invite_code = ""

#        if get_member_id_from_invite(invite_code, member_contact_info):
#            print('You entered the right password')
#        else:
#            print('I am sorry but the password does not match')


        # Get member from invite code
        invite_member_id = get_member_id_from_invite(invite_code)

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

    if (drink == YES):
        new_member.drinker = True
    else:
        new_member.drinker = False

    if (smoke == YES):
        new_member.smoker = True
    else:
        new_member.smoker = False

    if (exercise == YES):
        new_member.exercises = True
    else:
        new_member.exercises = False

    new_member.member_profile_entered_date = timezone.now()

    new_member.save()

    return HttpResponseRedirect(reverse("connect:thankyou", 
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

    if (drink == YES):
        new_member.drinker = True
    else:
        new_member.drinker = False

    if (smoke == YES):
        new_member.smoker = True
    else:
        new_member.smoker = False

    if (exercise == YES):
        new_member.exercises = True
    else:
        new_member.exercises = False

    new_member.member_profile_entered_date = timezone.now()

    new_member.save()

    return HttpResponseRedirect(reverse("connect:network", 
                                        kwargs={}))


def network(request):
    new_member = get_current_member(request)

    context = {"member":new_member, "num_range_str":settings.CONTACT_RANGE_STR, "custom_errors":""}
    return render(request, "circly/network.html", context)


def submitcircle(request):
    new_member = get_current_member(request)
    new_circle = get_current_circle(request)

    count = 2
    posted_members = {}

    custom_errors = ""

    while count <= settings.CIRCLE_MAX_SIZE:
        member_contact = {}

        current_name = request.POST.get("name_" + str(count), None)
        current_contact = request.POST.get("contact_" + str(count), None)

        if len(posted_members) < (settings.CIRCLE_MIN_SIZE - 1):
            # Logic for minimum number of circle members
            if (current_name):
                if (current_contact):
                    # Check to see if current contact info is valid phone or email
                    if is_phone(current_contact):
                        member_contact["contact_type"] = "phone"

                    if is_email(current_contact):
                        member_contact["contact_type"] = "email"

                    if not is_phone(current_contact) and not is_email(current_contact):
                        # Bad data error
                        custom_errors += "<li>contact_" + str(count) + " must be either a valid phone number OR email</li>"

                    member_contact["contact_info"] = current_contact

                    posted_members[current_name] = member_contact
                else:
                    # Missing contact data error
                    custom_errors += "<li>name_" + str(count) + " is present but contact_" + str(count) + " is missing</li>"
            else:
                # Missing name data error
                custom_errors += "<li>name_" + str(count) + " is missing</li>"

        count += 1

    # Check to see if we have minimum more members added
    if len(posted_members) < (settings.CIRCLE_MIN_SIZE - 1):
        custom_errors += "<li>You need at least " + str(settings.CIRCLE_MIN_SIZE) + " members (including yourself) in your circle</li>"

    if custom_errors != "":
        custom_errors = format_html("<p><ul>{}</ul></p>",
                                    mark_safe(custom_errors))

        # If there are any errors, kick out and display them
        context = {"member":new_member, "num_range_str":settings.CONTACT_RANGE_STR, "custom_errors":custom_errors, }
        return render(request, "circly/network.html", context)

    for each_member in posted_members.keys():
        # Create new members and add to the circle
        if (posted_members[each_member]["contact_type"] == "email"):
            next_member = Member(circle=new_circle,
                                 circle_owner=False,
                                 member_name=each_member,
                                 member_email=posted_members[each_member]["contact_info"],
                                 member_created_date=timezone.now(), )
        elif (posted_members[each_member]["contact_type"] == "phone"):
            next_member = Member(circle=new_circle,
                                 circle_owner=False,
                                 member_name=each_member,
                                 member_phone=phonenumbers.format_number(posted_members[each_member]["contact_info"], 
                                                                         phonenumbers.PhoneNumberFormat.E164),
                                 member_created_date=timezone.now(), )

        next_member.save()

        # Create invite code with short link for profile sign up
        invite_code = hash_invite(posted_members[each_member]["contact_info"])

        invite_url = "http://www.circly.org/invite/" + invite_code
        new_short_url = random_bitly(invite_url)

        invite = Invitation(member=next_member,
                            invite_code=invite_code, 
                            invite_short_url=new_short_url, 
                            invite_created_date=timezone.now(),
                            invite_send_date=timezone.now())
        invite.save()

        # Create reminders for all new members to join the circle
        remind = Reminder(member=next_member,
                          reminder_subject=" would like you to join their circle of support",
                          reminder_message="Hey " + each_member + ", visit " + new_short_url + " to fill in your profile and join a circle of preventive care.",
                          reminder_created_date=timezone.now(),
                          reminder_send_date=timezone.now(), )
        remind.save()

    return HttpResponseRedirect(reverse("connect:dashboard", 
                                        kwargs={}))


def dashboard(request):
    new_member = get_current_member(request)
    new_circle = get_current_circle(request)

    context = {"member":new_member, "circle":new_circle, "circle_members":new_circle.member_set.all(), }
    return render(request, "circly/dashboard.html", context)


def thankyou(request):
    new_member = get_current_member(request)
    new_circle = get_current_circle(request)

    context = {"member":new_member, "circle":new_circle, "circle_members":new_circle.member_set.all(), }
    return render(request, "circly/thankyou.html", context)


def checkmeout(request):
    context = {}
    return render(request, "circly/checkmeout.html", context)
