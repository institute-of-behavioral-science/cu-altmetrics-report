""" This module parses data from the Altmetric API for output to CSV
Email, or any other use"""
import time
from datetime import datetime, timedelta
from operator import itemgetter
import requests

from altmetric import badge_to_details_url

def assign_attribute(attribute_dictionary, sub_attribute):
    """Grabs the correct attribute from our data dictionary so that we can assign it to a variable"""
    if sub_attribute in attribute_dictionary.keys():
        if isinstance(attribute_dictionary[sub_attribute], list):
            return ', '.join(attribute_dictionary[sub_attribute])
        return attribute_dictionary[sub_attribute]
    return ''

def csv_titles():
    """Creates the list of friendly titles for our CSV columns"""
    return ('Altmetric Attention Score',
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

def get_altmetric_data(url, timeframe_days=365, department_exclusions=['Research Professors', 'Other Faculty Titles', 'Regular Faculty', 'Rostered Tenure Track Faculty', 'Postdocs', 'Organisation']):
    """Gets data from the API and processes it into a data dictionary with the publications.
    Also processes the include_map, which associates Altmetric IDs for Journals,
    Authors, and other important attributes with their human-readable names"""
    # Initialize our return values
    pub_data = []
    include_map = {}

    # Go request the json from the api
    request = requests.get(url).json()

    # Figure out how many pages of results there are
    total_pages = request['meta']['response']['total-pages']

    # Exclude some redundant 'department' and 'affiliation' fields. Used below
    affiliation_exclusions = ['University of Colorado Boulder']

    # Go through the API 'include' data and map IDs to friendly names in include_map
    # For the first page only
    # Do the same for subsequent pages, up until the last result on the page is beyond our timeframe_days value
    last_page = False
    for i in range(total_pages):
        time.sleep(0.5)
        print(f'Loading page {i+1} of {total_pages}')
        if last_page:
            break
        # Store the publications ('data') section to our data dictionary
        pub_data.extend(request['data'])
        # Get the 'include' data (Journal/Author/etc mappings to altmetric IDs)
        included = request['included']
        for include in included:
            if include['id'] not in include_map.keys():
                if include['type'] == 'journal':
                    include_map[include['id']] = {'title': include['attributes']['title'], 'issns': include['attributes']['issns']}
                if include['type'] == 'author':
                    include_map[include['id']] = {'name': include['attributes']['name']}
                if include['type'] == 'department' and include['attributes']['name'] not in department_exclusions:
                    include_map[include['id']] = {'name': include['attributes']['name']}
                if include['type'] == 'grid-affiliation' and include['attributes']['name'] not in affiliation_exclusions:
                    include_map[include['id']] = {'name': include['attributes']['name']}
                if include['type'] == 'grid-funder':
                    include_map[include['id']] = {'name': include['attributes']['name']}
                if include['type'] == 'field-of-research':
                    include_map[include['id']] = {'name': include['attributes']['name']}
        if request['links']['self'] != request['links']['last']:
            request = requests.get(request['links']['next']).json()
        if type(request['data'][-1]['attributes']['publication-date']) is None or (datetime.now() - datetime.strptime(request['data'][-1]['attributes']['publication-date'], '%Y-%m-%d')) > timedelta(days=timeframe_days):
            last_page = True
    # Store this as a list of dicts to be easier to iterate over
    return pub_data, include_map

def generate_csv(pub_data, include_map, timeframe_days=365, email_timeframe_days=60):
    """Generates the lists of dictionaries we need for processing into a CSV and email body"""
    # Initialize our return values
    csv_data = []
    email_data = []

    # Iterate through the publication data list of dictionaries
    for result in pub_data:
        # Create some sub-dictionaries for easing processing
        d = result['attributes']
        i = result['attributes']['identifiers']
        m = result['attributes']['mentions']
        r = result['relationships']

        # Initialize these values so that we can set them true if we want the particular publication record to be included in each type of output
        include_me = False
        include_me_email = False

        # Check the publication date to determine whether to include in email and CSV, and set it for output.
        if isinstance(assign_attribute(d, 'publication-date'), str):
            if (datetime.now() - datetime.strptime(assign_attribute(d, 'publication-date'), '%Y-%m-%d')) < timedelta(days=timeframe_days):
                include_me = True
                publication_date = datetime.strptime(assign_attribute(d, 'publication-date'), '%Y-%m-%d').date()
                if (datetime.now() - datetime.strptime(assign_attribute(d, 'publication-date'), '%Y-%m-%d')) < timedelta(days=email_timeframe_days):
                    include_me_email = True
        else:
            publication_date = datetime.strptime('1970-01-01', '%Y-%m-%d').date()

        # Assign various values out of the sub-dictionaries that are the first argument in the assign_attribute() function
        altmetric_score      = assign_attribute(d, 'altmetric-score')
        title                = assign_attribute(d, 'title')
        output_type          = assign_attribute(d, 'output-type')
        oa_type              = assign_attribute(d, 'oa-type')

        # Add the DOI number to a URL prefix so it's clickable
        dois                 = 'https://doi.org/' + assign_attribute(i, 'dois')

        handles              = assign_attribute(i, 'handles')
        ssrns                = assign_attribute(i, 'ssrns')
        uris                 = assign_attribute(i, 'uris')
        urns                 = assign_attribute(i, 'urns')
        isbns                = assign_attribute(i, 'isbns')
        pubmed_ids           = assign_attribute(i, 'pubmed-ids')
        ads_ids              = assign_attribute(i, 'ads-ids')
        arxiv_ids            = assign_attribute(i, 'arxiv-ids')
        repec_ids            = assign_attribute(i, 'repec-ids')
        pmc_ids              = assign_attribute(i, 'pmc-ids')
        nct_ids              = assign_attribute(i, 'nct-ids')

        # Social Media Attributes
        msm                  = assign_attribute(m, 'msm')
        blog                 = assign_attribute(m, 'blog')
        policy               = assign_attribute(m, 'policy')
        tweet                = assign_attribute(m, 'tweet')
        peer_review          = assign_attribute(m, 'peer_review')
        weibo                = assign_attribute(m, 'weibo')
        fbwall               = assign_attribute(m, 'fbwall')
        wikipedia            = assign_attribute(m, 'wikipedia')
        gplus                = assign_attribute(m, 'gplus')
        linkedin             = assign_attribute(m, 'linkedin')
        rdt                  = assign_attribute(m, 'rdt')
        pinterest            = assign_attribute(m, 'pinterest')
        f1000                = assign_attribute(m, 'f1000')
        qna                  = assign_attribute(m, 'qna')
        video                = assign_attribute(m, 'video')

        syllabus             = assign_attribute(m, 'syllabus')
        readers_mendeley     = assign_attribute(d['readers'], 'mendeley')
        dimensions_citations = assign_attribute(d['dimensions'], 'citations')
        badge_url            = assign_attribute(d, 'badge-url')
        details_url          = badge_to_details_url(badge_url)

        # These attributes need to be mapped using the include_map from an altmetric ID to a human-readable name
        if 'institutional-authors' in r.keys():
            author_list = []
            for author in r['institutional-authors']:
                if author['id'] in include_map.keys():
                    author_list.append(include_map[author['id']]['name'].title())
            authors = '; '.join(author_list)
        else:
            authors = ''

        if 'institutional-departments' in r.keys():
            department_list = []
            for department in r['institutional-departments']:
                if department['id'] in include_map.keys():
                    department_list.append(include_map[department['id']]['name'])
            departments = '; '.join(department_list)
        else:
            departments = ''

        if 'journal' in r.keys():
            if r['journal']['id'] in include_map.keys():
                journal_attr = include_map[r['journal']['id']]
                journal_title = journal_attr['title']
                journal_issns = journal_attr['issns']

                if isinstance(journal_issns, list):
                    journal_issns = ', '.join(journal_issns)
            else:
                journal_title = ''
                journal_issns = ''
        else:
            journal_title = ''
            journal_issns = ''

        if 'fields-of-research' in r.keys():
            subject_list = []
            for subject in r['fields-of-research']:
                if subject['id'] in include_map.keys():
                    subject_list.append(include_map[subject['id']]['name'])
            subjects = '; '.join(subject_list)
        else:
            subjects = ''

        if 'affiliations' in r.keys():
            affiliation_list = []
            for affiliation in r['affiliations']:
                if affiliation['id'] in include_map.keys():
                    affiliation_list.append(include_map[affiliation['id']]['name'])
            affiliations = '; '.join(affiliation_list)
        else:
            affiliations = ''

        if 'funders' in r.keys():
            funder_list = []
            for funder in r['funders']:
                if funder['id'] in include_map.keys():
                    funder_list.append(include_map[funder['id']]['name'])
            funders = '; '.join(funder_list)
        else:
            funders = ''

        # Include all of the records within timeframe_days to the CSV data, row-by-row, making sure the order matches values from csv_titles()
        if include_me:
            csv_data.append((altmetric_score,
                             publication_date,
                             authors,
                             title,
                             dois,
                             journal_title,
                             journal_issns,
                             pubmed_ids,
                             pmc_ids,
                             departments,
                             output_type,
                             subjects,
                             affiliations,
                             funders,
                             isbns,
                             details_url
                            ))

        # Include all of the records within email_timeframe_days to the email data list
        if include_me_email:
            email_data.append({'Author': authors, 'Journal': journal_title, 'PubDate': publication_date, 'Title': title, 'Link': details_url})

    # Get the titles
    titles = csv_titles()

    # Sort the data fields first
    csv_data.sort(key=itemgetter(1), reverse=True)

    # Insert the titles now that the data fields are sorted by date
    csv_data.insert(0, titles)

    return csv_data, email_data

def generate_body(email_data, email_timeframe_days, email_sender, num_results=10):
    """Takes in the list of dictionaries from email_data and formats it into a list of publications within email_timeframe_days"""
    # Gets the earliest publication in the included list and the duration to include as strings for display
    duration = str((datetime.now().date() - email_data[-1]['PubDate']).days)
    timeframe = str(email_timeframe_days)

    # Sets the first lines of the body before we include publications
    body = '<h2>Showing IBS Publications from the last ' + timeframe + ' days: </h2>' + \
    '<h4>Oldest publication shown here is ' + duration + ' days old.</h4>'

    # Initialize some values for the loop
    included_results = 0
    extra_results = 0

    # Generate a nice record for each publication up to num_results, and count the ones after that
    for publication in email_data:
        if included_results < num_results:
            body = body + \
            'Author(s): ' + publication['Author'] + '<br>' + \
            'Journal(s): ' + publication['Journal'] + '<br>' + \
            'Published: ' + str(publication['PubDate']) + '<br>' + \
            'Title: <a href ="' + publication['Link'] + '">' + publication['Title'] + '</a><br>' + \
            '<hr style="width:50%;text-align:left;margin-left:0"><br>'
            included_results += 1
        else:
            # Counting the results after num_results for display
            extra_results += 1

    if extra_results != 0:
        # If we had more publications within email_timeframe_days than num_results
        body = body + \
        '<h3>Plus ' + str(extra_results) + ' additional publications in the last ' + timeframe + ' days. </h3><br>'
    # Add some final information at the end of the email
    body = body + \
    '<h3>See Attached CSV for the last 12 months of publications by departmental authors.</h3>' + \
    'Sent by the CRS Altmetrics Reporting Tool. To unsubscribe or for questions, email <a href="mailto:' + email_sender + '">' + email_sender +'</a>'
    return body
