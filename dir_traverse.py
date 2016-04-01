import os
from shutil import copyfile
import tika
from tika import detector

# Set the directory you want to start from
rootDir = '/media/jaydeep/mySpace/spring2016/599/polarfulldump'

for dirName, subdirList, fileList in os.walk(rootDir):
    
    print('Found directory: %s' % dirName)
    for fname in fileList:
	filetype = detector.from_file(dirName +'/'+ fname)
	if filetype == 'video/mp4':
		copyfile(dirName +'/'+ fname, '/media/jaydeep/mySpace/spring2016/599/polarmp4/'+fname)
	
        print('\t%s' % dirName +'/'+ fname)
	
