import argparse
import sys
import os.path
import requests
import time
from bs4 import BeautifulSoup as bs
import re


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


CLEANR = re.compile('<.*?>')


def clean_html(html):
    """
    Helper: remove tags, replace unicode in raw html
    """
    clean = re.sub(CLEANR, '', html) if html != None else ''
    clean = clean.replace('\u2013', '-').replace('\u2019', "'")
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
        cols = tr.findAll('td')
        if len(cols) > 0:
            rows.append([clean_html(td.string) for td in cols])

    for tr in rows: assert len(tr) == len(header)
    return rows


"""
Download list of urls in given csv
Usage: python download-urls-list <input file>
"""
# Parameters
parser = argparse.ArgumentParser()
parser.add_argument("input", help="input file with urls", type=str)
args = parser.parse_args()

# Parse input file
urls = parse_urls(args.input)

for u in urls:
    url, output = u

    # Check each output file freshness
    if os.path.exists(output):
        ti_m = time.time() - os.path.getmtime(output)
        if ti_m < 23*60*60:
            print ("   ", output, "is fresh (less then 23 hours) not downloading")
            continue

    # Open the output file
    try:
        fout = open(output, "w", encoding="utf-8")
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit()

    # Try to download it
    print("   downloading", url)
    request = requests.get(url)

    # Exit if fail
    if request.status_code == 200:
        head_response = requests.head(url)

        # Scrape html for table of papers, save as csv
        # print("content-type" in head_response.headers)
        if "content-type" in head_response.headers:
            if "text/html" in head_response.headers["content-type"]:
                html = request.content.decode("utf-8", 'ignore')
                papers = scrape_papers(html)
                papers_csv = '\n'.join(','.join(p) for p in papers)
                fout.write(papers_csv)

        # Download non-html
        else:
            fout.write(request.text)
    else:
        print("   Query failed to run returned code of %d " %
              (request.status_code))
        sys.exit()

fout.close()