# CU Altmetrics Report

Connects to the Altmetric API to get information on CU Department publications, and then publishes this to a CSV and email report.

# Variables

Make sure to set the following variables and files before starting in query.py:
- EMAIL_ADDRESS: the Google email address to send from
- EMAIL_FRIENDLY_NAME: the human-readable name you'd like the report to appear from
- EMAIL_REPORT_SUBJECT: the subject line of the report emails
- ALTMETRICS_DEPT_ID: if you do an Altmetrics Explorer Research Outputs search for your department, this will show up as the last digits of the URL after 'cuboulder%3Agroup%3A'
- SEND_REPORTS_TO_EMAILS: a list of email strings to send to. See query.py for an example.
- SEND_DEV_REPORTS_TO_EMAILS: a list of email strings to send to for testing purposes. See query.py for an example.
- DEPARTMENT_EXCLUSIONS: The friendly name of your department according to Altmetrics. This is the actual name that shows up when you filter by your department in their searches.

# Required files

Create a credentials.json file according to step 1 in https://developers.google.com/gmail/api/quickstart/python and either put this in the root of your copy of the repo, or configure it as a secret for Github Actions.

After you put credentials.json into the root of your repo, run query.py (probably in a python venv) to generate token.json. Then you can configure it as a secret for Github Actions.

# Github Actions Secrets

Remove the .example suffix from the .yml files in .github/workflows/ and customize them to your needs.

- ALTMETRIC_API_KEY: a 32 character alphanumeric string from https://www.altmetric.com/explorer/documentation/api
- ALTMETRIC_API_SECRET: a 32 character alphanumeric string from https://www.altmetric.com/explorer/documentation/api
- GMAIL_CREDENTIALS: the contents of credentials.json from above
- GMAIL_TOKEN: the contents of token.json from above
