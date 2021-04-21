"""A collection of functions for interacting with the Altmetric public API
and the Altmetric Explorer API.
Public API Documentation: https://www.altmetric.com/research-access/
Explorer API Documentation: https://www.altmetric.com/explorer/documentation/api
"""

import hmac
import re
import time
import requests
import os

REGEX = re.compile(r'https\:\/\/api\.altmetric\.com\/v1\/donut\/([0-9]*)_240.png')

def get_api(environment_variable):
    """Gets API keys or secrets from environment variables"""
    if not isinstance(environment_variable, str):
        raise TypeError('API key must be a string')
    if len(os.environ[environment_variable]) != 32 or not (os.environ[environment_variable]).isalnum():
        raise ValueError(f'{ environment_variable } is not 32 alphanumeric characters')
    return os.environ[environment_variable]

def badge_to_details_url(url):
    """Takes in an Altmetric Badge URL in the form https://api.altmetric.com/v1/donut/########_240.png, gets the ### portion, and puts it into the proper form for a details url"""
    return 'https://www.altmetric.com/details/' + REGEX.match(url).group(1)

def get_article_details(altmetric_id):
    """Gets article details from the public API with no API key, based on the Altmetric ID"""
    time.sleep(0.5)
    url = 'https://api.altmetric.com/v1/id/' + str(altmetric_id)
    result = requests.get(url)
    if result.status_code == 200:
        return result.status_code, result.json()
    return result.status_code, {}

def digest_to_hmac(filter_list, environment_prefix=None):
    """Converts the list, or | separated string of filters, excluding 'order' to a digest with the private API key"""
    if environment_prefix is None:
        environment_variable = 'ALTMETRIC_API_SECRET'
    else:
        environment_variable = environment_prefix + '_ALTMETRIC_API_SECRET'
    api_secret = bytes(get_api(environment_variable), 'utf-8')
    if isinstance(filter_list, list):
        if 'order' in filter_list:
            filter_list.remove('order')
        filters = bytes('|'.join(filter_list), 'utf-8')
    else:
        filters = bytes(str(filter_list), 'utf-8')
    digest = hmac.new(api_secret, filters, 'sha1').hexdigest()
    return digest

def altmetric_url(department, environment_prefix=None, page_size=100):
    """Generates an Altmetric API URL based on the desired filters passed as an argument either as a list or as a | separated string"""
    department_for_url = department.replace(':', '%3A')
    web_filters = 'department_id|' + department
    if environment_prefix is None:
        environment_variable = 'ALTMETRIC_API_KEY'
    else:
        environment_variable = environment_prefix + '_ALTMETRIC_API_KEY'
    digest = digest_to_hmac(web_filters, environment_prefix)
    key = get_api(environment_variable)
    url = 'https://www.altmetric.com/explorer/api/research_outputs?digest=' + str(digest) + '&filter[department_id]=' + department_for_url + '&filter[order]=publication_date&key=' + key + '&page[size]=' + str(page_size)
    url = url.replace('[', '%5B').replace(']', '%5D')
    return url
