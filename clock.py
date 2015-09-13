import os
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.mail import send_mail

from django.utils import timezone


sched = BlockingScheduler()

@sched.scheduled_job('interval', seconds=5)
def timed_job():
    from .models import Member, Reminder

    from twilio.rest import TwilioRestClient
 
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    tw_client = TwilioRestClient(account_sid, auth_token)

    # Select all Reminders that are unsent
    reminders = Reminder.objects.filter(reminder_send_date__lte=timezone.now())

    for each_reminder in reminders:
        if each_reminder.member.member_email:
            # Send emails
            send_mail(each_reminder.reminder_subject, each_reminder.reminder_message, 'heal@circly.org', [each_reminder.member.member_email], fail_silently=False)
        elif each_reminder.member.member_phone:
            # Send SMS messages
            message = tw_client.messages.create(to=each_reminder.member.member_phone,
                                                from_="+14803767375",
                                                body=each_reminder.reminder_message)

        # Mark reminder as sent
        each_reminder.reminder_sent = True
        each_reminder.save()

#@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
#def scheduled_job():
#    print('This job is run every weekday at 5pm.')

sched.start()
