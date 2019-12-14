from tqdm import tqdm
import os
import lexicon as L
import forward
import inverted
from cleanText import clean
import json
from datetime import datetime

barrelLength = 500

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

	print(datetime.now(), "Reading lexicon and forward index from file")
	lexicon, wordID = readLexForward(dictDir)

	os.makedirs(cleanDir, exist_ok=True)

	print(datetime.now(), "Generating lexicon and forward index")
	
	forwardBarrels = dict()
	for docID, file in enumerate(os.listdir(os.path.join(rawDir))):
		tokens = clean(os.path.join(rawDir, file))


		wordID = L.processFile(lexicon, wordID, tokens)
		forward.processFile(lexicon, forwardBarrels, barrelLength, tokens, docID+100000)

	print(datetime.now(), "Writing lexicon and forward index to file")
	L.dump(dictDir, lexicon)
	forward.dump(dictDir, forwardBarrels)

	for i, file in enumerate(os.listdir(os.path.join(dictDir,'forward_barrels'))):
		inverted.processFile(dictDir, file, i, barrelLength)
	# inverted.generateInvertedIndex(dictDir)

if __name__ == "__main__":
	main()