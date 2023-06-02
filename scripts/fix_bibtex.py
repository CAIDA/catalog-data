#!  /usr/bin/env python3
import yaml
import os, warnings

# Match invalid bibtex types to valid types
bibtex_normalize = {
    "PhD thesis": "phdthesis",
    "patent": "misc",
    "thesis": "phdthesis",
    "tech report": "techreport",
    "online": "misc",
    "tech_report": "techreport",
    "class report": "misc",
    "presentation": "misc",
    "MSc thesis": "mastersthesis",
    "in_joural": "article",
    "in_proceedings": "inproceedings",
    "BA thesis": "misc",
    "BSc thesis": "misc",
    "MS thesis": "mastersthesis",
    "in_journal": "article",
    "tech. report": "techreport",
    "in_book": "book",
    "preprint": "misc"
}
filename="./data/data-papers.yaml"
filename_fixed="./data/data-papers-fixed.yaml"

with open(filename, 'r') as f:
    papers = yaml.load_all(f, Loader=yaml.Loader)
    fixed_papers = []
    for p in papers:
        if "TYPE" in p:
            paper_type = p["TYPE"]
            # Normalize if paper type matches an invalid key
            p["TYPE"] = bibtex_normalize.get(paper_type, paper_type)
            fixed_papers.append(p)
    # Write to YAML file
    filestream = open(filename_fixed, "w")
    yaml.dump_all(fixed_papers, stream=filestream, sort_keys=False)
    filestream.close()
    f.close() 

# check invalid bibtex types are fixed
success = False
with open(filename_fixed, "r") as f:
    papers = yaml.load_all(f, Loader=yaml.Loader)
    warnings.simplefilter('error', UserWarning)
    try:
        for p in papers:
            if "TYPE" in p and p["TYPE"] in bibtex_normalize.keys():
                warnings.warn("Fix invalid bibtex type in " + p["MARKER"] + ": " + p["TYPE"])
        print("Successfully fixed all invalid bibtex types")
        success = True
    except Exception as e:
        print(e)
    finally:
        f.close()

if (success):
    os.replace(filename_fixed, filename)