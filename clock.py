from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.mail import send_mail

sched = BlockingScheduler()

@sched.scheduled_job('interval', seconds=20)
def timed_job():
    SMS_to_send = []
    email_to_send = []

    # Select all Reminders that are unsent
    reminders = xx

    for each_reminder in reminders:
        if each_reminder.is_an_email():



    # Send SMS messages


    # Send emails
    send_mail('Reminder! Tell Kennedy to self-examine his breast', 'Hey Madelena, please send Kennedy a reminder to do a breast self-exam! Go to the page at http://j.mp/SelfChec to get some ideas for what to talk about.', 'from@example.com', ['madelena.mak@gmail.com'], fail_silently=False)


    # Mark reminder as sent
    

    print('This job is run every 20 seconds.')

#@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
#def scheduled_job():
#    print('This job is run every weekday at 5pm.')

sched.start()
