#!/usr/bin/env python3
"""Queries the Altmetric API, generates a CSV of the data, and emails it"""

import csv
import time
from datetime import datetime

import gmail
from altmetric import altmetric_url
from api_parser import get_altmetric_data, generate_csv, generate_body

# You'll need to get a credentials.json file and make sure that it lands in the root of the repo.
# You can get the credentials.json by following Step 1 for your service account here:
# https://developers.google.com/gmail/api/quickstart/python
# Then run this file, and you'll get a token.json. That and credentials.json will need to be
# in the root of the repo in order to send emails. Make sure EMAIL_ADDRESS below matches
# that gmail account.

# If you're using this with github actions, make sure that the contents of
# credentials.json are stored as a secret named GMAIL_CREDENTIALS and token.json is stored as
# a secret named GMAIL_TOKEN. The actions will ingest these and use them.
# Make sure to set ALTMETRIC_API_KEY to your Altmetrics API key, and ALTMETRICS_API_SECRET
# to your Altmetrics API secret, both of which you can get from
# https://www.altmetric.com/explorer/documentation/api once you're logged in.

# Number of days worth of results to include in the body of the email that's sent
EMAIL_TIMEFRAME_DAYS = 60
# The email address as a string
EMAIL_ADDRESS = 'ralphie_automated@colorado.edu'
# Name you'd like the email to show up as being from, as a string
EMAIL_FRIENDLY_NAME = 'CRS Altmetrics Tool'
# Subject line for the report email
EMAIL_REPORT_SUBJECT = 'Weekly Altmetrics Publications Report'

# Altmetrics Department ID
ALTMETRICS_DEPT_ID = 'cuboulder:group:###'

# Number of days worth of results to include in the attached CSV spreadsheet
TIMEFRAME_DAYS = 365

# True means that we will look at all returned API pages. False means we'll only look at the first.
INCLUDE_ALL = True

# list of emails to send the summary email to
SEND_REPORTS_TO_EMAILS = ['ralphie_dev@colorado.edu', 'ralphie_staff@colorado.edu']
# list of emails to send test emails to. Will only use this list if the 'DEV' environment
# variable is set to any value.
SEND_DEV_REPORTS_TO_EMAILS = ['ralphie_dev@colorado.edu']

# Let's get the email addresses based on our environment
EMAILS = gmail.get_emails(SEND_REPORTS_TO_EMAILS, SEND_DEV_REPORTS_TO_EMAILS)

# go get our altmetric URL for our department ID
ALTMETRIC_URL = altmetric_url(ALTMETRICS_DEPT_ID)
# Replace 'Institute of Behavioral Science(IBS)' with the friendly name of your institute or
# department if you don't want to see it for every result.
DEPARTMENT_EXCLUSIONS = ['Institute of Behavioral Science (IBS)', 'Research Professors', 'Other Faculty Titles', 'Regular Faculty', 'Rostered Tenure Track Faculty', 'Postdocs', 'Organisation']

# Get data from the API and put it into python datastructures for processing
PUB_DATA, INCLUDE_MAP = get_altmetric_data(ALTMETRIC_URL, TIMEFRAME_DAYS, True, DEPARTMENT_EXCLUSIONS)
CSV_DATA, EMAIL_DATA = generate_csv(PUB_DATA, INCLUDE_MAP, TIMEFRAME_DAYS, EMAIL_TIMEFRAME_DAYS)

# Get the current YYYY-mm-dd date and create a filename out of it
DATE = datetime.now().strftime("%Y-%m-%d")
FILENAME = 'Altmetric Pubs ' + DATE + '.csv'

# Generate the email body in HTML with the data we gathered from the API
EMAIL_BODY = generate_body(EMAIL_DATA, EMAIL_TIMEFRAME_DAYS, EMAIL_ADDRESS)

def main(email_address, email_friendly_name, email_subject):
    """Writes the CSV data to the csv file, then opens a connection to gmail and sends the email with that attachment"""
    with open(FILENAME, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(CSV_DATA)

    service = gmail.setup()
    sender_email = email_address
    email_from = email_friendly_name + ' <' + sender_email +'>'

    for email in EMAILS:
        email_to = email
        message = gmail.create_message_with_attachment(email_from, email_to, email_subject, EMAIL_BODY, FILENAME)
        gmail.send_message(service, sender_email, message)
        time.sleep(0.5)

if __name__ == "__main__":
    main(EMAIL_ADDRESS, EMAIL_FRIENDLY_NAME, EMAIL_REPORT_SUBJECT)
