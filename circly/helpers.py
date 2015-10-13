import datetime
import hashlib
import uuid

from django.conf import settings
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from models import Circle, Member, Reminder, Invitation

import bitly_api


def random_bitly(old_url):
    c = bitly_api.Connection(api_key=settings.BITLY_CLIENT_ID,
                             secret=settings.BITLY_SECRET_KEY,
                             access_token=settings.BITLY_ACCESS_TOKEN,
                             login=settings.BITLY_LOGIN)

    bitly_data_dict = c.shorten(old_url)

    return bitly_data_dict["url"]


def clear_member_and_circle(request):
    request.session["current_circle"] = None
    request.session["current_member"] = None


def get_current_member(request):
    new_member_test = request.session.get("current_member", None)

    if new_member_test:
        new_member = get_object_or_404(Member, pk=new_member_test["id"])

        return new_member


def get_current_circle(request):
    new_circle_test = request.session.get("current_circle", None)

    if new_circle_test:
        new_circle = get_object_or_404(Circle, pk=new_circle_test["id"])

        return new_circle


def set_member_and_circle(request, new_circle, new_member):
    new_circle_dict = model_to_dict(new_circle)
    new_member_dict = model_to_dict(new_member)

    if new_circle_dict['circle_created_date']:
        new_circle_dict['circle_created_date'] = new_circle_dict['circle_created_date'].isoformat()

    if new_circle_dict['circle_reminders_refreshed_on_date']:
        new_circle_dict['circle_reminders_refreshed_on_date'] = new_circle_dict['circle_reminders_refreshed_on_date'].isoformat()

    if new_member_dict['member_created_date']:
        new_member_dict['member_created_date'] = new_member_dict['member_created_date'].isoformat()

    if new_member_dict['member_profile_entered_date']:
        new_member_dict['member_profile_entered_date'] = new_member_dict['member_profile_entered_date'].isoformat()

    request.session['current_circle'] = new_circle_dict
    request.session['current_member'] = new_member_dict


def is_phone(phone_str):
    import phonenumbers

    try:
        z = phonenumbers.parse(phone_str, "US")

        if phonenumbers.is_possible_number(z): 
            if phonenumbers.is_valid_number(z):
                return True
    except:
        return False


def is_email(email_str):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError

    try:
        validate_email(email_str)
    except ValidationError as e:
        return False
    else:
        return True


def hash_code(member_email, existing_salt=None):
    # uuid is used to generate a random number
    if (existing_salt):
        salt = existing_salt
    else:
        salt = uuid.uuid4().hex

    return hashlib.sha256(salt.encode() + member_email.encode()).hexdigest() + ':' + salt


def check_invite(invite_code):
    check_member_contact_info, salt = invite_code.split(':')

    # Get all open invites
    open_invites = Invitation.objects.filter(member_joined_on_date=None)

    for each_invite in open_invites:
        if each_invite.member.member_email:
            contact_info = each_invite.member.member_email

        if each_invite.member.member_phone:
            contact_info = each_invite.member.member_phone

        if hash_code(contact_info, salt) == invite_code:
            return each_invite.member.id

    return None


def check_owner(owner_hash):
    check_member_contact_info, salt = owner_hash.split(':')

    # Get all open invites
    circle_owners = Member.objects.filter(circle_owner=True)

    for each_owner in circle_owners:
        contact_info = None

        if each_owner.member_email:
            contact_info = each_owner.member_email

        if each_owner.member_phone:
            contact_info = each_owner.member_phone

        if contact_info:
            if hash_code(contact_info, salt) == owner_hash:
                return each_owner.id

    return None
