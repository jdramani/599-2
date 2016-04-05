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

import editdistance
from SolrClient import SolrClient


def stringify(attribute_value):
    if isinstance(attribute_value, list):
        attribute_value = [str(val) for val in attribute_value]
        try:
            return str((", ".join(attribute_value)).encode('utf-8').strip())
        except:
            return str(", ".join(attribute_value)).strip()
    else:
        try:
            return str(attribute_value.encode('utf-8').strip())
        except:
            return str(attribute_value)


def computeScores2(type, query, output_file, is_all_key):
    na_metadata = ["id", "_version_", "Name", "name"]

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
                row_edit_distance = [type, doc1["Name"], doc2["Name"]]
            else:
                row_edit_distance = [type, doc1["name"], doc2["name"]]

            intersect_features = set(doc1.keys()) & set(doc2.keys())
            intersect_features = [feature for feature in intersect_features if feature not in na_metadata]

            file_edit_distance = 0.0
            for feature in intersect_features:

                file1_feature_value = stringify(doc1[feature])
                file2_feature_value = stringify(doc2[feature])

                if len(file1_feature_value) == 0 and len(file2_feature_value) == 0:
                    feature_distance = 0.0
                else:
                    feature_distance = float(editdistance.eval(file1_feature_value, file2_feature_value)) / (
                        len(file1_feature_value) if len(file1_feature_value) > len(file2_feature_value) else len(
                            file2_feature_value))

                file_edit_distance += feature_distance

            if is_all_key:
                file1_only_features = set(doc1.keys()) - set(intersect_features)
                file1_only_features = [feature for feature in file1_only_features if feature not in na_metadata]

                file2_only_features = set(doc2.keys()) - set(intersect_features)
                file2_only_features = [feature for feature in file2_only_features if feature not in na_metadata]

                file_edit_distance += len(file1_only_features) + len(
                    file2_only_features)  # increment by 1 for each disjunct feature in (A-B) & (B-A), file1_disjunct_feature_value/file1_disjunct_feature_value = 1
                file_edit_distance /= float(
                    len(intersect_features) + len(file1_only_features) + len(file2_only_features))

            else:
                file_edit_distance /= float(len(intersect_features))  # average edit distance

            row_edit_distance.append(1 - file_edit_distance)
            a.writerow(row_edit_distance)


if __name__ == "__main__":
    index = "polar"
    output_file = "result_measurement.csv"
    computeScores2({"index": index}, output_file, is_all_key=False)
