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
import itertools

from SolrClient import SolrClient

from vector import Vector


def computeScores1(type, query, output_file):
    solr = SolrClient('http://localhost:8983/solr')

    res = solr.query(query['index'], {
        'q': '*:*',
        'wt': 'json',
        'indent': True,
        'rows': 1000,
    })

    docs = res.data['response']['docs']

    with open(output_file, "wb") as outF:
        a = csv.writer(outF, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        a.writerow(["type", "x-coordinate", "y-coordinate", "Similarity_score"])

        for doc in docs:
            for key in doc:
                if key in ["id", "_version_"]:
                    continue
                try:
                    doc[key] = doc[key][0].encode("ascii", "ignore")
                except:
                    doc[key] = str(doc[key][0]).decode("unicode_escape").encode("ascii", "ignore")

        doc_tuples = itertools.combinations(docs, 2)
        for raw1, raw2 in doc_tuples:

            doc1 = raw1.copy()
            doc2 = raw2.copy()

            if "Name" in doc1:
                row_cosine_distance = [type, doc1["Name"], doc2["Name"]]
            else:
                row_cosine_distance = [type, doc1["name"], doc2["name"]]

            v1 = Vector(row_cosine_distance[0], doc1)
            v2 = Vector(row_cosine_distance[1], doc2)

            row_cosine_distance.append(v1.cosTheta(v2))

            a.writerow(row_cosine_distance)


if __name__ == "__main__":
    index = "polar_geo"
    output_file = "result_geo.csv"
    computeScores1({"index": index}, output_file)
