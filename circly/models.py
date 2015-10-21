import uuid
from django.db.models import Model
from django.db.models import CharField, DateTimeField, ForeignKey, BooleanField
from django.db.models import URLField, SmallIntegerField, UUIDField
from django.utils import timezone


class Event(Model):
    event_id = CharField(max_length=50)
    event_name = CharField(max_length=200)
    event_date = DateTimeField('date of event')

    def __unicode__(self):
        return self.event_name


class Attendee(Model):
    event = ForeignKey(Event)
    attendee_id = CharField(max_length=50)
    attendee_email = CharField(max_length=200)
    attendee_name = CharField(max_length=100)
    checked_in = BooleanField(default=False)

    def __unicode__(self):
        return self.attendee_name


class Circle(Model):
    circle_name = CharField(max_length=100)
    circle_created_date = DateTimeField('circle created on')
    circle_reminders_refreshed_on_date = DateTimeField('reminders refreshed on', null=True, blank=True)
    circle_short_url = URLField(null=True, blank=True)

    def circle_owner_name(self):
        circle_owner = self.member_set.filter(circle_owner=True)
        name_str = circle_owner[0].member_name

        return name_str


    def __unicode__(self):
        return self.circle_name


class Member(Model):
    from choices_member import *

    circle = ForeignKey(Circle)
    circle_owner = BooleanField(default=False)
    member_name = CharField(max_length=100)
    member_created_date = DateTimeField('member created on', null=True, blank=True)
    member_email = CharField(max_length=200, null=True, blank=True)
    member_phone = CharField(max_length=25, null=True, blank=True)

    age_range = CharField(max_length=5,
                          choices=AGE_RANGE_CHOICES,
                          default=BTWN_20_29)

    sex_range = CharField(max_length=2,
                          choices=SEX_CHOICES,
                          default=FEMALE)

    ethnicity_range = CharField(max_length=3,
                                choices=ETHNICITY_CHOICES,
                                default=WHITE)

    bmi_range = CharField(max_length=3,
                          choices=BMI_CHOICES,
                          default=BMI_UNDER)

    smoker = BooleanField(default=False)
    drinker = BooleanField(default=False)
    exercises = BooleanField(default=True)

    cancer_family = SmallIntegerField(default=0)

    member_profile_entered_date = DateTimeField('profile entered on', null=True, blank=True)


    def risk(self):
        female_risk_percentage = {UNDER_20: 0.0000,
                                  BTWN_20_29: 0.0006,
                                  BTWN_30_39: 0.0044,
                                  BTWN_40_44: 0.0145,
                                  BTWN_45_49: 0.0145,
                                  BTWN_50_59: 0.0233,
                                  OVER_60: 0.0345,
                                 }

        male_risk_percentage = 0.0010

        return


    def add_reminders(self):
        return


    def __unicode__(self):
        return self.member_name


class Invitation(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    member = ForeignKey(Member)
    invite_code = CharField(max_length=300, null=True, blank=True)
    invite_short_url = URLField(null=True, blank=True)
    invite_created_date = DateTimeField('invite created on')
    invite_send_date = DateTimeField('send invite on', null=True, blank=True)
    invite_sent_on_date = DateTimeField('invite sent on', null=True, blank=True)
    member_joined_on_date = DateTimeField('member joined on', null=True, blank=True)


    def __unicode__(self):
        return unicode(self.id)


class Reminder(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    member = ForeignKey(Member)
    reminder_subject = CharField(max_length=65)
    reminder_message = CharField(max_length=150)
    reminder_created_date = DateTimeField('reminder created on')
    reminder_send_date = DateTimeField('send reminder on', null=True, blank=True)
    reminder_sent_on_date = DateTimeField('reminder sent on', null=True, blank=True)
    member_reminded_on_date = DateTimeField('member reminded on', null=True, blank=True)


    def is_an_email(self):
        if (self.member.member_email):
            return True

        return False


    def is_an_SMS(self):
        if (self.member.member_phone):
            return True

        return False


    def __unicode__(self):
        return unicode(self.id)
