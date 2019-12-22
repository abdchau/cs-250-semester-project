import os
import json


# DATA_PATH = "D:/Uni/Semester 3/DSA/Project/Popular Blog Post Dataset"
DATA_PATH = "../data"
DICT_PATH = "../dicts"
INITIAL_BARREL_LENGTH = 100

try:
	with open(os.path.join(DICT_PATH, 'indexed_docs.json'), 'r', encoding="utf8") as f:
		indexedDocs = json.load(f)
except FileNotFoundError:
	indexedDocs = dict()

