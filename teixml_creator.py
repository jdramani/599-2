import json
from pprint import pprint
import os
import subprocess
import codecs


## This scirpt generates .tei.xml file for every pdf file in specified directory

pdf_file_dir = "/media/jaydeep/mySpace/spring2016/599/papers/"
teidotxml_file_dir = "/media/jaydeep/mySpace/spring2016/599/out/"
temp_file_path = "/home/jaydeep/"
for i in os.listdir(pdf_file_dir):
	try:
		file_path = pdf_file_dir + "" + i
		command = "java -classpath /home/jaydeep/src/grobidparser-resources/:/home/jaydeep/tika-1.12/tika-app/target/tika-app-1.12.jar org.apache.tika.cli.TikaCLI --config=/home/jaydeep/src/grobidparser-resources/tika-config.xml -J "+ file_path

		json_result = subprocess.check_output(command, shell=True)
		f = open(temp_file_path + "dump.json","w")
		f.write(json_result)
		f.close()

		with open(temp_file_path + "dump.json") as data_file:    
			data = json.load(data_file)
	

		if "grobid:header_TEIXMLSource" in data[0]:
			f = codecs.open(teidotxml_file_dir + i + ".tei.xml", 'w', encoding='utf8')
			f.write(data[0]["grobid:header_TEIXMLSource"])
			f.close()
	except:
		continue

	

	
