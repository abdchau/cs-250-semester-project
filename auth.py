import json
import os
import string
from tqdm import tqdm
import collections

#inDir = "D:/data/717_webhose-2017-03_20170904123310"
inDir = "D:/Uni/Semester 3/DSA/Project/Popular Blog Post Dataset/717_webhose-2017-03_20170904123310"

def getIndexPositions(listOfElements, element):
    ''' Returns the indexes of all occurrences of give element in
    the list- listOfElements '''
    indexPosList = []
    indexPos = 0
    while True:
        try:
            # Search for item in list from indexPos to the end of list
            indexPos = listOfElements.index(element, indexPos)
            # Add the index position in list
            indexPosList.append(indexPos)
            indexPos += 1
        except ValueError as e:
            break
 
    return indexPosList

def main1():

	docrepos = dict()
	with open('lexicon.json', 'r', encoding="utf8") as lexfile:
		lexicon = json.load(lexfile)
	wordID = lexicon[list(lexicon.keys())[-1]] + 1		# get the last wordID in the lexicon,            															# add 1 to get wordID for next addition
		
	for file in tqdm(os.listdir(inDir)[1:3]):		# run for 3 files to generate doc id with words and hits
		position = dict()
		docId = inDir[-3:] + file[-11:-5]               #unique docID for every blog
		with open(os.path.join(inDir,file),'r',encoding='utf8') as f:
			mydict = json.load(f)

		text = mydict['text']

                # remove punctuation from the text. Some hardcoding for Unicode characters
		translator = str.maketrans('', '', string.punctuation)
		text = text.lower().replace("-", " ").replace('\u201c', "").replace('\u201d', "").translate(translator)
		tokens = text.replace('\u2018', "").replace('\u2019', "").split()
		
		for i in range(len(tokens)):
			tokens[i] = lexicon[tokens[i]]	          #convert words to their respective wordId
		for i in range(len(tokens)):	
			indexposition = getIndexPositions(tokens,tokens[i])
			indexposition.insert(0,len(indexposition))
			position[tokens[i]] = indexposition
		docrepos[docId] = position	
	with open("doc2.json",'w',encoding = "utf8") as docfile:     
		json.dump(docrepos,docfile)
main1()