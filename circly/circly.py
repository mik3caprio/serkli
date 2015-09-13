import os
import sys
import getopt
import json
import sqlite3

from contextlib import closing
from collections import deque

import eventbrite

from url_request import dorequest


#EVENTBRITE_EVENT_ID = os.environ['EVENTBRITE_EVENT_ID']
EVENTBRITE_EVENT_ID ='17475222862'

#EVENTBRITE_OAUTH_TOKEN = os.environ['EVENTBRITE_OAUTH_TOKEN']
EVENTBRITE_OAUTH_TOKEN='OZWZO4LQPRZMGXMAJLB3'


# Instantiate the Eventbrite API client.
eventbrite = eventbrite.Eventbrite(EVENTBRITE_OAUTH_TOKEN)




@app.route('/')
def index():
    """ This is the display view. """
    # Create a page for each event - pass event ID as variable in querystring

    # Get the event details
    event = eventbrite.get_event(EVENTBRITE_EVENT_ID)

    # Get the attendee list
#    cur = g.db.execute('select name, attendee_id, entries from raffle order by name asc')
#    attendees = [dict(name=row[0], attendee_id=row[1], entries=row[2]) for row in cur.fetchall()]

    checked_attendees = []

    attendees = eventbrite.get_event_attendees(EVENTBRITE_EVENT_ID)
    current_page = attendees["pagination"]["page_number"]
    last_page = attendees["pagination"]["page_count"]

    while current_page <= last_page:
        # Lowercase all names
        for each_attendee in attendees["attendees"]:
            if (each_attendee["checked_in"]):
                each_attendee["profile"]["name"] = each_attendee["profile"]["name"].lower()

                checked_attendees.append(each_attendee)

        args["page"] = current_page + 1

        attendees = eventbrite.get_event_attendees(EVENTBRITE_EVENT_ID, **args)
        current_page = attendees["pagination"]["page_number"]
        last_page = attendees["pagination"]["page_count"]


    print checked_attendees
    # Reverse so latest to sign up is at the top

    #sorted(student_objects, key=lambda student: student.age)

    checked_attendees.sort()

#    display_attendees = sorted(attendees, )

#    attendee.profile.name

    # Print out a list of all attendees with a plus and minus button for each one


    # Render our HTML.https://slack-files.com/files-tmb/T047XS613-F08U4VCGM-81e9dc4e45/slack_for_ios_upload_1024.jpg
    return render_template(
        'index.html',
        winner=False,
        event=event,
        attendees=checked_attendees
    )


#{
#    "attendees": [
#        {
#            "id": "561936325", 
#            "profile": {
#                "email": "mik3cap@gmail.com", 
#                "name": "Michael Caprio", 
#            }, 
#            "checked_in": false, 
#        }, 


def add_entry(attendee_id):
    g.db.execute('update raffle SET entries=(entries + 1) where attendee_id=?) values (?)',
                 [attendee_id])
    g.db.commit()

    flash('New entry was successfully added')

    # Render our HTML.
    return render_template(
        'index.html',
        winner=False,
        event=event,
        attendees=attendees
    )


def remove_entry(attendee_id):
    cur = g.db.execute('select entries from raffle where attendee_id=?', [attendee_id])
    result = [dict(entries=row[0]) for row in cur.fetchall()]

    if result['entries'] >= 1:
        g.db.execute('update raffle SET entries=(entries - 1) where attendee_id=?) values (?)',
                     [attendee_id])
        g.db.commit()

        flash('Entry was successfully removed')

    # Render our HTML.
    return render_template(
        'index.html',
        winner=False,
        event=event,
        attendees=attendees
    )


def refresh_attendees():
    # Reload the attendee list and add new attendees


    # Render our HTML.
    return render_template(
        'index.html',
        winner=False,
        event=event,
        attendees=attendees
    )  


def pick_winner(event_id):
    # Create the pool to choose from
    event_pool = create_pool(event_id)

    # Pick a winner from the pool
    winning_user_id = select_winner(event_pool)


    # Render our HTML.
    return render_template(
        'index.html',
        winner=True,
        event=event,
        attendees=attendees
    )


if __name__ == '__main__':
    app.run()


# Store the number of raffle entries for each attendee

# Plus increase chances to win by one, minus decreases chances



# Create a pool of contestants
def create_pool(event_id):
    """The method that creates a pool of contestants."""
    # Use a double ended queue structured list for the pool
    pool_deque = deque([])

    # Get the list of all attendees for an event; only -> "checked_in": true
    eventbrite = Eventbrite('OZWZO4LQPRZMGXMAJLB3')
    this_event = eventbrite.get('/events/' + event_id + '/attendees')

    # Add all attendee IDs to a deque as many times as the ID
    # has chances to win


    for each_attendee in this_event["attendees"]:
        pool_deque.append(each_attendee["id"])

        # Match each attendee to their number entries in the database


    current_page = int(this_event["pagination"]["page_number"])
    last_page = int(this_event["pagination"]["page_count"])

    if (current_page != last_page):
        while (current_page <= last_page):
            this_event = eventbrite.get('/events/' + event_id + '/attendees?page=' + str(current_page + 1))



            current_page = this_event["pagination"]["page_number"]
            last_page = this_event["pagination"]["page_count"]

    return pool_deque


# Select the winner from the pool
def select_winner(this_pool):
    """A method to pick a winner from a pool."""
    from random import shuffle

    # Get size of pool
    pool_size = len(this_pool)

    # Randomize the order of the pool
    random.shuffle(this_pool)

    # Use random.org to pick a random number between 0 and pool size
    random_pick = process_random_org_query(pool_size)

    # Shift to the winning id and pop it
    this_pool.rotate(random_pick)

    the_winning_id = this_pool.popleft()

    return the_winning_id


def process_random_org_query(pool_size):
    version = ""
    server = "https://api.random.org/json-rpc/1/invoke" + version
    endpoint_type = ""

    url = server + endpoint_type
    params = {}

    params["jsonrpc"] = "2.0"
    params["method"] = "generateIntegers"
    params["id"] = "1"

    params["params"] = {"n": 1, "min": 0, "max": pool_size, "replacement": false}

    random_json = dorequest(url,
                            params,
                            debug=_debug)

    random_json = json.loads(random_json)

    for each_item in random_json["result"]["random"]["data"]:
        chosen_number = int(each_item)

    return chosen_number
