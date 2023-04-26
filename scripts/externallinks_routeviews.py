import lib.utils as utils
from random import randint
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
    Helper: reformat semicolon-separated string of authors given as 
            "F1. M1. Last1; F2. Last2; F3. M31. M32. Last3" to 
            "Last1, F1. M1., Last2, F2., Last3, F3. M31. M32."
    """
    formatted = []
    SUFFIXES = ["Jr."]
    NOBILIARY_PARTICLES = ["van", "va", "de", "di"]
    split_name = lambda name: re.split('\s+?', name.strip())    

    for a in authors.split(';'):
        name = split_name(a)
        formatted_name = ''
        suffix = ''

        # Edge case: illegal empty name (extra delimeter ';')
        if len(name) < 2: continue 

        # Edge case: name has suffix
        for s in SUFFIXES:
            if s in name[-1]:
                suffix = ' ' + name[-1].replace('.', '')
                name = name[:len(name)-1]

        # Edge case: last name has nobiliary particle, join into last name
        last = [name[-1]]
        for i in range(len(name)-1, -1, -1):
            n = name[i].strip()
            if n in NOBILIARY_PARTICLES:
                last.append(name.pop(i))
        if len(last) > 1:
            last.reverse()
            name.pop(-1)
            name.append(' '.join(last).replace('.', ''))
            formatted_name = name

        # Handle names with or without middle initials
        if len(name) > 2: 
            finitial, minitials, last = name[0], name[1:-1], name[-1]
            mid = ' '.join([f'{m}' for m in minitials])
            formatted_name = f"{last}{suffix}, {finitial} {mid}"
        else:
            assert len(name) == 2
            finitial, last = name
            formatted_name = f"{last}{suffix}, {finitial}"

        # Edge case: only last initial is given, remove period
        if '.' in last: 
            formatted_name = formatted_name.replace('.', '', 1)    
        formatted.append(formatted_name) 

    # Return reformatted authors string, first author info for MARKER
    first_author = authors.split(';')[0]
    first_finit, first_last = split_name(first_author)[0], split_name(first_author)[-1]
    return (', '.join(formatted), first_finit.lower(), first_last.lower())

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
    authors, first_finit, first_last = format_authors(authors)
    marker_id = randint(10**4, 10**5-1)
    marker = f"{date.split('-')[0]}_{first_last}_{first_finit}_{marker_id}"    
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
        "MARKER": marker,
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
        yaml_str += f"{k}: \"{v}\"\n"
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
