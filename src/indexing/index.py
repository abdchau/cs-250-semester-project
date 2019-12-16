from tqdm import tqdm
import os
from indexing import lexicon as L
from indexing import forward
from indexing import inverted
from indexing.cleanText import clean
from datetime import datetime
from config import DATA_PATH, DICT_PATH, BARREL_LENGTH


def addFile(dictDir, file, lexicon, barrelLength):

	tokens = clean(file)
	L.processFile(lexicon, L.getNewWordID(lexicon), tokens)

	wordIDs = sorted(set([lexicon[token] for token in tokens]))
	barrels = set([wordID//barrelLength for wordID in wordIDs])

	forwardBarrels, docID = forward.addFile(dictDir, lexicon, tokens, barrels, barrelLength)
	inverted.addFile(dictDir, wordIDs, docID-1, barrels, forwardBarrels)
	L.dump(dictDir, lexicon)


def indexDataset(lexicon):
	# rawDir = "D:/data/717_webhose-2017-03_20170904123310"
	# rawDir = r"..\..\data\raw"
	# rawDir = r"..\..\..\Popular Blog Post Dataset\717_webhose-2017-03_20170904123310"
	# cleanDir = r"..\..\data\cleaned"
	# dictDir = r"..\..\dicts"
	
	print(datetime.now(), "Generating lexicon and forward index")
	
	forwardBarrels = dict()
	wordID = 0
	for docID, file in tqdm(enumerate(os.listdir(DATA_PATH)[1:4])):
		tokens = clean(os.path.join(DATA_PATH, file))

		wordID = L.processFile(lexicon, wordID, tokens)
		forward.processFile(lexicon, forwardBarrels, BARREL_LENGTH, tokens, docID+100000)

	print(datetime.now(), "Writing lexicon and forward index to file")
	L.dump(DICT_PATH, lexicon)
	forward.dump(DICT_PATH, forwardBarrels)

	print(datetime.now(), "Generating inverted index")
	for i, file in enumerate(os.listdir(os.path.join(DICT_PATH,'forward_barrels'))):
		inverted.processFile(DICT_PATH, file, i)

	print(datetime.now(), "Indexing complete")

if __name__ == "__main__":
	main()