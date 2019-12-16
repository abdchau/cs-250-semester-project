import os
from indexing import index
from indexing.lexicon import load
from config import *

lexicon, wordID = load(DICT_PATH)
index.indexDataset(lexicon)
index.addFile(DICT_PATH, os.path.join(DATA_PATH, os.listdir(DATA_PATH)[4]), lexicon, BARREL_LENGTH)
