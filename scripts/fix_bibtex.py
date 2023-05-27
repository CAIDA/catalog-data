#!  /usr/bin/env python3
import yaml
# import subprocess

fixed_paper = open("./data/data-papers-fixed.yaml", "w+")
# Match invalid bibtex types to valid types
normalize = {
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

with open('./data/data-papers.yaml', 'r') as f:
    papers = yaml.load_all(f, Loader=yaml.FullLoader)
    fixed_papers = []
    for p in papers:
        if "TYPE" in p:
            paper_type = p["TYPE"]
            # Normalize if paper type matches an invalid key
            p["TYPE"] = normalize.get(paper_type, paper_type)
            fixed_papers.append(p)         
    # Write to YAML file
    fixed_paper.write(yaml.dump_all(fixed_papers, line_break="4"))
            
# check invalid bibtex types are fixed
with open("./data/data-papers-fixed.yaml", "r") as f:
    papers = yaml.load_all(f, Loader=yaml.FullLoader)
    for p in papers:
        if "TYPE" in p and p["TYPE"] in normalize.keys():
            print("Invalid bibtex type: " + p["TYPE"])
        
    # subprocess.run(["git","mv",fname,filename])``