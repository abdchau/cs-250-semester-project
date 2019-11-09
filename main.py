import json
import os
import operator
import string
from tqdm import tqdm

inDir = "../Popular Blog Post Dataset/717_webhose-2017-03_20170904123310"

def main():
	
	for file in tqdm(os.listdir(inDir)[:20]):		#run for entire directory to generate complete lexicon
		with open(os.path.join(inDir, file), 'r', encoding="utf8") as f:
			dicc = json.load(f)

		text = dicc['text']

		translator = str.maketrans('', '', string.punctuation)
		text = text.lower().translate(translator).replace('\u201c', "").replace('\u201d', "")
		tokens = text.replace("-", " ").split()

		try:
			with open('lexicon.json', 'r', encoding="utf8") as f:
				lexicon =json.load(f)
			wordID = max(lexicon.items(), key=operator.itemgetter(1))[1] + 1
		except FileNotFoundError:
			lexicon = dict()
			wordID = 0

		#print(wordID)
		#invalidChars = set(string.punctuation)

		for token in tokens:
			
			if not token in lexicon: #not any(char in invalidChars for char in token)
				lexicon[token] = wordID
				wordID+=1

		with open('lexicon.json', 'w') as f:
			json.dump(lexicon, f)

main()