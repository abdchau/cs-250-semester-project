import json
import os
import string
from tqdm import tqdm

inDir = "../Popular Blog Post Dataset/717_webhose-2017-03_20170904123310"

def main():
	
	for file in tqdm(os.listdir(inDir)[:20]):		# run for entire directory to generate complete lexicon
		with open(os.path.join(inDir, file), 'r', encoding="utf8") as f:
			myDict = json.load(f)

		text = myDict['text']

		# remove punctuation from the text. Some hardcoding for Unicode characters
		translator = str.maketrans('', '', string.punctuation)
		text = text.lower().replace("-", " ").replace('\u201c', "").replace('\u201d', "").translate(translator)
		tokens = text.replace('\u2018', "").replace('\u2019', "").split()

		# if a lexicon already exists, load it. Otherwise create new lexicon
		try:
			with open('lexicon.json', 'r', encoding="utf8") as f:
				lexicon = json.load(f)
			wordID = lexicon[list(lexicon.keys())[-1]] + 1		# get the last wordID in the lexicon,
																# add 1 to get wordID for next addition
		except FileNotFoundError:
			lexicon = dict()
			wordID = 0

		for token in tokens:
			if not token in lexicon: 	# if the word is not already present in lexicon, add it
				lexicon[token] = wordID
				wordID+=1

		with open('lexicon.json', 'w') as f:
			json.dump(lexicon, f)

main()