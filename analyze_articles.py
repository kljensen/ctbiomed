# -*- coding: utf-8 -*-
""" This script reads in a bunch of Pubmed articles in XML format
    and outputs a series of .csv files containing various data:
    - <output_prefix>-zipcodes.csv: A breakdown of research output
      per CT zip code over time.

    Run this script like:
    python ./analyze_articles.py "articles/*.xml" output

    (Notice that you should put the glob pattern in quotes in order
    to prevent expansion of that pattern by your shell.)
"""
import sys
import glob
import xml.etree.ElementTree as ET
import codecs
import re
import csv
from collections import defaultdict


def read_article_xml(path):

    # Read in the UTF-8 encoded file
    #
    with codecs.open(path, encoding="utf-8") as fh:
        contents = fh.read()

    # Parse the XML
    #
    try:
        tree = ET.fromstring(contents.encode('utf-8'))
    except ET.ParseError:
        return (None, None)

    # Find the <Affiliation> elements.  For some reason, Pubmed
    # lists only one per article.  Bummer.
    #
    affliation = tree.find('.//Affiliation')

    # Zip code regexp: a "CT" followed by a space and 5
    # digits, followed by anything that is not a digit
    # or end-of-string.
    #
    if affliation is not None:
        ct_zip_re = re.compile(" CT (06\d{3})[^\d$]")
        match = ct_zip_re.search(affliation.text)
        if match:
            zipcode = match.group(1)
        else:
            zipcode = None
    else:
        zipcode = None

    # Find the year of publication
    #
    try:
        year = tree.find('.//JournalIssue/PubDate/Year').text
        year = int(year)
    except:
        year = None

    return (zipcode, year)


def main(argv):
    """ Main routine, fetches publication data.
    """

    # Get our list of pubmed XML files
    #
    pattern_for_glob = argv[1]
    output_file = argv[2]

    xml_files = glob.glob(pattern_for_glob)
    print "Found {0} files to analyze matching {1}".format(
        len(xml_files),
        pattern_for_glob
    )

    # Build a dictionary `articles_by_year`.  The keys of this dictionary
    # are CT zipcodes.  The values are other dictionaries where the keys
    # are year numbers and the values are the number of publications coming
    # out of that zipcode in that year.
    #
    valid_years = set(range(2000, 2013))
    articles_by_year = defaultdict(lambda: defaultdict(int))
    for (i, path) in enumerate(xml_files):
        (zipcode, year) = read_article_xml(path)
        if zipcode and year in valid_years:
            articles_by_year[zipcode][year] += 1

        if i % 100 == 0:
            print "Done with {0:5d}/{1:5d}".format(i, len(xml_files))

    with open(output_file, "w") as fh:
        csv_writer = csv.DictWriter(fh, ['Zipcode'] + sorted(valid_years))
        csv_writer.writeheader()

        # Write a csv.  One column for the zipcode and one for each year.
        #
        for zipcode, pub_counts in articles_by_year.iteritems():
            pub_counts.update({'Zipcode': str(zipcode)})
            for year in valid_years:
                if not pub_counts[year]:
                    pub_counts[year] = 0
            csv_writer.writerow(pub_counts)


if __name__ == '__main__':
    main(sys.argv)
