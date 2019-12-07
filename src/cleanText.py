import json
import os
import string
from unidecode import unidecode
from nltk.stem.snowball import EnglishStemmer
from nltk.corpus import stopwords

stemmer = EnglishStemmer()
def clean(file, cleanDir):
	"""
	parameters: file - the path to the file that is to be
	cleaned.

	cleanDir - the path to the directory where the cleaned
	files are to be written.

	This function will read a utf-8 encoded file and generate
	an ascii file stripped of digits and punctuation. It
	will also remove stop words.

	return: void
	"""
	with open(file, 'r', encoding="utf8") as f:
		myDict = json.load(f)

	text = myDict['text']

	# remove punctuation from the text, and "simplify" unicode characters
	punc = str.maketrans('', '', string.punctuation)
	dgts = str.maketrans('', '', string.digits)
	tokens = unidecode(text.lower()).replace('-', ' ').translate(punc).translate(dgts).split()

	stopWords = set(stopwords.words('english'))
	tokens = [stemmer.stem(token) for token in tokens if not token in stopWords]

	with open(cleanDir+file[-19:-4]+"txt", "w") as f:
		f.write(" ".join(tokens))