# About

This repo contains some scripts for examining who is publishing
what in the biomedical journals in Connecticut.  It uses 
[NCBI's Pubmed database](http://www.ncbi.nlm.nih.gov/pubmed)
and the [eutils API](http://www.ncbi.nlm.nih.gov/books/NBK25500/).

# Installation

To get the code, do 

	git clone https://github.com/kljensen/ctbiomed

Best to use a [virtualenv](https://pypi.python.org/pypi/virtualenv).
Then do 

	pip install -r requirements.txt

to install the dependencies into your Python environment.

# Running

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