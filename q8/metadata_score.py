import os

import tika
from tika import parser

tika.initVM()


def get_metadata_score(metadata):
    score = 0
    for field in metadata.keys():
        field = field.lower()
        if "description" in field:
            score += 1 / 3
        if "title" in field or "name" in field:
            score += 1 / 3
        if "version" in field or "created" in field or "date" in field:
            score += 1 / 3
        if "identifier" in field or "doi" in field:
            score += 1
        if "source" in field:
            score += 0.5
        if "type" in field:
            score += 1
        score += (len(metadata) - 2) / 5
        if "rights" in field:
            score += 1
    return score


# data folder path
path = "/Users/minhpham/data-classified"
with open("result.csv", "a") as f:
    f.write("Name,Score\n")
    for folder_name in os.listdir(path):
        if ".DS_Store" in folder_name:
            continue
        folder_path = os.path.join(path, folder_name)
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)

            parsed = parser.from_file(file_path)
            if 'metadata' in parsed:
                f.write(",".join([file_name, str(get_metadata_score(parsed['metadata']))]) + "\n")
