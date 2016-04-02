


## For each entry of author_list call google scholar api and save title, url link and year

import subprocess
import codecs
import time
import json

author_list_path = "/home/jaydeep/599hw2/authors.txt"
tempfile_path = "/home/jaydeep/"
f = open(author_list_path,"r")
related_pubs = {'name':'Authors','children':[]}
fjson = open("/home/jaydeep/599hw2/related_pubs.json","w")
count = 0
for line in f:
	try:
		if count > 1000:
			break
		count += 1
		line = line.rstrip("\n")
		command = "scholar.py -c 20 --author "+ line +" --csv"
		result = subprocess.check_output(command, shell=True)
		f1 = codecs.open(tempfile_path + "related20pubs.csv", "w","utf-8")
		f1.write(result)
		f1.close()
		f1 = open(tempfile_path + "related20pubs.csv","r")
		entry = {'name':line,'children':[]}
		for pub in f1:
			subentry = {"title":"","url":"","year":""}
			pub = pub.split("|")
			subentry["title"] = pub[0]
			subentry["url"] = pub[1]
			subentry["year"] = pub[2]
			entry['children'].append(subentry)

		related_pubs['children'].append(entry)
	#break
	except:
		continue
	time.sleep(10)
	break	
json.dump(related_pubs,fjson)		

fjson.close()
f.close()
