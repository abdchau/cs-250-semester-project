import os
import json


DATA_PATH = "../data/raw"
DICT_PATH = "../dicts"
BARREL_LENGTH = 500
docID_ = [100000]

try:
	with open(os.path.join(DICT_PATH, 'indexed_docs.json'), 'r', encoding="utf8") as f:
		indexedDocs = json.load(f)
except FileNotFoundError:
	indexedDocs = dict()

try:
	with open(os.path.join(DICT_PATH, 'metadata.json'), 'r', encoding="utf8") as f:
		metadata = json.load(f)
except FileNotFoundError:
	metadata = dict()


