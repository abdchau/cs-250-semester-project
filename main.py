import json
import os


inDir = "D:\\Uni\\Semester 3\\DSA\\Project\\Popular Blog Post Dataset\\717_webhose-2017-03_20170904123310"

def main():
	#dicc = 0
	with open(os.path.join(inDir, 'blogs_0000002.json'), 'r', encoding="utf8") as f:
		dicc = json.load(f)

	#print(dicc)
	with open('keys1.txt', 'w') as f:
		for key in dicc:
			f.write(key+"\n")

main()