# -*- coding: utf8 -*-
import json
from multiprocessing import Pool
from namuwiki.extractor import extract_text
import argparse
import contextlib # for python 2
import codecs # for python2

parser = argparse.ArgumentParser()

parser.add_argument('-i', '--input', required = True, help = 'input_filename')
parser.add_argument('-o', '--output', required = True, help = 'output_filename')
parser.add_argument('-m', '--multiprocess', action = 'store_true', help = 'run mutiprocessing')
parser.add_argument('-t', '--title', action = 'store_true', help = 'include title of documents')

args = parser.parse_args()

json_file = args.input
output_filename = args.output
multiprocess  = args.multiprocess
extract_title = args.title

# Simple Usage
if multiprocess == False:
	with open(json_file, 'r') as json_file:
		namu_wiki = json.load(json_file)

	with open(output_filename, 'w') as output_file:
		for document in namu_wiki:
			# Extract Title	if specified
			if extract_title == True:
				title = document['title'].encode('utf-8') + '\n'
				output_file.write(title)
			# Extract Content
			content = extract_text(document['text']).encode('utf-8')
			output_file.write(content)

# Multiprocessing Usage
else:
	def work(document):
		return {
			'title': document['title'],
			'content': extract_text(document['text'])
		}

	try:
	# Python 3
		with open(json_file, 'r', encoding='utf-8') as json_file:
			namu_wiki = json.load(json_file)
		with Pool() as pool:
			documents = pool.map(work, namu_wiki)
			with open(output_filename, 'w') as output_file:
				for document in documents:
				# Extract Title	if specified
					if extract_title == True:
						title = document['title'] + '\n'
					output_file.write(title)
				# Extract Content
					content = document['content']
					output_file.write(content)
	except:
	# Python 2
		with codecs.open(json_file, 'r', encoding='utf-8') as json_file:
			namu_wiki = json.load(json_file)
		with contextlib.closing(Pool()) as pool:
			documents = pool.map(work, namu_wiki)
			with codecs.open(output_filename, 'w', encoding='utf-8') as output_file:
				for document in documents:
				# Extract Title	if specified
					if extract_title == True:
						title = document['title'] + '\n'
					output_file.write(title)
				# Extract Content
					content = document['content']
					output_file.write(content)
		
