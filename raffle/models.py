from django.db import models

# Create your models here.
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
