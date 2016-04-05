import subprocess
import codecs
import time
import json
import os

mp4_file_path = "/media/jaydeep/mySpace/spring2016/599/polarmp4/"
tempfile_path = "/home/jaydeep/"
#count = 0
mp4info_json = []
f2 = codecs.open("/home/jaydeep/599hw2/599-2/extracredit2/mp4jsoninfo.json", "w","utf-8")
for f in os.listdir(mp4_file_path):
	try:
		#if count >10:
		#	break
		command = "./exiftool " + mp4_file_path + f
		result = subprocess.check_output(command, shell=True)
		f1 = codecs.open(tempfile_path + "extractmp4temp", "w","utf-8")
		f1.write(result)
		f1.close()
		#count += 1

		f1 = open(tempfile_path + "extractmp4temp", "r")
		entry = {}
		for line in f1:
			splitline = line.split(':')
			key = splitline[0].rstrip(' ').lstrip(' ')
			value = splitline[1].lstrip(' ').rstrip('\n').rstrip(' ')
			entry[key] = value
		mp4info_json.append(entry)
			
		f1.close()
		
		
	except:
		continue


json.dump(mp4info_json,f2)
f2.close()
