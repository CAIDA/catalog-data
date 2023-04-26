import argparse
import sys
import os.path
import requests
import time
from bs4 import BeautifulSoup as bs
import re

CLEANR = re.compile('<.*?>')

"""
Contains helper functions used in scripts/externallinks_routeviews.py
"""

def parse_urls(input):
    """
    Helper: parse urls from csv
    """
    header = True
    urls = []

    with open(input) as f:
        for line in f:
            line = line.strip()
            if line[0] == '#':
                continue
            elif line[0] != '#' and header:
                header = False
                continue
            else:
                url, output = [s.strip() for s in line.split(',')]
                urls.append((url, output))

    return urls

def clean_html(html):
    """
    Helper: remove tags, replace unicode in raw html
    """
    clean = re.sub(CLEANR, '', html) if html != None else ''
    clean = clean.replace('\u2013', '-').replace('\u2019', "'")\
            .replace(u'\xa0','').replace('\u201c', "\"")
    return clean


def scrape_papers(html):
    """
    Helper: look for table in downloaded html where each row is a paper,
    return rows as list of lists of strings
    """
    soup = bs(html, "html.parser")
    table = soup.find("table", {"id": "table_id"})

    # Table header (attributes)
    header = [clean_html(th.string) for th in table.findAll("th")]

    # Table rows (papers)
    rows = [header]
    for tr in table.findAll("tr"):
        cols = tr.findAll("td")
        links = lambda c: c.findAll("a", href=True)
        cols = [links(c)[0]['href'] if len(links(c)) == 1 else c for c in cols]
        if len(cols) > 0:
            rows.append([td if type(td)==str else clean_html(td.string) for td in cols])

    # Remove commas in attributes
    # authors should be separated by semicolon
    for tr in rows:
        assert len(tr) == len(header)
        for j, col in enumerate(tr):
            if j == 0: tr[j] = col.replace(',', ';')
            else: tr[j] = col.replace(',', '')
    
    return rows

def is_fresh(path):
    """
    Helper: returns False if file younger than 5 days
    """
    if os.path.exists(path):
        ti_m = time.time() - os.path.getmtime(path)
        if ti_m < 5*24*60*60:
            print ("   ", path, "is fresh (less then 5 days) not downloading")
            return True
        return False
    return False

def download_html(request, fout):
    """
    Helper: download html content to output file
    """
    html = request.content.decode("utf-8", 'ignore')
    papers = scrape_papers(html)
    papers_csv = '\n'.join(','.join(p) for p in papers)
    fout.write(papers_csv)

"""
Download list of urls in given csv
Usage: python download-urls-list <input file>
"""
if __name__ == "__main__":
    
    # Parameters
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="input file with urls", type=str)
    args = parser.parse_args()

    # Parse input file
    urls = parse_urls(args.input)

    for u in urls:
        url, output = u

        # Check each output file freshness
        if is_fresh(output):
            continue

        # Open the output file
        try:
            fout = open(output, "w", encoding="utf-8")
        except Exception as e:
            print(e, file=sys.stderr)
            sys.exit()

        # Try to download it
        print("    downloading", url)
        request = requests.get(url)

        # Exit if fail
        if request.status_code == 200:
            head_response = requests.head(url)

            # Scrape html for table of papers, save as csv
            # print("content-type" in head_response.headers)
            if "content-type" in head_response.headers:
                if "text/html" in head_response.headers["content-type"]:
                    download_html(request, fout)

            # Download non-html
            else:
                fout.write(request.text)
        else:
            print("   Query failed to run returned code of %d " %
                (request.status_code))
            sys.exit()

        fout.close()