This File contains instructions on how to run script and information about which script does what for relevant questions.


Question :3

Tag ratios and NER
-> For each file, we first ran the Tag ratios algorithm and found out the lines which could contain any measurement data. 
-> Then using those results, we read those   lines and using the OpenNLP NER and extracted the relevant measurement data that was present in those files. 
-> We were able to run this for approximately 500,000 files. 
-> To run the program, we need to point to the correct path where the files are stored. Also, the proper path to the ner.bin files need to be given. 
-> The output of this program is a CSV file with the format (filename, measurement_data).

Question :4

DOI Content Handler
-> We used yourls, which is a URL shortner library, to generate shortened URLs for each file. 
-> Once the proper setup for the yourls API was set up, it was quite easy to generate the shortened URLS.
-> We read each file and sent the details to the yourls API which returned the shortened URL.


Question :5

-> teixml_creator.py script creates .tei.xml file from pdf files.
-> From the above .tei.xml file we extract the TEI metadata using tei_xml_parser.py
-> We had to separate this part as there is memory leak error in the GROBID Journal parser library if we run it in batch mode.
-> tei_xml_parser outputs tei_json file which contians TEI Meatdata and list_of_authors.
-> Then we removed duplicates and noice (There were some entries which are not human names) from list_of_authors and formed authors.txt
-> Then Google_scholar.py goes through each and every author in authors.txt file and generates json file of author and his/her 20 related publications.

Question :6

-> textfromany.java program extracts text from pdf,html,text,xhtml files and then runs geo topic parser on it.
-> The output of the above file gives json of latitude,longitude and location name.

Question 7:
- Extract SWEET ontology into a folder named ontology
- Run SweetConceptExtractor.java to extract the concepts and categories from the ontology files
- Run tika-server with instructions from https://wiki.apache.org/tika/TikaJAXRS.
- Run tika-ner bash script to extract named entity from the data (modify path to data in the script).
- Run extract_sweet_concepts.py to get the intersection betweens these two sets of data.

Question 8:
- Modify path to data in metascorer.py script.
- Run metascorer.py script.

Question 9:
- Locate solr root folder.
- Run bin/solr create -c core_name to create a new index core
- Run bin/solr -c core_name path_to_data_file (data files can be either csv or json files)
- Index csv and json result files from different questions to Solr
	+ For measurement data, use polar as core name
	+ For location data, use polar_geo as core name
	+ For scholar data, use polar_scholar as core name
	+ For sweet data, use polar_sweet as core name
	+ For metadata score, use polar_score as core name
	+ For extra_credit part, use polar_extra as core name
	+ For storing tika-similarity clusters structure, use polar_similarity as core name


Question :10

Memex GeoParser
-> Using the data from the GeoTopic parser, we indexed the data into solr. 
-> Then we ran the Memex GeoParser on the index and generated the location map.

Question 11:
- Install tika-similarity as instructed from https://github.com/chrismattmann/tika-similarity/.
- Replace the python files in tika-similarity with our python files.
- Run clustering_script.py to generate the d3 files.
- Run indexer.py to flatten nested structures in d3 json files and index it into solr

Question :14 (Extra credit part 2)

-> We chose the Exiftool-10.13 content extraction tool for media files.
-> extractmp4info.py script runs on every media file and outputs json with every file's metadata featues.


