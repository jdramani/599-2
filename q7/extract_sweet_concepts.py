import json




def extract_sweet_concepts(sweet_file, ner_file):
    with open(sweet_file, 'r') as f:
        full_text = f.read()
    concepts = [c.strip() for c in full_text.split(",")]
    entities = []
    with open(ner_file, 'r') as f:
        for line in f.readlines():
            if "NER" in line:
                content = line.split(":")[1].strip()
                for s in content.split(","):
                    s = s.strip()
                    for c in concepts:
                        if c and c in s:
                            entities.append({"Name": c, "Concept": c})
    with open("ner.json", 'w') as f:
        json.dump(entities, f)


if __name__ == "__main__":
    extract_sweet_concepts("ontology.txt", "result.txt")
