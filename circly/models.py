import uuid
from django.db import models
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


    def __unicode__(self):
        return self.circle_name


class Member(models.Model):
    circle = models.ForeignKey(Circle)
    circle_owner = models.BooleanField(default=False)
    member_name = models.CharField(max_length=100)
    member_created_date = models.DateTimeField('member created on', null=True, blank=True)
    member_email = models.CharField(max_length=200, null=True, blank=True)
    member_phone = models.CharField(max_length=25, null=True, blank=True)

    UNDER_20 = '<20'
    BTWN_20_29 = '20-29'
    BTWN_30_39 = '30-39'
    BTWN_40_44 = '40-44'
    BTWN_45_49 = '45-49'
    BTWN_50_59 = '50-59'
    OVER_60 = '>60'
    AGE_RANGE_CHOICES = (
        (UNDER_20, 'under 20'),
        (BTWN_20_29, 'between 20 and 29'),
        (BTWN_30_39, 'between 30 and 39'),
        (BTWN_40_44, 'between 40 and 44'),
        (BTWN_45_49, 'between 45 and 49'),
        (BTWN_50_59, 'between 50 and 59'),
        (OVER_60, '60 and over'),
    )
    age_range = models.CharField(max_length=5,
                                 choices=AGE_RANGE_CHOICES,
                                 default=BTWN_20_29)

    FEMALE = 'XX'
    MALE = 'XY'
    SEX_CHOICES = (
        (FEMALE, 'XX sex chromosomes (female)'),
        (MALE, 'XY sex chromosomes (male)'),
    )
    sex_range = models.CharField(max_length=2,
                                 choices=SEX_CHOICES,
                                 default=FEMALE)

    WHITE = 'CNH'
    BLACK = 'AFR'
    HISPANIC = 'HIS'
    ASIAN = 'ASI'
    OTHER = 'OTH'
    ETHNICITY_CHOICES = (
        (WHITE, 'Caucasian Non-Hispanic'),
        (BLACK, 'African American'),
        (HISPANIC, 'Hispanic'),
        (ASIAN, 'Asian'),
        (OTHER, 'Other race or ethnicity'),
    )
    ethnicity_range = models.CharField(max_length=3,
                                       choices=ETHNICITY_CHOICES,
                                       default=WHITE)

    BMI_UNDER = '<25'
    BMI_OVER = '25>'
    BMI_CHOICES = (
        (BMI_UNDER, 'is less than 25'),
        (BMI_OVER, 'is 25 or greater'),
    )
    bmi_range = models.CharField(max_length=3,
                                 choices=BMI_CHOICES,
                                 default=BMI_UNDER)

    smoker = models.BooleanField(default=False)
    drinker = models.BooleanField(default=False)
    exercises = models.BooleanField(default=False)

    cancer_family = models.SmallIntegerField(default=0)

    member_profile_entered_date = models.DateTimeField('profile entered on', null=True, blank=True)


    def risk(self):
        female_risk_percentage = {self.UNDER_20: 0.0000,
                                  self.BTWN_20_29: 0.0006,
                                  self.BTWN_30_39: 0.0044,
                                  self.BTWN_40_44: 0.0145,
                                  self.BTWN_45_49: 0.0145,
                                  self.BTWN_50_59: 0.0233,
                                  self.OVER_60: 0.0345,
                                 }

        male_risk_percentage = 0.0010

        return


    def add_reminders(self):
        return


    def __unicode__(self):
        return self.member_name


class Reminder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    member = models.ForeignKey(Member)
    reminder_subject = models.CharField(max_length=65)
    reminder_message = models.CharField(max_length=150)
    reminder_created_date = models.DateTimeField('reminder created on')
    reminder_send_date = models.DateTimeField('send reminder on', null=True, blank=True)
    reminder_sent_on_date = models.DateTimeField('reminder sent on', null=True, blank=True)
    member_reminded_on_date = models.DateTimeField('member reminded on', null=True, blank=True)


    def is_an_email():
        if (self.member.member_email):
            return True

        return False


    def is_an_SMS():
        if (self.member.member_phone):
            return True

        return False


    def __unicode__(self):
        return unicode(self.id)
