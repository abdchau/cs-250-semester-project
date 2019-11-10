import json
import os
import string
from tqdm import tqdm
import collections

inDir = "D:/data/717_webhose-2017-03_20170904123310"

def main1():

	docrepos = dict()
	with open('lexicon.json', 'r', encoding="utf8") as lexfile:
		lexicon = json.load(lexfile)
	wordID = lexicon[list(lexicon.keys())[-1]] + 1		# get the last wordID in the lexicon,            															# add 1 to get wordID for next addition
		
	for file in tqdm(os.listdir(inDir)[:3]):		# run for 3 files to generate doc id with words and hits
		docId = inDir[-3:] + file[-11:-5]               #unique docID for every blog
		print(docId)
		with open(os.path.join(inDir,file),'r',encoding='utf8') as f:
			mydict = json.load(f)

		text = mydict['text']

                # remove punctuation from the text. Some hardcoding for Unicode characters
		translator = str.maketrans('', '', string.punctuation)
		text = text.lower().replace("-", " ").replace('\u201c', "").replace('\u201d', "").translate(translator)
		tokens = text.replace('\u2018', "").replace('\u2019', "").split()
		
		for i in range(len(tokens)):
			tokens[i] = lexicon[tokens[i]]          #convert words to their respective wordId
			hits=collections.Counter(tokens)        #recording hits of distinct word id and storing it in list
		docrepos[docId] = hits                          #inserting hit list to docID key in dictionary
		
	with open("doc.json",'w',encoding = "utf8") as docfile:     
		json.dump(docrepos,docfile)
main1()
