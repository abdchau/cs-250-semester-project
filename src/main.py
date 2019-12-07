from tqdm import tqdm
import os
from lexicon import generateLexicon
from forward import generateForwardIndex
from inverted import generateInvertedIndex
from cleanText import clean


def main():
	# rawDir = "D:/data/717_webhose-2017-03_20170904123310"
	rawDir = r"..\data\raw"
	# rawDir = r"..\..\Popular Blog Post Dataset\717_webhose-2017-03_20170904123310"
	cleanDir = r"..\data\cleaned"
	dictDir = r"..\dicts"

	if not os.path.exists(cleanDir):
		os.makedirs(cleanDir)

	for file in os.listdir(os.path.join(rawDir)):
		clean(os.path.join(rawDir, file), cleanDir)

	generateLexicon(cleanDir, dictDir)
	generateForwardIndex(cleanDir, dictDir)
	generateInvertedIndex(dictDir)

main()