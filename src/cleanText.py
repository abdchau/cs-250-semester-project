import json
import os
import string
import threading
from unidecode import unidecode
from nltk.stem.snowball import EnglishStemmer


def clean(file):
	stemmer = EnglishStemmer()

	with open(file, 'r', encoding="utf8") as f:
		myDict = json.load(f)

	text = myDict['text']

	# remove punctuation from the text, and "simplify" unicode characters
	punc = str.maketrans('', '', string.punctuation)
	dgts = str.maketrans('', '', string.digits)
	tokens = unidecode(text.lower()).replace('-', ' ').translate(punc).translate(dgts).split()
	tokens = [stemmer.stem(token) for token in tokens]

	with open(os.path.join("./data/cleaned/", file[11:-4]+"txt"), "w+") as f:
		f.write("".join(tokens))

clean("./data/raw/blogs_0000001.json")