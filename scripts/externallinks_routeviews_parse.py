import argparse
import re
from bs4 import BeautifulSoup as bs

parser = argparse.ArgumentParser()
parser.add_argument("-O", dest="output", help="saves yaml to output", type=str)
parser.add_argument("url",nargs=1, type=str,help="routeviews url")
args = parser.parse_args()
url = args.url[0]

def clean_html(html):
    """
    Helper: remove tags, replace unicode in raw html
    """
    CLEANR = re.compile('<.*?>')
    clean = re.sub(CLEANR, '', html) if html != None else ''
    clean = clean.replace('\u2013', '-').replace('\u2019', "'")\
            .replace(u'\xa0','').replace('\u201c', "\"")
    return clean


def scrape_papers(html_file):
    """
    Helper: returns papers in html as list
    """
    html_str = html_file.read()
    soup = bs(html_str, "html.parser")
    table = soup.find("table", {"id": "table_id"})

    # Table header (attributes)
    header = [clean_html(th.string) for th in table.findAll("th")]

    # Table rows (papers)
    papers = [header]
    for tr in table.findAll("tr"):
        cols = tr.findAll("td")
        links = lambda c: c.findAll("a", href=True)
        cols = [links(c)[0]['href'] if len(links(c)) == 1 else c for c in cols]
        if len(cols) > 0:
            papers.append([td if type(td)==str else clean_html(td.string) for td in cols])

    # Remove commas and separate authors by semicolon
    for tr in papers:
        assert len(tr) == len(header)
        for j, col in enumerate(tr):
            if j == 0: tr[j] = col.replace(',', ';')
            else: tr[j] = col.replace(',', '')
    
    # Return list of papers, excluding header
    return papers[1:]

EXTERNAL_ROUTEVIEWS_URL = 'https://www.routeviews.org/routeviews/index.php/papers/' 
EXTERNAL_ROUTEVIEWS_HTML = 'data/data-papers-routeviews.html'
EXTERNAL_ROUTEVIEWS_FILE = 'data/data-papers-routeviews.yaml'

def format_authors(authors: str):
    """
    Helper: reformat semicolon-separated string of authors given as 
            "F1. M1. Last1; F2. Last2; F3. M31. M32. Last3" to 
            "Last1, F1. M1., Last2, F2., Last3, F3. M31. M32."
    """
    formatted = []
    SUFFIXES = ["Jr."]
    NOBILIARY_PARTICLES = ["van", "va", "de", "di"]
    split_name = lambda name: re.split('\s+?', name.strip())

    # Edge case: author is "CAIDA"
    if (authors == "CAIDA"):
        return ("CAIDA", '', "CAIDA")

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

    # Return reformatted authors, and first author info for MARKER
    first_author = authors.split(';')[0]
    first_finit, first_last = split_name(first_author)[0], split_name(first_author)[-1]
    return (', '.join(formatted), first_finit.lower(), first_last.lower())

"""
Assuming routeviews html is downloaded, generates yaml for routeviews papers
Usage: 
"""
# Convert routeviews html to papers str
papers = scrape_papers(open(EXTERNAL_ROUTEVIEWS_HTML, "r", encoding="utf-8"))

# What TYPEs are in data/data-papers.yaml?
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

print(f'    generating {EXTERNAL_ROUTEVIEWS_FILE}')

# Add placeholder yaml for each paper
papers_yaml = ''
for p in papers:
    authors, date, title, src, vol, num, page, cat, url = p 
    authors, first_finit, first_last = format_authors(authors)

    # Generate marker by combining first author and either date or url
    marker_id = ''.join(year.split('-')) if len(url) == 0\
        else url.split('/')[-1][-5:].replace('.','').replace('-','')
    first_finit = first_finit.replace('.', '')
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
        "TOPKEY": "dataset:routeviews"
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
    
# What categories are in routeviews papers?
# cats = [p[-2] if p[-2] != '\"' else 'Unknown' for p in papers]
# cat_counts = {k: 0 for k in set(cats)}
# for c in cats: cat_counts[c] += 1
# print("Categories in routeviews papers:")
# print(sorted(cat_counts.items(), key=lambda x: x[1], reverse=True), '\n')

# Write to papers yaml
fout = open(EXTERNAL_ROUTEVIEWS_FILE, "w")
fout.write(papers_yaml)
fout.close()
