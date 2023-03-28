import argparse
import json
import string

def parse_papers(input):
    """
    Helper: parse papers from csv
    """
    header = True
    papers = []

    with open(input, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line[0] == '#':
                continue
            elif line[0] != '#' and header:
                header = False
                continue
            else:
                paper = [s.strip() for s in line.split(',')]
                papers.append(paper)

    return papers

"""
Create json in sources/papers for each routeviews paper in csv-like input
Usage: python add-routeviews-papers.py <input file>
"""

# Parameters
parser = argparse.ArgumentParser()
parser.add_argument("input", help="input file with routeviews papers", type=str)
args = parser.parse_args()

# Parse input file
papers = parse_papers(args.input)

# Add placeholder objects containing link
for p in papers:
    author, date, title, *_, category, url = p
    year = date.split('-')[0]
    ftitle = title.lower().replace(' ', '_')
    fdir = "sources/paper/"

    # Remove puncutation in file name
    to_remove = [":", "&", "'", "(", ")", "?", "#", "/", "*"]
    for c in to_remove: 
        ftitle = ftitle.replace(c, '')
    fname = f"{fdir}{year}_{ftitle}.json"
    fout = open(fname, "w")

    # Write paper json
    p_json = {}
    p_json["name"] = title
    p_json["links"] = [{"to": "dataset:routeviews", "label": "used by"}]
    fout.write(json.dumps(p_json, indent=4))
    fout.close()
