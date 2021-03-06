#!/usr/bin/env python2.7
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#


import csv
import json
import sys

row = []
csvPath = sys.argv[1]  # Input Path to csv file
with open(csvPath, "r") as f:
    lines = csv.reader(f, delimiter=',', quotechar='"')
    for line in lines:
        row.append(line)

data = {}

for i in range(len(row)):
    print row[i]
    if "x-coordinate" in row[i][1]:
        continue
    else:
        second = {"name": row[i][1] + "  " + row[i][2], "size": row[i][3]}
        if row[i][1] not in data:
            data[row[i][1]] = [second]
        else:
            data[row[i][1]].append(second)

clusterList = []
i = 0
for elem in data.keys():
    first = {"name": "cluster " + str(i), "children": data[elem]}
    clusterList.append(first)
    i += 1

print json.dumps(clusterList, sort_keys=True, indent=4, separators=(',', ': '))

clusterStruct = {"name": "clusters", "children": clusterList}
with open(sys.argv[2], "w") as f:  # Pass the json file as input to circle-packing.html
    f.write(json.dumps(clusterStruct, sort_keys=True, indent=4, separators=(',', ': ')))
