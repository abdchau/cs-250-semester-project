import json
import os
import string
from unidecode import unidecode
from nltk.stem.snowball import EnglishStemmer
from nltk.corpus import stopwords

stemmer = EnglishStemmer()
stopWords = set(stopwords.words('english'))
punc = str.maketrans('', '', string.punctuation)
dgts = str.maketrans('', '', string.digits)

def clean(text):
	"""
	arguments:
		- file: the path to the file that is to be cleaned.

	This function will read a utf-8 encoded file and generate
	a list of words stripped of digits and punctuation. It
	will also remove stop words.

	return: list of 'cleaned' words from file
	"""

	# remove punctuation from the text, "simplify" unicode characters
	tokens = unidecode(text.lower()).replace('-', ' ').translate(punc).translate(dgts).split()

	# stem and remove stop words
	tokens = [stemmer.stem(token) for token in tokens if not token in stopWords]

	return tokens

def readFile(file):
	with open(file, 'r', encoding="utf8") as f:
		myDict = json.load(f)

	return myDict['author'], myDict['title'], myDict['text'], myDict['url'], myDict['published'], len(myDict['text'])