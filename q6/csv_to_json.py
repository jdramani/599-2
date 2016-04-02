f = open('geo_parser_op.csv','r')
import json
places = []

for line in f:
	entry = {'name':'','location':{'latitude':0,'longitude':0}}
	line = line.rstrip('\n').split(',')
	entry['name'] = line[2]
	entry['location']['latitude'] = float(line[0])
	entry['location']['longitude'] = float(line[1])
	places.append(entry) 

f.close()

f = open('geo_parser_op.json','w')

json.dump(places,f)
f.close()
