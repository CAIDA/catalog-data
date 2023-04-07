import re
import requests

# Helpers from download-urls-list.py
from download_urls_list import download_html, is_fresh

ROUTEVIEWS_URL = "https://www.routeviews.org/routeviews/index.php/papers/"
PAPERS_PATH = "data/routeviews-data.txt"
YAML_PATH = "data/data-papers-routeviews.yaml"

def parse_papers(input):
    """
    Helper: parse routeviews papers data from csv
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
                papers.append(line.split(','))
    return papers

def format_authors(authors):
    """
    Helper: reformat string of authors given as "F1. M1. Last1; F2. Last2"
            to "Last1, F1. M1., Last2, F2."
    """
    formatted = []
    for a in authors.split(';'):
        name = re.split('.\s+?', a.strip())
        finitial = name[0]
        last = name[-1]
        minitial = name[1] if len(name) > 2 else ''
        formatted.append(f"{last}, {finitial}.{' '+minitial+'.' if minitial != '' else ''}")
    return ', '.join(formatted)

"""
Downloads papers csv from routeviews.org, create yaml entry in 
data/data-papers-routeviews.yaml for each routeviews paper
Usage: python externallinks_routeviews.py
"""

# Download papers csv to data/routeviews-data.txt

request = requests.get(ROUTEVIEWS_URL)
if not is_fresh(PAPERS_PATH):
    print(f"    downloading {PAPERS_PATH}")
    download_html(request, open(PAPERS_PATH, "w", encoding="utf-8"))

# What TYPEs in existing yaml?
# types = []
# type_counts = {}
# with open("data/data-papers.yaml", encoding='utf-8') as big_yaml:
#     for line in big_yaml:
#         line = line.strip()
#         if line.startswith("TYPE"):
#             ptype = re.findall("TYPE.*?:.*?\"(.*?)\".*", line)[0]
#             types.append(ptype)
#     type_counts = {t: 0 for t in types}
#     for t in types: type_counts[t] += 1
# print("Paper TYPE in data/data-papers.yaml")
# print(sorted(type_counts.items(), key=lambda x: x[1], reverse=True), '\n')

print(f'    generating {YAML_PATH}')

# Add placeholder yaml for each paper
papers = parse_papers(PAPERS_PATH)
papers_yaml = ''
for p in papers:
    authors, date, title, src, vol, num, page, cat, url = p   
    authors = format_authors(authors)
    year = '-'.join(date.split('-')[0:2])
    cat = cat.lower()
    ptype = 'in_proceedings' if 'conference' in cat else\
            'in_journal' if cat == 'peer' else\
            'MSc thesis' if cat == 'master thesis' else\
            'thesis' if 'thesis' in cat else\
            'in_book' if cat == 'book' else\
            'presentation' if cat == 'presentation' else\
            'online' if cat == 'self' else ''
    yaml = {
        "MARKER": "",
        "TYPE": ptype,
        "AUTHOR": authors,
        "TITLE": title,
        "CTITLE": src,
        "PUBLISH": src,
        "SERIAL": src,
        "YEAR": year,
        "VOLUME": vol,
        "PAGE": page,
        "URL": url,
        "ABS": "",
    }

    # Set yaml by category (peer, conference, etc.)
    if "conference" in cat:
        del yaml["PUBLISH"]
        del yaml["SERIAL"]
        yaml["CTITLE"] = src
        yaml["VOLUME"] = vol        
    elif cat == "peer":
        del yaml["CTITLE"]
        del yaml["PUBLISH"]
    else:
        del yaml["CTITLE"]
        del yaml["SERIAL"]
        del yaml["VOLUME"]

    # Yaml dict to string
    yaml_str = '---\n'
    for k, v in yaml.items():
        yaml_str += f"{k}\t: \"{v}\"\n"
    yaml_str += '\n'
    papers_yaml += yaml_str
    
# What categories are there among routeviews papers?
# cats = [p[-2] if p[-2] != '\"' else 'Unknown' for p in papers]
# cat_counts = {k: 0 for k in set(cats)}
# for c in cats: cat_counts[c] += 1
# print("Categories in routeviews papers:")
# print(sorted(cat_counts.items(), key=lambda x: x[1], reverse=True), '\n')

# Write to papers yaml
fout = open(YAML_PATH, "w")
fout.write(papers_yaml)
fout.close()
