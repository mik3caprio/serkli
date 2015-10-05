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

    #{u'url': u'http://j.mp/1wADtNt', 
    # u'hash': u'1wADtNt', 
    # u'global_hash': u'2V6CFi', 
    # u'long_url': u'http://www.google.com/', 
    # u'new_hash': 1}

    return bitly_data_dict["url"]


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

    new_circle_dict['circle_created_date'] = new_circle_dict['circle_created_date'].isoformat()
    new_member_dict['member_created_date'] = new_member_dict['member_created_date'].isoformat()

    request.session['current_circle'] = new_circle_dict
    request.session['current_member'] = new_member_dict


def is_phone(phone_str):
    import phonenumbers

    try:
        z = phonenumbers.parse(phone_str, None)
    except:
        return False

    if phonenumbers.is_possible_number(z): 
        if phonenumbers.is_valid_number(z):
            return True

    return False


def is_email(email_str):
    from django.core.validators import validate_email

    return True


def hash_invite(member_email):
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex

    return hashlib.sha256(salt.encode() + member_email.encode()).hexdigest() + ':' + salt


def check_invite(invite_code, member_contact_info):
    check_member_contact_info, salt = invite_code.split(':')

    return check_member_contact_info == hashlib.sha256(salt.encode() + member_contact_info.encode()).hexdigest()


def get_member_id_from_invite(invite_code, member_contact_info):
    return ""
