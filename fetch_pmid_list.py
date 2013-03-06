# -*- coding: utf-8 -*-
""" This script does a search for all articles in Pubmed that were
    written by Connecticut authors during the years 2000-2012 inclusive.
    It outputs a CSV file containing the year and Pubmed ID of each article
    so that the "details" of each article can be fetched later.
"""
import requests
import sys
import re
import csv


def get_pmids_from_xml(xml_body):
    """ Returns a list of all pubmed ids for articles in an API response,
        like those that follow:
        <Id>17564794</Id>
        <Id>17550787</Id>
        <Id>17544337</Id>
    """
    id_re = re.compile('<Id>(\d+)</Id>')
    return id_re.findall(xml_body)


def main(argv):
    """ Main routine, fetches publication data.
    """

    # Output file
    #
    output_file = argv[1]
    output = open(output_file, "w")
    output_writer = csv.writer(output)

    # Call Pubmed API for each year, 2000-2012 inclusive
    #
    pubmed_url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    for year in range(2000, 2013):

        # Construct GET query parameters
        #
        payload = {
            "db": "pubmed",
            # Ask for all publications where CT is in the author
            # affiliation and the year is `year`
            "term": "CT[ad] AND {0}[pdat]".format(year),
            "retmax": 10000,
        }

        # Get the results
        #
        response = requests.get(pubmed_url, params=payload)
        article_pmids = get_pmids_from_xml(response.text)

        # Write the results to our output file
        #
        for pmid in article_pmids:
            output_writer.writerow([year, pmid])

        # Write a little log message
        #
        print "Found {0} CT articles published in {1}"\
                    .format(len(article_pmids), year)

    output.close()


if __name__ == '__main__':
    main(sys.argv)
