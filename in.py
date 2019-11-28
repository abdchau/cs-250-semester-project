import json
import os
import string
from tqdm import tqdm

path = 'D:/cs-250-semester-project/forward.json'
def Remove(list1,list2): 
    final_list = [] 
    for num in list1: 
        if num not in list2: 
            final_list.append(num) 
    return final_list

def main1():
	wordids = []
	inverted = dict()

	with open(path, 'r', encoding="utf8") as findex:
		forward = json.load(findex)
	docids = list(forward.keys())		#get all docIds from forward index in a list
	for doc in tqdm(docids):
		wordids += Remove(list(forward[doc]),wordids)	#get all wordids without repition of wordsid
	for id in tqdm(wordids):
		indoc = dict()

		for doc in docids:

			if(forward[doc].get(id) == None):	#check if wordid exists in the subdictionary of docid
				continue						#go to next subdictionary if wordid is not present

			indoc[doc] = forward[doc][id]		#get hits and position from subdictionary and store it in new dictionary with docid as key and hits and position as value
		inverted[id] = indoc				#store the subdictionary in another dictionary with wordid as key

	with open("inverted.json",'w',encoding = "utf8") as docfile:     	#writing the dict into file
		json.dump(inverted,docfile)	
main1()