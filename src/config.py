import os
import json


DATA_PATH = "../data/raw"
DICT_PATH = "../dicts"
BARREL_LENGTH = 500

try:
	with open(os.path.join(DICT_PATH, 'indexed_docs.json'), 'r', encoding="utf8") as f:
		indexedDocs = json.load(f)
except FileNotFoundError:
	indexedDocs = dict()

