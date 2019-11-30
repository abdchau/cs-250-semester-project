import json
import os
import string
from tqdm import tqdm
import threading
from unidecode import unidecode
from nltk.stem.snowball import EnglishStemmer


stemmer = EnglishStemmer()
# if a lexicon already exists, load it. Otherwise create new lexicon
try:
	with open('../dicts/lexicon.json', 'r', encoding="utf8") as lexfile:
		lexicon = json.load(lexfile)
	wordID = lexicon[list(lexicon.keys())[-1]] + 1      # get the last wordID in the lexicon,
														# add 1 to get wordID for next addition
except FileNotFoundError:
	lexicon = dict()
	wordID = 0

def processFile(file):
	with open(file, 'r') as f:
		tokens = f.read()

	tokens = tokens.split()

	# remove punctuation from the text, and "simplify" unicode characters
	# punc = str.maketrans('', '', string.punctuation)
	# dgts = str.maketrans('', '', string.digits)
	# tokens = unidecode(text.lower()).replace('-', ' ').translate(punc).translate(dgts).split()
	# tokens = [stemmer.stem(token) for token in tokens]

	global lexicon, wordID
	for token in tokens:
		id = lexicon.get(token)             # id is set to None of token doesnt exist
		if id == None:                      # if the word is not already present in lexicon, add it
			lexicon[token] = wordID
			wordID+=1

def generateLexicon(cleanDir):

	for file in tqdm(os.listdir(cleanDir)):
		processFile(os.path.join(cleanDir, file))

	global lexicon
	with open('../dicts/lexicon.json', 'w', encoding="utf8") as lexfile:     # write the dictionary to at the end
		json.dump(lexicon, lexfile, indent=2)