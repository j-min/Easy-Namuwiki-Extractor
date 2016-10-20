import json
from multiprocessing import Pool
from namuwiki.extractor import extract_text
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-i', '--input', required = True, help = 'input_filename')
parser.add_argument('-o', '--output', required = True, help = 'output_filename')
parser.add_argument('-m', '--multiprocess', action = 'store_true', help = 'run mutiprocessing')
parser.add_argument('-t', '--title', action = 'store_true', help = 'include title of documents')

args = parser.parse_args()

json_file = args.input
output_filename = args.output
multiprocess  = args.multiprocess
title = args.title

# Simple Usage
if multiprocess == False:
	with open(json_file, 'r', encoding='utf-8') as json_file:
	    namu_wiki = json.load(json_file)

	with open(output_filename, 'w') as output_file:
		for document in namu_wiki:
			plain_text = extract_text(document['text'])
			if title == True:
				output_file.write(document['title'] + '\n')
			output_file.write(plain_text)

# Multiprocessing Usage
else:
	def work(document):
	    return {
	        'title': document['title'],
	        'content': extract_text(document['text'])
	    }

	with open(json_file, 'r', encoding='utf-8') as json_file:
	    namu_wiki = json.load(json_file)

	with Pool() as pool:
	    documents = pool.map(work, namu_wiki)
	    with open(output_filename, 'w') as output_file:
	    	for document in documents:
	    		if title == True:
	    			output_file.write(document['title'] + '\n')
	    		output_file.write(document['content'])
