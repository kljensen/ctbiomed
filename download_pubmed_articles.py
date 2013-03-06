# -*- coding: utf-8 -*-
""" This script takes a list of pubmed ids, as output by `fetch_pmid_list.py`
    and downloads the XML for each of the articles, unless it alread exists
    on the file system.
"""
import requests
import sys
import codecs
import os


def main(argv):
    """ Main routine, fetches publication data.
    """

    # Get our list of pubmed ids
    #
    input_file = argv[1]
    pmids = [line.strip().split(',')[1] for line in open(input_file)]

    # Make our output directory
    #
    output_directory = argv[2]
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    efetch_url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    for pmid in pmids:

        # Skip any file that we've downloaded previously
        #
        output_file = os.path.join(output_directory, "{0}.xml".format(pmid))
        if os.path.exists(output_file):
            continue

        payload = {
            "db": "pubmed",
            "id": pmid,
            "rettype": "full",
        }
        response = requests.get(efetch_url, params=payload)

        # Write our output to a file locally.  Some authors have
        # foreign names, so best to write the file in unicode (utf-8).
        #
        output = codecs.open(output_file, mode="w", encoding="utf-8")
        output.write(response.text)
        output.close()

        # Log a message
        #
        print "Downloaded {0}".format(output_file)


if __name__ == '__main__':
    main(sys.argv)
