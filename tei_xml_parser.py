from xml.dom.minidom import parse
import xml.dom.minidom
import os
import json
import codecs


## This scirpt parses every .tei.xml file

## TEI annotations data file


outputfile_path = "/home/jaydeep/599hw2/tei_json"
list_of_authors = "/home/jaydeep/599hw2/list_of_authors"
tei_file_dir = "/media/jaydeep/mySpace/spring2016/599/out/"
#tei_file_dir = "/home/jaydeep/src/grobid/out/"
feed = []
f1 = codecs.open(list_of_authors,"a",encoding='utf8')
with open(outputfile_path, 'w') as feedsjson:
	for i in os.listdir(tei_file_dir):
		# Open XML document using minidom parser
		if i.endswith(".tei.xml"):
			DOMTree = xml.dom.minidom.parse(tei_file_dir+''+i)
			collection = DOMTree.documentElement

			entry = {"authors":[],"publication_year":"","Affiliations":[],"title":""}
			# Get all the movies in the collection
			analytics = collection.getElementsByTagName("analytic")
			analytic = analytics[0]
			authors = analytic.getElementsByTagName("author")

			if len(authors) != 0:
				for author in authors:
	
					if len(author.getElementsByTagName("forename")) != 0:
						firstname = author.getElementsByTagName("forename")[0].childNodes[0].data
					if len(author.getElementsByTagName("surname")) != 0:
						lastname = author.getElementsByTagName("surname")[0].childNodes[0].data
					afflen = author.getElementsByTagName("orgName")
					affiliation = ''
					if len(afflen) != 0:
						for i in range(0,len(afflen)):
							affiliation = affiliation + ',' +author.getElementsByTagName("orgName")[i].childNodes[0].data
			
					name = firstname + " " + lastname
	
					entry["authors"].append(name)
					f1.write(name + "\n")
					entry["Affiliations"].append(affiliation.lstrip(","))
				if len(analytic.getElementsByTagName("title")) != 0:
					topic = analytic.getElementsByTagName("title")[0].childNodes[0].data
					entry["title"] = topic

				imprints = analytic.getElementsByTagName("imprint")
				if len(imprints) != 0:
					imprint = imprints[0]
					dates = imprint.getElementsByTagName("date")
					if len(dates) != 0:
						date = dates[0].getAttribute("when")
						entry["publication_year"] = date

				feed.append(entry)
	json.dump(feed,feedsjson)
	
f1.close()



	
