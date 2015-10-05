import datetime
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from models import Circle, Member, Reminder


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
    except NumberParseException:
        return False

    if phonenumbers.is_possible_number(z): 
        if phonenumbers.is_valid_number(z):
            return True

    return False


def is_email(email_str):
    from django.core.validators import validate_email

    return True
