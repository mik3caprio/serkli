import os
import sys
import logging
import datetime

import psycopg2
import urlparse

from apscheduler.schedulers.blocking import BlockingScheduler


logging.basicConfig()

sched = BlockingScheduler()

@sched.scheduled_job('cron', second=5)
def scheduled_job():
    from circly.models import Member, Reminder

    import sendgrid
    from twilio.rest import TwilioRestClient

    try:
        urlparse.uses_netloc.append("postgres")
        url = urlparse.urlparse(os.environ["DATABASE_URL"])

        conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
    except:
        print "I am unable to connect to the database"

    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    tw_client = TwilioRestClient(account_sid, auth_token)

    sg_user = os.environ['EMAIL_HOST_USER_VAR']
    sg_password = os.environ['EMAIL_HOST_PASSWORD_VAR']
    sg = sendgrid.SendGridClient(sg_user, sg_password)

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
                message = sendgrid.Mail()
                message.add_to('<' + new_row[2] + '>')
                message.set_subject(row[1])
                message.set_html(row[2])
                message.set_text(row[2])
                message.set_from('Circly Support <heal@circly.org>')
                status, msg = sg.send(message)
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
