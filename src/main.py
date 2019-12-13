from tqdm import tqdm
import os
import lexicon as L
import forward
import inverted
from cleanText import clean
import json
import datetime

def readLexForward(dictDir):
	try:
		with open(os.path.join(dictDir, 'lexicon.json'), 'r', encoding="utf8") as lexFile:
			lexicon = json.load(lexFile)
		wordID = lexicon[list(lexicon.keys())[-1]] + 1      # get the last wordID in the lexicon,
															# add 1 to get wordID for next addition
	except FileNotFoundError:
		lexicon = dict()
		wordID = 0

	# try:
	# 	with open(os.path.join(dictDir, 'forward.json'), 'r', encoding="utf8") as forwardFile:
	# 		forwardIndex = json.load(forwardFile)
	# except FileNotFoundError:
	# 	forwardIndex = dict()

	return lexicon, wordID


def main():
	# rawDir = "D:/data/717_webhose-2017-03_20170904123310"
	rawDir = r"..\data\raw"
	# rawDir = r"..\..\Popular Blog Post Dataset\717_webhose-2017-03_20170904123310"
	cleanDir = r"..\data\cleaned"
	dictDir = r"..\dicts"

	print(datetime.datetime.now(), "Reading lexicon and forward index from file")
	lexicon, wordID = readLexForward(dictDir)
	forwardIndex = []

	if not os.path.exists(cleanDir):
		os.makedirs(cleanDir)

	print(datetime.datetime.now(), "Generating lexicon and forward index")
	forwardBarrel = -1
	for docID, file in tqdm(enumerate(os.listdir(os.path.join(rawDir)))):
		tokens = clean(os.path.join(rawDir, file))

		if docID % 4 == 0:
			forwardBarrel+=1
			forwardIndex.append(dict())

		wordID = L.processFile(lexicon, wordID, tokens)
		forward.processFile(lexicon, forwardIndex[forwardBarrel], tokens, docID+100000)

	print(datetime.datetime.now(), "Writing lexicon and forward index to file")
	L.dump(dictDir, lexicon)
	forward.dump(dictDir, forwardIndex)

	# inverted.generateInvertedIndex(dictDir)

if __name__ == "__main__":
	main()