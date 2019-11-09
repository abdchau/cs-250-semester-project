import json
import os
import operator
import string

inDir = "..\\Popular Blog Post Dataset\\717_webhose-2017-03_20170904123310"

def main():
	#dicc = 0
	with open(os.path.join(inDir, 'blogs_0000001.json'), 'r', encoding="utf8") as f:
		dicc = json.load(f)

	text = dicc['text']
	tokens = text.split()


	try:
		with open('lexicon.json', 'r', encoding="utf8") as f:
			lexicon =json.load(f)
		wordID = max(lexicon.items(), key=operator.itemgetter(1))[1] + 1
	except FileNotFoundError:
		lexicon = dict()
		wordID = 0

	print(wordID)
	invalidChars = set(string.punctuation)

	for token in tokens:
		token = token.lower().translate(string.punctuation)
		if not (token in lexicon): #not any(char in invalidChars for char in token)
			lexicon[token] = wordID
			wordID+=1

	with open('lexicon.json', 'w') as f:
		json.dump(lexicon, f)

main()