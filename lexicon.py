import json
import os
import string
from tqdm import tqdm
import threading
from unidecode import unidecode
from nltk.stem.snowball import EnglishStemmer

inDir = "D:/data/717_webhose-2017-03_20170904123310"
#inDir = "D:/Uni/Semester 3/DSA/Project/Popular Blog Post Dataset/717_webhose-2017-03_20170904123310"

def lexicon():
	# if a lexicon already exists, load it. Otherwise create new lexicon
	try:
		with open('lexicon.json', 'r', encoding="utf8") as lexfile:
			lexicon = json.load(lexfile)
		wordID = lexicon[list(lexicon.keys())[-1]] + 1		# get the last wordID in the lexicon,
	except FileNotFoundError:
		lexicon = dict()
		wordID = 0            															# add 1 to get wordID for next addition
	
	stemmer = EnglishStemmer()
	for file in tqdm(os.listdir(inDir)[:100]):		# run for entire directory to generate complete lexicon
		with open(os.path.join(inDir, file), 'r', encoding="utf8") as f:
			myDict = json.load(f)

		text = myDict['text']

		# remove punctuation from the text, and "simplify" unicode characters
		punc = str.maketrans('', '', string.punctuation)
		dgts = str.maketrans('', '', string.digits)
		tokens = unidecode(text.lower()).replace('-', ' ').translate(punc).translate(dgts).split()
		tokens = [stemmer.stem(token) for token in tokens]
		
		for token in tokens:
			id = lexicon.get(token)             #id is set to None of token doesnt exist
			if id == None: 	# if the word is not already present in lexicon, add it
				lexicon[token] = wordID
				wordID+=1

	with open('lexicon.json', 'w', encoding="utf8") as lexfile:     # write the dictionary to at the end
		json.dump(lexicon, lexfile, indent=2)

lexicon()