import os
import sys
import logging

import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.mail import send_mail


logging.basicConfig()

sched = BlockingScheduler()

@sched.scheduled_job('cron', second=5)
def scheduled_job():
    from circly.models import Member, Reminder

    from twilio.rest import TwilioRestClient
#    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "event_meet.settings")

    import psycopg2

    try:
        conn = psycopg2.connect("dbname='d6mes5n1fk51ca' user='dhdzbpcuvrywuw' host='ec2-54-83-58-191.compute-1.amazonaws.com' port='5432' password='dbEhHY9varxV_wKKAQAwbVrU4O'")
    except:
        print "I am unable to connect to the database"

    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    tw_client = TwilioRestClient(account_sid, auth_token)

    # Select all Reminders that are unsent
    cur = conn.cursor()
    cur.execute("""select * from circly_reminder where reminder_send_date < now() and reminder_sent = false""")
    rows = cur.fetchall()

    for row in rows:
        cur2 = conn.cursor()
        cur2.execute("""select * from circly_member where id = %s""" % row[6])

        rows2 = cur2.fetchall()

        for new_row in rows2:
            if new_row[2]:
                # Send emails
                send_mail(row[1], row[2], 'heal@circly.org', [new_row[2]], fail_silently=False)
            elif new_row[12]:
                # Send SMS messages
                message = tw_client.messages.create(to=new_row[12],
                                                    from_="+14803767375",
                                                    body=row[2])

        # Mark reminder as sent
        cur2.execute("""update circly_reminder set reminder_sent = true where id = %s""" % row[0])


#@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
#def scheduled_job():
#    print('This job is run every weekday at 5pm.')

sched.start()
