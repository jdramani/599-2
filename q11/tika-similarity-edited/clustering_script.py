import os

from cosine_similarity import computeScores1
from edit_value_similarity import computeScores2
from indexer import index_from_json

index = "polar_geo"
output_file = "result_geo.csv"
computeScores1("geo", {"index": index}, output_file)

index = "polar"
output_file = "result_measurement.csv"
computeScores2("measurement", {"index": index}, output_file, is_all_key=False)

index = "polar_sweet"
output_file = "result_sweet.csv"
computeScores2("sweet", {"index": index}, output_file, is_all_key=False)

index = "polar_scholar"
output_file = "result_scholar.csv"
computeScores2("sweet", {"index": index}, output_file, is_all_key=False)

os.system("python edit-cosine-circle-packing.py result_measurement.csv circle_ms.json")
os.system("python edit-cosine-circle-packing.py result_geo.csv circle_geo.json")

os.system("python edit-cosine-circle-packing.py result_sweet.csv cirlce_sweet.json")
os.system("python edit-cosine-circle-packing.py result_scholar.csv circle_scholar.json")

