# Ct biomed study

## About

This repo contains some scripts for examining who is publishing
what in the biomedical journals in Connecticut.  It uses 
[NCBI's Pubmed database](http://www.ncbi.nlm.nih.gov/pubmed)
and the [eutils API](http://www.ncbi.nlm.nih.gov/books/NBK25500/).

## Installation

To get the code, do 

	git clone https://github.com/kljensen/ctbiomed

Best to use a [virtualenv](https://pypi.python.org/pypi/virtualenv).
Then do 

	pip install -r requirements.txt

to install the dependencies into your Python environment.

## Running

To download a list of all biomedical pubmed ids, run

	python ./fetch_pmid_list.py output.csv

This will put a csv-formatted list of Pubmed IDs into output.csv.
It will look like

	Year,PMID
	2000,18924689
	2000,18503422
	2000,18350009
	2000,18252404
	2000,18238659
	2000,17208856
	2000,16906197

Now, download the details for each article in XML format.

	python ./download_pubmed_articles.py output.csv articles

This will put one XML file in the `articles` directory for
each article.

	prompt> ls articles | head
		10752845.xml
		10753984.xml
		10754283.xml
		10754295.xml
		10754299.xml
		10754334.xml
		10755736.xml
		10904435.xml
		10917219.xml

You can `grep` through these files to see who is publishing.

	prompt> grep '<Affiliation>.* CT,' -m1 articles/* | cut -b-100 | head
	articles/18503422.xml: <Affiliation>Unilever Home and Personal Care Co, Skin Care Researc
	articles/18924689.xml: <Affiliation>Discovery Technologies, Neurogen Corporation, Branfor
	articles/18924712.xml: <Affiliation>Discovery Technologies, Neurogen Corporation, Branfor
	articles/19078481.xml: <Affiliation>University of Texas Health Sciences Center, San Anton
	articles/19184836.xml: <Affiliation>Department of Pathobiology, University of Connecticut
	articles/19649874.xml: <Affiliation>Pfizer Inc, Eastern Point Road, Groton, CT 06340, USA
	articles/19649897.xml: <Affiliation>Chemical Research and Development, Pfizer Inc, Groton

## Todo

There are a few interesting next steps to do:
 * Extract entities and locations from the articles.
 * Look at keys words in the articles.
 	- See if any are statistically overrepresented for CT relative to other states.
 * Plot various stuff over time.
 * Draw a social graph to show which CT institutions are publishing together.