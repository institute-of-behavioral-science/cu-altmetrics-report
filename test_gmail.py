#!/usr/bin/env python3
"""Tests Gmail Functions from gmail.py"""

import unittest
import os

import gmail

class TestGmail(unittest.TestCase):
    """Tests Gmail Functions from gmail.py"""

    def test_get_emails(self):
        """Check that we only get back the default email list in DEV environment"""
        # If Dev environment, check to see if Grant's email is the only one in the list
        emails = gmail.get_emails(['ralphie@colorado.edu', 'ralphie_dev@colorado.edu'], ['ralphie_dev@colorado.edu'])
        if bool(os.environ.get('DEV', False)):
            self.assertEqual(emails, ['ralphie_dev@colorado.edu'])
        # If not Dev environment, check to see that there is more than one element in the list
        if not bool(os.environ.get('DEV', False)):
            self.assertEqual(emails, ['ralphie@colorado.edu', 'ralphie_dev@colorado.edu'])

    def test_get_emails_dev(self):
        os.environ['DEV'] = 'True'
        self.assertEqual(gmail.get_emails(['ralphie@colorado.edu']), ['ralphie@colorado.edu'])

    def test_create_message_with_attachment(self):
        """Check to see that the length of the base64 raw message is 448, as it should be with these input values"""
        generated_message = gmail.create_message_with_attachment('test@test.com', 'test1@test.com', 'Test Subject', 'Message Text')
        self.assertEqual(len(generated_message['raw']), 448)
    
    # Only works if you have set up GMAIL_CREDENTIALS and GMAIL_TOKEN
    #def test_setup(self):
    #    """Check to see that we can close the gmail service object"""
    #    with gmail.setup() as gmail_service:
    #        self.assertIsNone(gmail_service.close())

if __name__ == "__main__":
    unittest.main()
