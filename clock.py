import os
import sys
import logging
import datetime

import psycopg2
import urlparse

from apscheduler.schedulers.blocking import BlockingScheduler


logging.basicConfig()

sched = BlockingScheduler()

@sched.scheduled_job('cron', second=10)
def scheduled_job():
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

    # Enter in new reminders for all unrefreshed circles

    # Add all unrefreshed circles to a list


    # Check circle last reminder refresh date

        # If null, add to refresh


        # Else if > 30 days add to refresh


    # Get all members of each circle in list


    # If all members of each circle have entered profiles


        # Populate their circle with reminders


    # Else send a reminder to circle owner and to members who did not enter profiles


    # Now send out all emails and SMS texts
    from twilio.rest import TwilioRestClient

    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    tw_client = TwilioRestClient(account_sid, auth_token)

    import sendgrid

    sg_user = os.environ['EMAIL_HOST_USER_VAR']
    sg_password = os.environ['EMAIL_HOST_PASSWORD_VAR']
    sg = sendgrid.SendGridClient(sg_user, sg_password)

    # Select all Reminders that are unsent
    reminder_cur = conn.cursor()
    reminder_cur.execute("""select * from circly_reminder where reminder_send_date < now() and reminder_sent_on_date is null""")
    reminders = reminder_cur.fetchall()

    for each_reminder in reminders:
        member_cur = conn.cursor()
        member_cur.execute("""select * from circly_member where id = %s""" % each_reminder[5])

        members = member_cur.fetchall()

        for each_member in members:
            if each_member[2]:
                # Send emails
                message = sendgrid.Mail()
                message.add_to('<' + each_member[2] + '>')
                message.set_subject(each_reminder[1])
                message.set_html(each_reminder[2])
                message.set_text(each_reminder[2])
                message.set_from('Your circle of support <heal@circly.org>')
                status, msg = sg.send(message)
            elif each_member[12]:
                # Send SMS messages
                message = tw_client.messages.create(to=each_member[12],
                                                    from_="+14803767375",
                                                    body=each_reminder[2])

            # Mark reminder as sent
            member_cur.execute("""update circly_reminder set reminder_sent_on_date = now() where id = '%s'""" % each_reminder[0])
            conn.commit()

sched.start()
