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
    reminder_cur = conn.cursor()
    reminder_cur.execute("""select * from circly_reminder where reminder_send_date < now() and reminder_sent = false""")
    reminders = reminder_cur.fetchall()

    for each_reminder in reminders:
        member_cur = conn.cursor()
        member_cur.execute("""select * from circly_member where id = %s""" % each_reminder[6])

        members = member_cur.fetchall()

        for each_member in members:
            if each_member[2]:
                # Send emails
                message = sendgrid.Mail()
                message.add_to('<' + each_member[2] + '>')
                message.set_subject(each_reminder[1])
                message.set_html(each_reminder[2])
                message.set_text(each_reminder[2])
                message.set_from('Circly Support <heal@circly.org>')
                status, msg = sg.send(message)
            elif each_member[12]:
                # Send SMS messages
                message = tw_client.messages.create(to=each_member[12],
                                                    from_="+14803767375",
                                                    body=each_reminder[2])

            # Mark reminder as sent
            member_cur.execute("""update circly_reminder set reminder_sent = true where id = '%s'""" % each_reminder[0])
            conn.commit()

sched.start()
