from tqdm import tqdm
import os
import lexicon as L
import forward
import inverted
from cleanText import clean
from datetime import datetime

barrelLength = 500

def main():
	# rawDir = "D:/data/717_webhose-2017-03_20170904123310"
	rawDir = r"..\data\raw"
	# rawDir = r"..\..\Popular Blog Post Dataset\717_webhose-2017-03_20170904123310"
	cleanDir = r"..\data\cleaned"
	dictDir = r"..\dicts"

	print(datetime.now(), "Reading lexicon from file")
	lexicon, wordID = L.load(dictDir)

	os.makedirs(cleanDir, exist_ok=True)

	print(datetime.now(), "Generating lexicon and forward index")
	
	forwardBarrels = dict()
	for docID, file in tqdm(enumerate(os.listdir(os.path.join(rawDir)))):
		tokens = clean(os.path.join(rawDir, file))

		wordID = L.processFile(lexicon, wordID, tokens)
		forward.processFile(lexicon, forwardBarrels, barrelLength, tokens, docID+100000)

	print(datetime.now(), "Writing lexicon and forward index to file")
	L.dump(dictDir, lexicon)
	forward.dump(dictDir, forwardBarrels)

	print(datetime.now(), "Generating inverted index")
	for i, file in enumerate(os.listdir(os.path.join(dictDir,'forward_barrels'))):
		inverted.processFile(dictDir, file, i)

	print(datetime.now(), "Indexing complete")


if __name__ == "__main__":
	main()