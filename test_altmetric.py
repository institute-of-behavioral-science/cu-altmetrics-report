#!/usr/bin/env python3
"""Tests Altmetric interaction functions from altmetric.py"""

import unittest
from requests import get
import os
import random
import string
import altmetric

class TestAltmetric(unittest.TestCase):
    """Tests Altmetric interaction functions from altmetric.py"""

    def test_get_api_success(self):
        api_chars = string.ascii_lowercase + string.digits
        os.environ['DEV_ALTMETRIC_API_KEY'] = ''.join(random.choice(api_chars) for i in range(32))
        self.assertEqual(altmetric.get_api('DEV_ALTMETRIC_API_KEY'), os.environ['DEV_ALTMETRIC_API_KEY'])

    def test_get_api_present_failure(self):
        api_chars = string.ascii_lowercase + string.digits
        os.environ['DEV_ALTMETRIC_API_SECRET'] = ''.join(random.choice(api_chars) for i in range(30))
        self.assertRaises(ValueError, altmetric.get_api, 'DEV_ALTMETRIC_API_SECRET')

    def test_get_api_key_absent_failure(self):
        self.assertRaises(KeyError, altmetric.get_api, 'NONEXISTENT_ALTMETRIC_API_KEY')

    def test_badge_to_details_url_literal(self):
        """Checks to see if a sample badge URL gets regexed and changed properly"""
        badge_url = 'https://api.altmetric.com/v1/donut/83360707_240.png'
        output_url = 'https://www.altmetric.com/details/83360707'
        self.assertEqual(altmetric.badge_to_details_url(badge_url), output_url)

    def test_badge_to_details_url_results(self):
        """Checks to see if a valid details link is created"""
        badge_url = 'https://api.altmetric.com/v1/donut/83360707_240.png'
        request = get(altmetric.badge_to_details_url(badge_url))
        self.assertEqual(request.status_code, 200)

    def test_get_article_details_outside_ibs(self):
        """Checks to see if we can get an individual article's details from a non-IBS author, and whether it's the right article for the ID"""
        status_code, json_object = altmetric.get_article_details(91496403)
        self.assertEqual(status_code, 200)
        self.assertEqual(json_object['title'], 'Rethinking Covid-19 Test Sensitivity — A Strategy for Containment')

    def test_get_article_details_inside_ibs(self):
        """Checks to see if we can get an individual article's details from an IBS author, and whether it's the right article for the ID"""
        status_code, json_object = altmetric.get_article_details(5082175)
        self.assertEqual(status_code, 200)
        self.assertEqual(json_object['title'], 'Effect of Removal of Planned Parenthood from the Texas Women’s Health Program')

    def test_digest_to_hmac_list_vs_string(self):
        """Checks whether the function processes strings and lists to the same hmac value"""
        digest_list = altmetric.digest_to_hmac(['department_id', 'cuboulder:group:112'])
        digest_string = altmetric.digest_to_hmac('department_id|cuboulder:group:112')
        self.assertEqual(digest_list, digest_string)

    def test_digest_to_hmac_list_with_order(self):
        """Checks to see if the 'order' attribute is successfully removed"""
        digest_list = altmetric.digest_to_hmac(['department_id', 'cuboulder:group:112', 'order', 'latest'])
        digest_list_no_order = altmetric.digest_to_hmac(['department_id', 'cuboulder:group:112', 'latest'])
        self.assertEqual(digest_list, digest_list_no_order)

    def test_digest_to_hmac_against_string(self):
        """Checks to see if we get the right hmac with an order filter that gets removed"""
        os.environ['DEV_ALTMETRIC_API_SECRET'] = 'c864n7yuw920upegazilhlz9nih3nkzs'
        digest_list = altmetric.digest_to_hmac(['department_id', 'cuboulder:group:112', 'order', 'latest'], 'DEV')
        self.assertEqual(digest_list, '8eb892eb1abb99e549a521d02939722ca4610867')
    
    # Only works if you have a defined API secret and key
    #def test_altmetric_url_results(self):
    #    """Checks to see if we can get results from the API, and whether there are more results than there were when this test was written"""
    #    request = get(altmetric.altmetric_url('cuboulder:group:112'))
    #    self.assertEqual(request.status_code, 200)
    #    self.assertGreater(request.json()['meta']['response']['total-results'], 2357)

if __name__ == "__main__":
    unittest.main()
