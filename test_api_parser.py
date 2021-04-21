#!/usr/bin/env python3
"""Tests API Parser functions from api_parser.py"""

import unittest
import datetime
from html.parser import HTMLParser

import api_parser
from altmetric import altmetric_url

class TestApiParser(unittest.TestCase):
    """Tests API Parser functions from api_parser.py"""

    def test_csv_titles_literal(self):
        """Make sure we get the same titles out (that they haven't been changed)"""
        test_tuple = ('Altmetric Attention Score',
                      'Publication Date',
                      'Authors at my Institution',
                      'Title',
                      'DOI',
                      'Journal/Collection Title',
                      'Journal ISSNs',
                      'PubMed ID',
                      'PubMedCentral ID',
                      'Departments',
                      'Output Type',
                      'Subjects (FoR)',
                      'Affiliations (GRID)',
                      'Funder',
                      'ISBN',
                      'Details Page URL'
                     )
        self.assertEqual(api_parser.csv_titles(), test_tuple)

    def test_csv_titles(self):
        """Check to make sure we get 16 titles"""
        self.assertEqual(len(api_parser.csv_titles()), 16)

    def test_generate_csv_titles(self):
        """Given some dummy data, check to make sure that the titles are inserted correctly"""
        test_pub_data = [{'id':101571224, 'type':'research-output', 'attributes':{'title':'Inequality and the Partisan Political Economy', 'identifiers':{'dois':['10.1080/00344893.2021.1883100']}, 'readers':{'mendeley':0}, 'dimensions':{'citations':0}, 'mentions':{'tweet':10, 'wikipedia':1}, 'altmetric-score':9, 'output-type':'article', 'historical-mentions':{'1d':0, '3d':0, '1w':0, '1m':11, '3m':11, '6m':11, '1y':11, 'at':11}, 'publication-date':'2021-03-06', 'badge-url':'https://api.altmetric.com/v1/donut/101571224_240.png', 'oa-status':'false', 'oa-type':'closed', 'institution':{'verified':'true'}}, 'relationships':{'journal':{'id':'4f6fa4d93cf058f61000143d', 'type':'journal'}, 'institutional-authors':[{'id':'cuboulder:person:4758', 'type':'author'}], 'institutional-departments':[{'id':'cuboulder:group:1', 'type':'department'}, {'id':'cuboulder:group:11', 'type':'department'}, {'id':'cuboulder:group:112', 'type':'department'}, {'id':'cuboulder:group:277', 'type':'department'}, {'id':'cuboulder:group:40', 'type':'department'}, {'id':'cuboulder:group:497', 'type':'department'}, {'id':'cuboulder:group:58', 'type':'department'}], 'affiliations':[{'id':'grid.266190.a', 'type':'grid-affiliation'}], 'fields-of-research':[{'id':'16', 'type':'field-of-research'}, {'id':'1606', 'type':'field-of-research'}]}}]
        test_include_map = {'id': '4f6fa4d93cf058f61000143d', 'title': 'Representation', 'issns': ['00344893', '17494001']}
        csv_data, _ = api_parser.generate_csv(test_pub_data, test_include_map)
        test_titles = api_parser.csv_titles()
        self.assertEqual(csv_data[0], test_titles)

    def test_generate_csv_pub_data(self):
        """Given some dummy data, make sure that the first result comes after the titles, and that it's the correct output data"""
        test_pub_data = [{'id':101571224, 'type':'research-output', 'attributes':{'title':'Inequality and the Partisan Political Economy', 'identifiers':{'dois':['10.1080/00344893.2021.1883100']}, 'readers':{'mendeley':0}, 'dimensions':{'citations':0}, 'mentions':{'tweet':10, 'wikipedia':1}, 'altmetric-score':9, 'output-type':'article', 'historical-mentions':{'1d':0, '3d':0, '1w':0, '1m':11, '3m':11, '6m':11, '1y':11, 'at':11}, 'publication-date':'2021-03-06', 'badge-url':'https://api.altmetric.com/v1/donut/101571224_240.png', 'oa-status':'false', 'oa-type':'closed', 'institution':{'verified':'true'}}, 'relationships':{'journal':{'id':'4f6fa4d93cf058f61000143d', 'type':'journal'}, 'institutional-authors':[{'id':'cuboulder:person:4758', 'type':'author'}], 'institutional-departments':[{'id':'cuboulder:group:1', 'type':'department'}, {'id':'cuboulder:group:11', 'type':'department'}, {'id':'cuboulder:group:112', 'type':'department'}, {'id':'cuboulder:group:277', 'type':'department'}, {'id':'cuboulder:group:40', 'type':'department'}, {'id':'cuboulder:group:497', 'type':'department'}, {'id':'cuboulder:group:58', 'type':'department'}], 'affiliations':[{'id':'grid.266190.a', 'type':'grid-affiliation'}], 'fields-of-research':[{'id':'16', 'type':'field-of-research'}, {'id':'1606', 'type':'field-of-research'}]}}]
        test_include_map = {'4f6fa4d93cf058f61000143d': {'title': 'Representation', 'issns': ['00344893', '17494001']}, 'cuboulder:person:4758': {'name': 'LASTNAME, Firstname'}}
        csv_data, _ = api_parser.generate_csv(test_pub_data, test_include_map)
        self.assertEqual(csv_data[1], (9, datetime.date(2021, 3, 6), 'Lastname, Firstname', 'Inequality and the Partisan Political Economy', 'https://doi.org/10.1080/00344893.2021.1883100', 'Representation', '00344893, 17494001', '', '', '', 'article', '', '', '', '', 'https://www.altmetric.com/details/101571224'))

    def test_generate_csv_email_data(self):
        """Given some dummy data, make sure that the email data comes out correctly for email processing"""
        test_pub_data = [{'id':101571224, 'type':'research-output', 'attributes':{'title':'Inequality and the Partisan Political Economy', 'identifiers':{'dois':['10.1080/00344893.2021.1883100']}, 'readers':{'mendeley':0}, 'dimensions':{'citations':0}, 'mentions':{'tweet':10, 'wikipedia':1}, 'altmetric-score':9, 'output-type':'article', 'historical-mentions':{'1d':0, '3d':0, '1w':0, '1m':11, '3m':11, '6m':11, '1y':11, 'at':11}, 'publication-date':'2021-03-06', 'badge-url':'https://api.altmetric.com/v1/donut/101571224_240.png', 'oa-status':'false', 'oa-type':'closed', 'institution':{'verified':'true'}}, 'relationships':{'journal':{'id':'4f6fa4d93cf058f61000143d', 'type':'journal'}, 'institutional-authors':[{'id':'cuboulder:person:4758', 'type':'author'}], 'institutional-departments':[{'id':'cuboulder:group:1', 'type':'department'}, {'id':'cuboulder:group:11', 'type':'department'}, {'id':'cuboulder:group:112', 'type':'department'}, {'id':'cuboulder:group:277', 'type':'department'}, {'id':'cuboulder:group:40', 'type':'department'}, {'id':'cuboulder:group:497', 'type':'department'}, {'id':'cuboulder:group:58', 'type':'department'}], 'affiliations':[{'id':'grid.266190.a', 'type':'grid-affiliation'}], 'fields-of-research':[{'id':'16', 'type':'field-of-research'}, {'id':'1606', 'type':'field-of-research'}]}}]
        test_include_map = {'4f6fa4d93cf058f61000143d': {'title': 'Representation', 'issns': ['00344893', '17494001']}, 'cuboulder:person:4758': {'name': 'LAST, First'}}
        _, email_data = api_parser.generate_csv(test_pub_data, test_include_map)
        self.assertEqual(email_data[0], {'Author': 'Last, First', 'Journal': 'Representation', 'PubDate': datetime.date(2021, 3, 6), 'Title': 'Inequality and the Partisan Political Economy', 'Link': 'https://www.altmetric.com/details/101571224'})

    def test_generate_csv_pub_data_two_authors(self):
        """Given some dummy data with two authors, make sure that they get properly capitalized and output in the CSV data"""
        test_pub_data = [{'id':101571224, 'type':'research-output', 'attributes':{'title':'Inequality and the Partisan Political Economy', 'identifiers':{'dois':['10.1080/00344893.2021.1883100']}, 'readers':{'mendeley':0}, 'dimensions':{'citations':0}, 'mentions':{'tweet':10, 'wikipedia':1}, 'altmetric-score':9, 'output-type':'article', 'historical-mentions':{'1d':0, '3d':0, '1w':0, '1m':11, '3m':11, '6m':11, '1y':11, 'at':11}, 'publication-date':'2021-03-06', 'badge-url':'https://api.altmetric.com/v1/donut/101571224_240.png', 'oa-status':'false', 'oa-type':'closed', 'institution':{'verified':'true'}}, 'relationships':{'journal':{'id':'4f6fa4d93cf058f61000143d', 'type':'journal'}, 'institutional-authors':[{'id':'cuboulder:person:4758', 'type':'author'}, {'id':'cuboulder:person:12345', 'type':'author'}], 'institutional-departments':[{'id':'cuboulder:group:1', 'type':'department'}, {'id':'cuboulder:group:11', 'type':'department'}, {'id':'cuboulder:group:112', 'type':'department'}, {'id':'cuboulder:group:277', 'type':'department'}, {'id':'cuboulder:group:40', 'type':'department'}, {'id':'cuboulder:group:497', 'type':'department'}, {'id':'cuboulder:group:58', 'type':'department'}], 'affiliations':[{'id':'grid.266190.a', 'type':'grid-affiliation'}], 'fields-of-research':[{'id':'16', 'type':'field-of-research'}, {'id':'1606', 'type':'field-of-research'}]}}]
        test_include_map = {'4f6fa4d93cf058f61000143d': {'title': 'Representation', 'issns': ['00344893', '17494001']}, 'cuboulder:person:4758': {'name': 'PERSON, Test'}, 'cuboulder:person:12345': {'name': 'TEST, Person'}}
        csv_data, _ = api_parser.generate_csv(test_pub_data, test_include_map)
        self.assertEqual(csv_data[1], (9, datetime.date(2021, 3, 6), 'Person, Test; Test, Person', 'Inequality and the Partisan Political Economy', 'https://doi.org/10.1080/00344893.2021.1883100', 'Representation', '00344893, 17494001', '', '', '', 'article', '', '', '', '', 'https://www.altmetric.com/details/101571224'))

    def test_generate_csv_email_data_two_authors(self):
        """Given some dummy data with two authors, make sure that they get properly capitalized and output for email data"""
        test_pub_data = [{'id':101571224, 'type':'research-output', 'attributes':{'title':'Inequality and the Partisan Political Economy', 'identifiers':{'dois':['10.1080/00344893.2021.1883100']}, 'readers':{'mendeley':0}, 'dimensions':{'citations':0}, 'mentions':{'tweet':10, 'wikipedia':1}, 'altmetric-score':9, 'output-type':'article', 'historical-mentions':{'1d':0, '3d':0, '1w':0, '1m':11, '3m':11, '6m':11, '1y':11, 'at':11}, 'publication-date':'2021-03-06', 'badge-url':'https://api.altmetric.com/v1/donut/101571224_240.png', 'oa-status':'false', 'oa-type':'closed', 'institution':{'verified':'true'}}, 'relationships':{'journal':{'id':'4f6fa4d93cf058f61000143d', 'type':'journal'}, 'institutional-authors':[{'id':'cuboulder:person:4758', 'type':'author'}, {'id':'cuboulder:person:12345', 'type':'author'}], 'institutional-departments':[{'id':'cuboulder:group:1', 'type':'department'}, {'id':'cuboulder:group:11', 'type':'department'}, {'id':'cuboulder:group:112', 'type':'department'}, {'id':'cuboulder:group:277', 'type':'department'}, {'id':'cuboulder:group:40', 'type':'department'}, {'id':'cuboulder:group:497', 'type':'department'}, {'id':'cuboulder:group:58', 'type':'department'}], 'affiliations':[{'id':'grid.266190.a', 'type':'grid-affiliation'}], 'fields-of-research':[{'id':'16', 'type':'field-of-research'}, {'id':'1606', 'type':'field-of-research'}]}}]
        test_include_map = {'4f6fa4d93cf058f61000143d': {'title': 'Representation', 'issns': ['00344893', '17494001']}, 'cuboulder:person:4758': {'name': 'PERSON, Test'}, 'cuboulder:person:12345': {'name': 'TEST, Person'}}
        _, email_data = api_parser.generate_csv(test_pub_data, test_include_map)
        self.assertEqual(email_data[0], {'Author': 'Person, Test; Test, Person', 'Journal': 'Representation', 'PubDate': datetime.date(2021, 3, 6), 'Title': 'Inequality and the Partisan Political Economy', 'Link': 'https://www.altmetric.com/details/101571224'})

    def test_generate_body_with_dummy_data_html(self):
        """Check to make sure that the last tag is an html tag"""
        test_email_data = [{'Author': 'Test Author', 'Journal': 'Test Journal', 'PubDate': datetime.datetime.now().date(), 'Title': 'Test Title', 'Link': 'https://www.altmetric.com/details/101571224'}]
        test_email_address = 'ralphie_dev@colorado.edu'
        test_body = api_parser.generate_body(test_email_data, 30, test_email_address)
        parser = HTMLParser()
        parser.feed(test_body)
        test_output = parser.get_starttag_text()
        parser.close()
        self.assertEqual(test_output, '<a href="mailto:ralphie_dev@colorado.edu">')

    def test_generate_body_with_dummy_data_author(self):
        """Check to make sure that the Test Author has been inserted correctly with a break tag"""
        test_email_data = [{'Author': 'Test Author', 'Journal': 'Test Journal', 'PubDate': datetime.datetime.now().date(), 'Title': 'Test Title', 'Link': 'https://www.altmetric.com/details/101571224'}]
        test_email_address = 'ralphie_dev@colorado.edu'
        test_body = api_parser.generate_body(test_email_data, 30, test_email_address)
        self.assertNotEqual(test_body.find('Author(s): Test Author<br>'), -1)

    # These only work if you have set an API key and secret in github actions
    #def test_get_altmetric_data_data(self):
    #    """Check to make sure we can get the last 30 days of data, and that it has at least one article included"""
    #    url = altmetric_url('cuboulder:group:112', None, 1)
    #    department_exclusions = ['Institute of Behavioral Science (IBS)', 'Research Professors', 'Other Faculty Titles', 'Regular Faculty', 'Rostered Tenure Track Faculty', 'Postdocs', 'Organisation']
    #    pub_data, _ = api_parser.get_altmetric_data(url, 30, department_exclusions)
    #    self.assertEqual(pub_data[0]['type'], 'research-output')

    #def test_get_altmetric_data_include_map(self):
    #    """Check to make sure we're getting 'includes' so that we can map IDs to authors, journals, etc"""
    #    url = altmetric_url('cuboulder:group:112', None, 1)
    #    department_exclusions = ['Institute of Behavioral Science (IBS)', 'Research Professors', 'Other Faculty Titles', 'Regular Faculty', 'Rostered Tenure Track Faculty', 'Postdocs', 'Organisation']
    #    _, include_map = api_parser.get_altmetric_data(url, 30, department_exclusions)
    #    self.assertGreater(len(include_map), 0)
    #    self.assertTrue(list(include_map.keys())[0].isalnum())

if __name__ == "__main__":
    unittest.main()
