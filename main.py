import json
import os
import string
from tqdm import tqdm

inDir = "C:/Users/mahaasghar/Documents/DSA Project/717_20170904123036/file 1"

def main():
  #open lexicon file to load data only once
	try:
		with open('lexicon.json', 'r', encoding="utf8") as lexfile:
			lexicon = json.load(lexfile)
		wordID = lexicon[list(lexicon.keys())[-1]] + 1		# get the last wordID in the lexicon,
	except FileNotFoundError:
		lexicon = dict()
		wordID = 0            															# add 1 to get wordID for next addition
		
	for file in tqdm(os.listdir(inDir)[:30000]):		# run for entire directory to generate complete lexicon
		with open(os.path.join(inDir, file), 'r', encoding="utf8") as f:
			myDict = json.load(f)

		text = myDict['text']

		# remove punctuation from the text. Some hardcoding for Unicode characters
		translator = str.maketrans('', '', string.punctuation)
		text = text.lower().replace("-", " ").replace('\u201c', "").replace('\u201d', "").translate(translator)
		tokens = text.replace('\u2018', "").replace('\u2019', "").split()

		# if a lexicon already exists, load it. Otherwise create new lexicon
		
		for token in tokens:
			id = lexicon.get(token)             #id is set to None of token doesnt exist
			if id == None: 	# if the word is not already present in lexicon, add it
				lexicon[token] = wordID
				wordID+=1
		#print("good scene")
	with open('lexicon.json', 'w', encoding="utf8") as lexfile:     #write the dictionary to at the end
		json.dump(lexicon, lexfile)

main()