import uuid
from django.db import models.Model, models.CharField, models.DateTimeField, models.ForeignKey, models.BooleanField
from django.db import models.URLField, models.SmallIntegerField, models.UUIDField
from django.utils import timezone


class Event(models.Model):
    event_id = models.CharField(max_length=50)
    event_name = models.CharField(max_length=200)
    event_date = models.DateTimeField('date of event')

    def __unicode__(self):
        return self.event_name


class Attendee(models.Model):
    event = models.ForeignKey(Event)
    attendee_id = models.CharField(max_length=50)
    attendee_email = models.CharField(max_length=200)
    attendee_name = models.CharField(max_length=100)
    checked_in = models.BooleanField(default=False)

    def __unicode__(self):
        return self.attendee_name


class Circle(models.Model):
    circle_name = models.CharField(max_length=100)
    circle_created_date = models.DateTimeField('circle created on')
    circle_reminders_refreshed_on_date = models.DateTimeField('reminders refreshed on', null=True, blank=True)
    circle_short_url = models.URLField(null=True, blank=True)

    def circle_owner_name(self):
        circle_owner = self.member_set.filter(circle_owner=True)
        name_str = circle_owner[0].member_name

        return name_str


    def __unicode__(self):
        return self.circle_name


class Member(models.Model):
    from choices_member import *

    circle = models.ForeignKey(Circle)
    circle_owner = models.BooleanField(default=False)
    member_name = models.CharField(max_length=100)
    member_created_date = models.DateTimeField('member created on', null=True, blank=True)
    member_email = models.CharField(max_length=200, null=True, blank=True)
    member_phone = models.CharField(max_length=25, null=True, blank=True)

    age_range = models.CharField(max_length=5,
                                 choices=AGE_RANGE_CHOICES,
                                 default=BTWN_20_29)

    sex_range = models.CharField(max_length=2,
                                 choices=SEX_CHOICES,
                                 default=FEMALE)

    ethnicity_range = models.CharField(max_length=3,
                                       choices=ETHNICITY_CHOICES,
                                       default=WHITE)

    bmi_range = models.CharField(max_length=3,
                                 choices=BMI_CHOICES,
                                 default=BMI_UNDER)

    smoker = models.BooleanField(default=False)
    drinker = models.BooleanField(default=False)
    exercises = models.BooleanField(default=True)

    cancer_family = models.SmallIntegerField(default=0)

    member_profile_entered_date = models.DateTimeField('profile entered on', null=True, blank=True)


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


class Invitation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    member = models.ForeignKey(Member)
    invite_code = models.CharField(max_length=300, null=True, blank=True)
    invite_short_url = models.URLField(null=True, blank=True)
    invite_created_date = models.DateTimeField('invite created on')
    invite_send_date = models.DateTimeField('send invite on', null=True, blank=True)
    invite_sent_on_date = models.DateTimeField('invite sent on', null=True, blank=True)
    member_joined_on_date = models.DateTimeField('member joined on', null=True, blank=True)


    def __unicode__(self):
        return unicode(self.id)


class Reminder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    member = models.ForeignKey(Member)
    reminder_subject = models.CharField(max_length=65)
    reminder_message = models.CharField(max_length=150)
    reminder_created_date = models.DateTimeField('reminder created on')
    reminder_send_date = models.DateTimeField('send reminder on', null=True, blank=True)
    reminder_sent_on_date = models.DateTimeField('reminder sent on', null=True, blank=True)
    member_reminded_on_date = models.DateTimeField('member reminded on', null=True, blank=True)


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
