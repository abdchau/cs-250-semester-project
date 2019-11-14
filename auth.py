import json
import os
import string
from tqdm import tqdm
import collections

inDir = "D:/data/717_webhose-2017-03_20170904123310"

def main1():

	try:
		with open('D:/cs-250-semester-project/author.json', 'r', encoding="utf8") as lexfile:
			lexicon = json.load(lexfile)
	except FileNotFoundError:
		lexicon = dict()
		  		# get the last wordID in the lexicon,            															# add 1 to get wordID for next addition
		
	for file in tqdm(os.listdir(inDir)[:10]):		# run for 3 files to generate doc id with words and hits
		docId = inDir[-3:] + file[-11:-5]               #unique docID for every blog
		with open(os.path.join(inDir,file),'r',encoding='utf8') as f:
			mydict = json.load(f)

		text = mydict['author']
		id = lexicon.get(docId)             #id is set to None of token doesnt exist
		if id == None: 	# if the word is not already present in lexicon, add it
			lexicon[docId] = text
	with open("author.json",'w',encoding = "utf8") as docfile:     
		json.dump(lexicon,docfile)
main1()